from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from .nodes import (
    generate_search_queries,
    search_github,
    to_validate_projects,
    validate_project
)
from .state import OverallState

load_dotenv()

graph = StateGraph(OverallState)

# 添加节点
graph.add_node("generate_search_queries", generate_search_queries)
graph.add_node("search_github", search_github)
graph.add_node("validate_project", validate_project)

# 定义流程
graph.add_edge(START, "generate_search_queries")
graph.add_edge("generate_search_queries", "search_github")
# 使用条件边，将项目分发到并行验证节点（Send 会自动处理）
graph.add_conditional_edges("search_github", to_validate_projects, "validate_project")
graph.add_edge("validate_project", END)

graph = graph.compile()

