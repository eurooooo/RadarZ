import os
from langgraph.types import Command, Send
from langchain.chat_models import init_chat_model
from src.searchagent.schemas import SearchQueryList, ValidateCriteriaList, ProjectValidation
from .prompts import (
    generate_search_queries_prompt,
    validate_criteria_prompt,
    validate_project_prompt
)
from .state import OverallState, ProjectValidationState
from src.github.github_client import GitHubClient
from langgraph.graph import END


MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER") or None

def get_llm():
    return init_chat_model(model=MODEL_NAME, model_provider=MODEL_PROVIDER, temperature=0)

def generate_search_queries(state: OverallState) -> OverallState:
    """生成搜索查询"""
    messages = generate_search_queries_prompt.format_messages(
        user_input=state['user_input']
    )
    llm = get_llm()
    response = llm.with_structured_output(SearchQueryList).invoke(messages)
    print(f"🔍 Generated search queries: {response.query}")
    # return {'search_queries': response.query}
    return {'search_queries': response.query}


def search_github(state: OverallState) -> OverallState:
    """根据搜索查询在 GitHub 上搜索项目"""
    github_token = os.getenv("GITHUB_TOKEN")
    github_client = GitHubClient(token=github_token)
    
    search_queries = state.get('search_queries', [])
    all_results = []
    
    for query in search_queries:
        print(f"🔍 Searching GitHub with query: {query}")
        results = github_client.search_repositories(
            query=query,
            limit=2,
            # sort="stars",
            # order="desc"
        )
        all_results.extend(results)
        print(f"   Found {len(results)} repositories")
    
    # 去重（基于 full_name）
    seen = set()
    unique_results = []
    for repo in all_results:
        full_name = repo.get('full_name')
        if full_name and full_name not in seen:
            seen.add(full_name)
            unique_results.append(repo)
    
    print(f"✅ Total unique repositories found: {len(unique_results)}")
    return {'github_results': unique_results}

def generate_validate_criteria(state: OverallState) -> OverallState:
    """生成验证标准"""
    llm = get_llm()
    messages = validate_criteria_prompt.format_messages(
        user_input=state['user_input'],
    )
    response = llm.with_structured_output(ValidateCriteriaList).invoke(messages)
    print(f"🔍 Generated validate criteria: {response.validate_criteria}")
    return {'validate_criteria': response.validate_criteria}

def to_validate_projects(state: OverallState):
    """LangGraph condition function that dispatches projects for parallel validation."""
    github_results = state.get('github_results', [])
    validate_criteria = state.get('validate_criteria', [])
    user_input = state.get('user_input', '')
    
    if not github_results:
        # 当没有结果时，返回 END 常量
        return Command(goto=END)
    
    send_list = [
        Send("validate_project", {
            "repo": repo,
            "validate_criteria": validate_criteria,
            "user_input": user_input
        })
        for repo in github_results
    ]
    
    # 返回 Send 列表，LangGraph 会自动并行处理
    return Command(goto=send_list)


def validate_project(state: ProjectValidationState) -> OverallState:
    """处理单个项目的验证（由 Send 并行调用）"""
    repo = state['repo']
    validate_criteria = state.get('validate_criteria', [])
    user_input = state.get('user_input', '')
    
    full_name = repo.get('full_name', '')
    project_name = repo.get('name', full_name)
    project_description = repo.get('description', '') or ''
    print(f"🔍 Validating project: {state['repo']['full_name']}")
    
    # 获取 README 内容
    github_token = os.getenv("GITHUB_TOKEN")
    github_client = GitHubClient(token=github_token)
    readme_content = github_client.get_repository_readme(full_name)
    # 限制 README 预览长度（避免 token 过多）
    readme_preview = ''
    if readme_content:
        # 取前 2000 个字符作为预览
        readme_preview = readme_content[:500]
        if len(readme_content) > 500:
            readme_preview += "\n\n...(README 内容已截断)"
    else:
        readme_preview = "无 README 内容"
    
    # 格式化验证标准为字符串
    criteria_text = '\n'.join([f"{i+1}. {criterion}" for i, criterion in enumerate(validate_criteria)])
    
    # 使用 LLM 进行验证
    try:
        llm = get_llm()
        messages = validate_project_prompt.format_messages(
            user_input=user_input,
            validate_criteria=criteria_text,
            project_name=project_name,
            project_description=project_description,
            readme_preview=readme_preview
        )
        response = llm.with_structured_output(ProjectValidation).invoke(messages)
        is_validated = response.is_validated
        
        project_data = {
            **repo,
            "is_validated": is_validated
        }
        
        status_icon = "✅" if is_validated else "❌"
        print(f"   {status_icon} Validated: {full_name} - {'符合' if is_validated else '不符合'}")

        # 只返回通过验证的项目
        if is_validated:
            return {'validated_projects': [project_data]}
        else:
            return {'validated_projects': []}
    except Exception as e:
        print(f"   ⚠️ 验证失败 {full_name}: {e}")
        # 验证失败时，默认不通过
        return {'validated_projects': []}

