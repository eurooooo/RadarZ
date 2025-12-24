from typing import List, Optional
import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from src.models import Project
from src.github import ProjectService
from src.agent.graph import graph
from src.searchagent.graph import graph as search_graph
from src.React.graph import graph as react_graph
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

# @app.get("/summary")
# async def get_summary(
#     repo_name: str = Query(..., description="仓库全名，如 owner/repo"),
# ):
#     """
#     GET 方式获取 README 摘要，便于前端直接调用。
#     使用传统的 LangGraph 工作流。
#     """
#     readme_text = project_service.get_repository_readme(repo_name, None)
#     if not readme_text:
#         raise HTTPException(
#             status_code=404, detail="缺少 README 内容，且无法通过仓库名获取。"
#         )
#     input_data = {
#         "project_name": repo_name,
#         "readme": readme_text,
#     }
#     result = graph.invoke(input_data)
#     return {"repo": repo_name, "summary": result['final_summary']}

@app.get("/summary")
async def get_summary(
    repo_name: str = Query(..., description="仓库全名，如 owner/repo"),
    max_steps: int = Query(10, description="最大执行步骤数，默认 10"),
):
    """
    使用 ReAct 框架生成项目总结。
    
    ReAct 框架通过思考-行动-观察的循环来完成研究任务：
    1. Think（思考）：分析当前状态，决定下一步行动
    2. Act（行动）：执行动作（搜索、过滤、总结）
    3. Observe（观察）：观察结果，决定是否继续
    
    参数：
    - repo_name: GitHub 仓库全名，如 "owner/repo"
    - max_steps: 最大执行步骤数，防止无限循环，默认 10
    """
    readme_text = project_service.get_repository_readme(repo_name, None)
    if not readme_text:
        raise HTTPException(
            status_code=404, detail="缺少 README 内容，且无法通过仓库名获取。"
        )
    
    # 初始化 ReAct 状态
    input_data = {
        "project_name": repo_name,
        "readme": readme_text,
        "step_count": 0,
        "max_steps": max_steps,
        "should_continue": True,
    }
    
    # 执行 ReAct 工作流
    try:
        result = react_graph.invoke(input_data)
        
        # 检查是否成功生成总结
        if not result.get('final_summary'):
            raise HTTPException(
                status_code=500,
                detail=f"ReAct 框架未能生成总结。步骤数: {result.get('step_count', 0)}/{max_steps}"
            )
        
        return {
            "repo": repo_name,
            "summary": result['final_summary'],
            "steps": result.get('step_count', 0),
            "thoughts": result.get('thoughts', []),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ReAct 框架执行失败: {str(e)}"
        )

@app.get("/search")
async def search(
    user_input: str = Query(..., description="用户输入"),
):
    """搜索 GitHub 项目，流式返回结果"""
    
    async def generate():
        try:
            # 初始化状态
            initial_state = {"user_input": user_input}
            
            # 用于跟踪已发送的项目，避免重复发送
            sent_projects = set()
            
            # 使用 astream 来流式执行 graph
            async for event in search_graph.astream(initial_state):
                # 发送每个节点的更新
                for node_name, node_output in event.items():
                    if node_name == "generate_search_queries":
                        # 发送搜索查询
                        search_queries = node_output.get("search_queries", [])
                        if search_queries:
                            yield f"data: {json.dumps({'type': 'search_queries', 'data': search_queries}, ensure_ascii=False)}\n\n"
                    
                    elif node_name == "generate_validate_criteria":
                        # 发送验证标准
                        validate_criteria = node_output.get("validate_criteria", [])
                        if validate_criteria:
                            yield f"data: {json.dumps({'type': 'validate_criteria', 'data': validate_criteria}, ensure_ascii=False)}\n\n"
                    
                    elif node_name == "search_github":
                        # 发送搜索进度
                        github_results = node_output.get("github_results", [])
                        if github_results:
                            yield f"data: {json.dumps({'type': 'search_progress', 'data': {'total': len(github_results)}}, ensure_ascii=False)}\n\n"
                    
                    elif node_name == "validate_project":
                        # 流式发送验证后的项目（并行验证，每个项目验证完成后立即发送）
                        validated_projects = node_output.get("validated_projects", [])
                        # 每个 validate_project 节点只返回一个项目，取最后一个确保是最新验证的
                        if validated_projects:
                            project = validated_projects[-1]
                            full_name = project.get("full_name", "")
                            if full_name and full_name not in sent_projects:
                                sent_projects.add(full_name)
                                
                                # 转换为 Project 格式
                                language = project.get("language")
                                tags = project.get("topics", [])
                                if language and language not in tags:
                                    tags.append(language.lower())
                                
                                # 提取仓库名称（不包含owner）
                                repo_name = project.get("name", "") or (full_name.split("/")[-1] if "/" in full_name else full_name)
                                
                                project_data = {
                                    "id": full_name,
                                    "title": repo_name,
                                    "authors": project.get("owner", {}).get("login", "Unknown"),
                                    "description": project.get("description", "") or "",
                                    "tags": tags[:10],
                                    "stars": project.get("stargazers_count", 0),
                                    "forks": project.get("forks_count", 0),
                                    "language": language,
                                }
                                yield f"data: {json.dumps({'type': 'project', 'data': project_data}, ensure_ascii=False)}\n\n"
            
            # 发送完成信号
            yield f"data: {json.dumps({'type': 'complete', 'data': {'total': len(sent_projects)}}, ensure_ascii=False)}\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'data': str(e)}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )

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