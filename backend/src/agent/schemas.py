from pydantic import BaseModel, Field

class SearchQueryList(BaseModel):
    query: list[str] = Field(
        description="用于网络搜索的搜索查询列表"
    )

class RelevanceAssessment(BaseModel):
    """单个搜索结果的相关性评估结果"""
    is_relevant: bool = Field(description="是否与项目相关")
    relevance_score: float = Field(description="相关性分数 0-1")

class RelevanceAssessmentList(BaseModel):
    """批量搜索结果的相关性评估结果列表"""
    assessments: list[RelevanceAssessment] = Field(
        description="每个搜索结果的相关性评估，顺序与输入的搜索结果列表一致"
    )

class FinalSummary(BaseModel):
    summary: str = Field(description="项目总结")