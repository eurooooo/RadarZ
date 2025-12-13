from pydantic import BaseModel, Field

class ProjectValidation(BaseModel):
    """项目验证结果"""
    is_valid: bool = Field(description="项目是否符合验证标准")


class SearchQueryList(BaseModel):
    query: list[str] = Field(
        description="用于github搜索的搜索查询列表"
    )