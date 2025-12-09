from typing import TypedDict, Dict, Annotated
from schemas import SearchQueryList
import operator

class ResearchState(TypedDict):
    # 输入
    project_name: str
    readme: str
    github_url: str
    repo_stats: Dict  # stars, language, topics, etc.
    
    # Node 1 输出
    search_queries: Annotated[SearchQueryList, operator.add]
    
    # # Node 2 输出
    # raw_search_results: Annotated[List[Dict], operator.add]  # 支持增量添加
    # deduplicated_results: List[Dict]
    
    # # Node 3 输出
    # filtered_results: List[Dict]
    
    # # Node 4 输出
    # final_summary: str