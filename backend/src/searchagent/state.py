from typing import TypedDict, List, Dict, Any, Optional, Annotated
import operator

class OverallState(TypedDict):
    user_input: str
    search_queries: List[str]
    validate_criteria: List[str]
    github_results: List[Dict[str, Any]]  # GitHub 搜索的原始结果
    validated_projects: Annotated[List[Dict[str, Any]], operator.add]  # 经过验证的项目，支持增量添加

class ProjectValidationState(TypedDict):
    """单个项目验证的状态"""
    repo: Dict[str, Any]  # 单个项目的数据
    validate_criteria: List[str]  # 验证标准列表
    user_input: str  # 用户输入

class ProjectValidationProState(TypedDict):
    """升级版项目验证的状态（支持工具调用）"""
    repo: Dict[str, Any]  # 单个项目的数据
    validate_criteria: List[str]  # 验证标准列表
    user_input: str  # 用户输入
    messages: Annotated[List[Dict[str, Any]], operator.add]  # LLM 消息历史
    iteration_count: int  # ReAct 循环迭代次数，用于防止无限循环

