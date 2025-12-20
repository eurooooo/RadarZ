import os
from langgraph.types import Send
from langchain.chat_models import init_chat_model
from src.searchagent.schemas import SearchQueryList
from .prompts import (
    generate_search_queries_prompt
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
            limit=5,
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


def to_validate_projects(state: OverallState):
    """LangGraph condition function that dispatches projects for parallel validation."""
    github_results = state.get('github_results', [])
    
    if not github_results:
        # 当没有结果时，返回 END 常量
        return END
    
    # 返回 Send 列表，LangGraph 会自动并行处理
    return [
        Send("validate_project", {
            "repo": repo
        })
        for repo in github_results
    ]


def validate_project(state: ProjectValidationState) -> OverallState:
    """处理单个项目的验证（由 Send 并行调用）"""
    repo = state['repo']
    
    full_name = repo.get('full_name', '')
    
    # 直接接受所有项目，不进行验证
    project_data = {
        **repo,
        'is_validated': True
    }
    print(f"   ✅ Validated: {full_name}")
    # 返回所有项目，LangGraph 会自动合并（使用 operator.add）
    return {'validated_projects': [project_data]}

