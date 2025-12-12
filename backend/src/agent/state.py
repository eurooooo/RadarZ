from typing import TypedDict, Annotated
import operator

class ResearchState(TypedDict, total=False):
    # 输入
    project_name: str
    readme: str
    
    # Node 1 输出
    search_queries: Annotated[list[str], operator.add]
    
    # Node 2 输出（由 Send 并行调用，使用 operator.add 合并）
    search_results: Annotated[list[dict], operator.add]  # 支持增量添加
    
    # # Node 3 输出（聚合和去重后，覆盖之前的结果）
    # deduplicated_results: List[Dict]
    
    # # Node 4 输出
    filtered_results: Annotated[list[dict], operator.add]
    
    # # Node 5 输出
    final_summary: str

class WebSearchState(TypedDict):
    search_query: str