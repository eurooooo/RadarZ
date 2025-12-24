# graph.py
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from .nodes import (
    generate_search_queries,
    generate_validate_criteria,
    search_github,
    to_validate_projects,
    validate_project
)
from .state import OverallState

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

# 将 compiled_graph 重命名为 graph，以匹配导入期望
graph = build_graph()