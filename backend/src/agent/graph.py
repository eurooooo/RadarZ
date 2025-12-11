from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from .nodes import generate_queries, to_web_research, web_research, filter_irrelevant_results, generate_final_summary, test_generate_final_summary
from .state import ResearchState

load_dotenv()

graph = StateGraph(ResearchState)
graph.add_node(generate_queries)
graph.add_node(web_research)
graph.add_node(filter_irrelevant_results)
graph.add_node(generate_final_summary)

graph.add_edge(START, "generate_queries")
graph.add_conditional_edges("generate_queries", to_web_research, "web_research")
graph.add_edge("web_research", "filter_irrelevant_results")
graph.add_edge("filter_irrelevant_results", "generate_final_summary")
graph.add_edge("generate_final_summary", END)

graph = graph.compile()

test_graph = StateGraph(ResearchState)
test_graph.add_node(test_generate_final_summary)
test_graph.add_edge(START, "test_generate_final_summary")
test_graph.add_edge("test_generate_final_summary", END)
test_graph = test_graph.compile()