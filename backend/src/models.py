from pydantic import BaseModel


class Project(BaseModel):
    """项目数据模型"""

    id: str
    title: str
    authors: str
    description: str
    tags: list[str]
    stars: int
    forks: int
    language: str | None = None  # 项目主要编程语言

