import os
from langgraph.types import Command, Send
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.searchagent.schemas import SearchQueryList, ValidateCriteriaList, ProjectValidation
from .prompts import (
    generate_search_queries_prompt,
    validate_criteria_prompt,
    validate_project_prompt,
    validate_project_pro_prompt
)
from .state import OverallState, ProjectValidationState, ProjectValidationProState
from src.github.github_client import GitHubClient
from langgraph.graph import END
from .tools import validation_tools


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
            limit=10,
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
            readme_content=readme_content
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


def validate_project_pro(state: ProjectValidationProState) -> ProjectValidationProState:
    """升级版项目验证节点，支持工具调用"""
    repo = state['repo']
    validate_criteria = state.get('validate_criteria', [])
    user_input = state.get('user_input', '')
    messages = state.get('messages', [])
    iteration_count = state.get('iteration_count', 0)
    
    full_name = repo.get('full_name', '')
    project_name = repo.get('name', full_name)
    project_description = repo.get('description', '') or ''
    
    if iteration_count == 0:
        print(f"🔍 Validating project (pro): {full_name}")
    
    # 获取 README 内容（仅在第一次迭代时）
    readme_content = ''
    if iteration_count == 0:
        github_token = os.getenv("GITHUB_TOKEN")
        github_client = GitHubClient(token=github_token)
        readme_content = github_client.get_repository_readme(full_name)
    
    # 格式化验证标准为字符串
    criteria_text = '\n'.join([f"{i+1}. {criterion}" for i, criterion in enumerate(validate_criteria)])
    
    # 构建消息
    if iteration_count == 0:
        # 第一次调用，构建初始消息（包含 system message 和 user message）
        initial_messages = validate_project_pro_prompt.format_messages(
            user_input=user_input,
            validate_criteria=criteria_text,
            project_name=project_name,
            project_description=project_description,
            readme_content=readme_content
        )
        all_messages = initial_messages
    else:
        # 后续调用，使用已有的消息历史，并在末尾添加迭代次数提示
        iteration_hint = HumanMessage(
            content=f"⚠️ 当前迭代次数: {iteration_count}/3。如果已达到或超过 3 次，请立即停止调用工具并基于已有信息做出最终判断。"
        )
        all_messages = messages + [iteration_hint]
    
    # 绑定工具到 LLM
    llm = get_llm()
    llm_with_tools = llm.bind_tools(validation_tools)
    
    # 调用 LLM
    response = llm_with_tools.invoke(all_messages)
    
    # 由于 messages 使用 operator.add，只需要返回新增的消息
    # 第一次调用时返回初始消息 + response，后续调用时只返回 response
    if iteration_count == 0:
        new_messages = initial_messages + [response]
    else:
        new_messages = [response]
    
    # 更新状态
    return {
        'messages': new_messages,
        'iteration_count': iteration_count + 1
    }


def should_continue(state: ProjectValidationProState) -> str:
    """判断是否需要继续调用工具"""
    
    messages = state.get('messages', [])
    if not messages:
        return "end"
    
    last_message = messages[-1]
    
    # 检查最后一条消息是否有 tool_calls
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    else:
        return "end"


def execute_tools(state: ProjectValidationProState) -> ProjectValidationProState:
    """执行工具调用并更新状态"""
    messages = state.get('messages', [])
    
    if not messages:
        return state
    
    last_message = messages[-1]
    
    # 检查是否有工具调用
    if not (hasattr(last_message, 'tool_calls') and last_message.tool_calls):
        return state
    
    # 创建工具映射
    tool_map = {tool.name: tool for tool in validation_tools}
    
    # 执行工具调用并创建 ToolMessage
    tool_messages = []
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call.get('name', '')
        tool_args = tool_call.get('args', {})
        tool_call_id = tool_call.get('id', '')
        
        # 执行工具
        if tool_name in tool_map:
            try:
                tool = tool_map[tool_name]
                tool_result = tool.invoke(tool_args)
                
                # 创建 ToolMessage
                tool_message = ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call_id
                )
                tool_messages.append(tool_message)
                
                print(f"   🔧 工具调用: {tool_name} - {tool_args}")
            except Exception as e:
                # 工具调用失败，创建错误消息
                error_message = ToolMessage(
                    content=f"工具调用失败: {str(e)}",
                    tool_call_id=tool_call_id
                )
                tool_messages.append(error_message)
                print(f"   ⚠️ 工具调用失败 {tool_name}: {e}")
        else:
            # 未知工具
            error_message = ToolMessage(
                content=f"未知工具: {tool_name}",
                tool_call_id=tool_call_id
            )
            tool_messages.append(error_message)
    
    # 由于 messages 使用 operator.add，只需要返回新增的 tool_messages
    # 它们会被自动添加到现有的 messages 中
    return {
        'messages': tool_messages
    }


def to_validate_projects_pro(state: OverallState):
    """LangGraph condition function that dispatches projects for parallel validation using validate_project_pro."""
    github_results = state.get('github_results', [])
    validate_criteria = state.get('validate_criteria', [])
    user_input = state.get('user_input', '')
    
    if not github_results:
        # 当没有结果时，返回 END 常量
        return Command(goto=END)
    
    send_list = [
        Send("validate_project_pro_wrapper", {
            "repo": repo,
            "validate_criteria": validate_criteria,
            "user_input": user_input,
            "messages": [],
            "iteration_count": 0
        })
        for repo in github_results
    ]
    
    # 返回 Send 列表，LangGraph 会自动并行处理
    return Command(goto=send_list)


def validate_project_pro_wrapper(state: ProjectValidationProState) -> OverallState:
    """包装节点：调用 validation_pro_graph 并返回 OverallState"""
    from .graph import validation_pro_graph
    
    # 运行 validation_pro_graph
    final_state = validation_pro_graph.invoke(state)
    
    # 从消息历史中提取最终结果
    messages = final_state.get('messages', [])
    repo = state['repo']
    
    # 从最后一条 AI 消息中提取验证结果
    # 如果最后一条消息没有 tool_calls，说明已经做出最终判断
    is_validated = False
    if messages:
        last_message = messages[-1]
        # 检查是否有 tool_calls，如果没有，说明已经完成验证
        if not (hasattr(last_message, 'tool_calls') and last_message.tool_calls):
            # 尝试从消息内容中提取验证结果
            content = getattr(last_message, 'content', '')
            if content:
                # 使用结构化输出提取验证结果
                try:
                    llm = get_llm()
                    # 构建提取提示
                    extract_prompt = f"""请从以下消息中提取项目验证结果。消息内容：
{content}

请判断项目是否符合验证标准，返回 JSON 格式：
{{"is_validated": true/false}}
"""
                    response = llm.with_structured_output(ProjectValidation).invoke(extract_prompt)
                    is_validated = response.is_validated
                except Exception as e:
                    # 如果结构化输出失败，使用简单的文本匹配
                    print(f"   ⚠️ 结构化输出失败，使用文本匹配: {e}")
                    if '符合' in content or 'validated' in content.lower() or 'true' in content.lower() or '通过' in content:
                        is_validated = True
    
    project_data = {
        **repo,
        "is_validated": is_validated
    }
    
    status_icon = "✅" if is_validated else "❌"
    print(f"   {status_icon} Validated (pro): {repo.get('full_name', '')} - {'符合' if is_validated else '不符合'}")
    
    # 只返回通过验证的项目
    if is_validated:
        return {'validated_projects': [project_data]}
    else:
        return {'validated_projects': []}

