from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class ThoughtAction(BaseModel):
    """思考-行动的结构化输出"""
    thought: str = Field(description="当前步骤的思考内容，说明为什么要执行这个行动")
    action: Literal["search", "filter", "summarize", "finish"] = Field(
        description="要执行的动作：search(搜索)、filter(过滤)、summarize(总结)、finish(完成)"
    )
    action_input: Optional[str] = Field(
        default=None,
        description="动作的输入参数，例如搜索查询、过滤条件等"
    )

class SearchQueryList(BaseModel):
    """搜索查询列表"""
    queries: List[str] = Field(
        description="用于网络搜索的搜索查询列表"
    )

class RelevanceAssessment(BaseModel):
    """单个搜索结果的相关性评估结果"""
    is_relevant: bool = Field(description="是否与项目相关")
    relevance_score: float = Field(description="相关性分数 0-1")
    reason: str = Field(description="评估理由")

class RelevanceAssessmentList(BaseModel):
    """批量搜索结果的相关性评估结果列表"""
    assessments: List[RelevanceAssessment] = Field(
        description="每个搜索结果的相关性评估，顺序与输入的搜索结果列表一致"
    )

class FinalSummary(BaseModel):
    """最终总结"""
    summary: str = Field(description="项目总结，使用 Markdown 格式")

