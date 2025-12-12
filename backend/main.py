from typing import List, Optional
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.models import Project
from src.github import ProjectService
from src.agent.graph import graph
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


@app.get("/summary/readme")
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

@app.get("/summary")
async def get_summary(
    repo_name: str = Query(..., description="仓库全名，如 owner/repo"),
):
    """
    GET 方式获取 README 摘要，便于前端直接调用。
    """
    readme_text = project_service.get_repository_readme(repo_name, None)
    if not readme_text:
        raise HTTPException(
            status_code=404, detail="缺少 README 内容，且无法通过仓库名获取。"
        )
    input_data = {
        "project_name": repo_name,
        "readme": readme_text,
    }
    result = graph.invoke(input_data)
    return {"repo": repo_name, "summary": result['final_summary']}


@app.get("/new")
async def get_new_projects() -> int:
    """获取新的 GitHub 项目"""
    repos = project_service.get_new_repositories(days=20, min_stars=2000, language="Python", limit=1000)
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "readmes"
    output_dir.mkdir(exist_ok=True)
    
    for repo in repos:
        repo_name = repo.get("full_name")
        readme = project_service.get_repository_readme(repo_name)
        
        if readme:
            # 生成安全的文件名
            safe_repo_name = repo_name.replace("/", "_").replace("\\", "_")
            safe_repo_name = "".join(c for c in safe_repo_name if c.isalnum() or c in ('_', '-', '.'))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_repo_name}_{timestamp}.md"
            filepath = output_dir / filename
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {repo_name}\n\n")
                f.write(f"**GitHub URL:** https://github.com/{repo_name}\n\n")
                f.write(f"**获取时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(readme)
            
            print(f"💾 README saved: {filepath}")

    return len(repos)