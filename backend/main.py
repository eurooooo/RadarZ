from typing import List, Optional
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.models import Project
from src.github import ProjectService

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

github_token = os.getenv("GITHUB_TOKEN")
project_service = ProjectService(github_token=github_token)

@app.get("/projects", response_model=List[Project])
async def get_projects() -> List[Project]:
    """获取当日的 GitHub trending 项目"""
    return project_service.get_trending_projects(limit=25)


@app.get("/summaries/readme")
async def summarize_readme_get(
    repo_name: str = Query(..., description="仓库全名，如 owner/repo"),
    ref: Optional[str] = Query(None, description="分支名或 commit"),
):
    """
    GET 方式生成 README 摘要，便于前端直接调用。
    """
    readme_text = project_service.get_repository_readme(repo_name, ref)
    if not readme_text:
        raise HTTPException(
            status_code=404, detail="缺少 README 内容，且无法通过仓库名获取。"
        )

    return {"repo": repo_name, "summary": readme_text}