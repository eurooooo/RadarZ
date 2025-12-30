# graph.py
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from .nodes import (
    generate_search_queries,
    generate_validate_criteria,
    search_github,
    to_validate_projects,
    validate_project,
    validate_project_pro,
    should_continue,
    execute_tools,
    to_validate_projects_pro,
    validate_project_pro_wrapper
)
from .state import OverallState, ProjectValidationProState

load_dotenv()

def build_graph():
    graph = StateGraph(OverallState)
    
    # 添加节点
    graph.add_node("generate_search_queries", generate_search_queries)
    graph.add_node("search_github", search_github)
    graph.add_node("generate_validate_criteria", generate_validate_criteria)
    graph.add_node("to_validate_projects", to_validate_projects)
    graph.add_node("validate_project", validate_project)
    
    # 并行启动
    graph.add_edge(START, "generate_search_queries")
    graph.add_edge(START, "generate_validate_criteria")
    
    # 链式
    graph.add_edge("generate_search_queries", "search_github")
    
    # 汇聚
    graph.add_edge("search_github", "to_validate_projects")
    graph.add_edge("generate_validate_criteria", "to_validate_projects")
    
    # 结束
    graph.add_edge("validate_project", END)
    
    return graph.compile()


def build_validation_pro_graph():
    """构建升级版验证流程的图（支持工具调用）"""
    graph = StateGraph(ProjectValidationProState)
    
    # 添加节点
    graph.add_node("validate_project_pro", validate_project_pro)
    graph.add_node("execute_tools", execute_tools)
    
    # 从开始到验证节点
    graph.add_edge(START, "validate_project_pro")
    
    # 从验证节点到条件判断
    graph.add_conditional_edges(
        "validate_project_pro",
        should_continue,
        {
            "tools": "execute_tools",  # 如果有工具调用，执行工具
            "end": END  # 如果没有工具调用，结束
        }
    )
    
    # 从工具执行节点回到验证节点（形成循环）
    graph.add_edge("execute_tools", "validate_project_pro")
    
    return graph.compile()


def build_graph_pro():
    """构建使用 validate_project_pro 的主图"""
    graph = StateGraph(OverallState)
    
    # 添加节点
    graph.add_node("generate_search_queries", generate_search_queries)
    graph.add_node("search_github", search_github)
    graph.add_node("generate_validate_criteria", generate_validate_criteria)
    graph.add_node("to_validate_projects_pro", to_validate_projects_pro)
    graph.add_node("validate_project_pro_wrapper", validate_project_pro_wrapper)
    
    # 并行启动
    graph.add_edge(START, "generate_search_queries")
    graph.add_edge(START, "generate_validate_criteria")
    
    # 链式
    graph.add_edge("generate_search_queries", "search_github")
    
    # 汇聚
    graph.add_edge("search_github", "to_validate_projects_pro")
    graph.add_edge("generate_validate_criteria", "to_validate_projects_pro")
    
    # 结束
    graph.add_edge("validate_project_pro_wrapper", END)
    
    return graph.compile()


# 将 compiled_graph 重命名为 graph，以匹配导入期望
graph = build_graph()

# 升级版验证图（子图）
validation_pro_graph = build_validation_pro_graph()

# 使用 validate_project_pro 的主图
graph_pro = build_graph_pro()