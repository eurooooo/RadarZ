from pydantic import BaseModel


class Project(BaseModel):
    """项目数据模型"""

    id: str
    title: str
    authors: str
    date: str
    description: str
    tags: list[str]
    stars: int
    forks: int
    image_url: str | None = None  # GitHub Open Graph 图片 URL

