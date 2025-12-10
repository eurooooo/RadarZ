from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from .nodes import generate_queries, to_web_research, web_research
from .state import ResearchState

load_dotenv()

graph = StateGraph(ResearchState)
graph.add_node(generate_queries)
graph.add_node(web_research)
graph.add_edge(START, "generate_queries")
graph.add_conditional_edges("generate_queries", to_web_research, "web_research")
graph.add_edge("web_research", END)

graph = graph.compile()
