from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from nodes import generate_queries
from state import ResearchState

load_dotenv()

graph = StateGraph(ResearchState)
graph.add_node(generate_queries)
# graph.add_node(search_and_deduplicate)
# graph.add_node(filter_irrelevant_results)
# graph.add_node(generate_final_summary)
graph.add_edge(START, "generate_queries")
# graph.add_edge("generate_queries", "search_and_deduplicate")
# graph.add_edge("search_and_deduplicate", "filter_irrelevant_results")
# graph.add_edge("filter_irrelevant_results", "generate_final_summary")
# graph.add_edge("generate_final_summary", END)
graph = graph.compile()
