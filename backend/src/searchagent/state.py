from typing import TypedDict, List, Dict, Any, Optional, Annotated
import operator

class OverallState(TypedDict):
    user_input: str
    search_queries: List[str]
    github_results: List[Dict[str, Any]]  # GitHub 搜索的原始结果
    validated_projects: Annotated[List[Dict[str, Any]], operator.add]  # 经过验证的项目，支持增量添加

class ProjectValidationState(TypedDict):
    """单个项目验证的状态"""
    repo: Dict[str, Any]  # 单个项目的数据

