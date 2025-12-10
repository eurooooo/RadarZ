from typing import TypedDict, Dict, List, Annotated
import operator
from .schemas import SearchQueryList

class ResearchState(TypedDict, total=False):
    # 输入
    project_name: str
    readme: str
    github_url: str
    
    # Node 1 输出
    search_queries: Annotated[SearchQueryList, operator.add]
    
    # Node 2 输出（由 Send 并行调用，使用 operator.add 合并）
    raw_search_results: Annotated[List[Dict], operator.add]  # 支持增量添加
    
    # # Node 3 输出（聚合和去重后，覆盖之前的结果）
    # deduplicated_results: List[Dict]
    
    # # Node 4 输出
    # filtered_results: List[Dict]
    
    # # Node 5 输出
    # final_summary: str

class WebSearchState(TypedDict):
    search_query: str