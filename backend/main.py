from typing import List
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.models import Project
from src.project_service import ProjectService

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

# 初始化项目服务
# 可以从环境变量获取 GitHub token（可选）
github_token = os.getenv("GITHUB_TOKEN")
project_service = ProjectService(github_token=github_token)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/projects", response_model=List[Project])
async def get_projects() -> List[Project]:
    """获取当日的 GitHub trending 项目"""
    return project_service.get_trending_projects(limit=25)