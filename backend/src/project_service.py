from typing import List, Optional, Dict
from datetime import datetime
from .github_client import GitHubClient
from .models import Project


class ProjectService:
    """项目服务类，负责从 GitHub 获取并转换项目数据"""

    def __init__(self, github_token: Optional[str] = None):
        """
        初始化项目服务
        
        Args:
            github_token: GitHub Personal Access Token (可选)
        """
        self.github_client = GitHubClient(token=github_token)

    def get_trending_projects(self, limit: int = 25) -> List[Project]:
        """
        获取当日的 GitHub trending 项目
        
        Args:
            limit: 返回项目数量限制
            
        Returns:
            Project 对象列表
        """
        # 从 GitHub trending 获取数据
        repos = self.github_client.get_trending_repositories(
            since="daily", limit=limit
        )

        projects = []
        for repo in repos:
            # 转换 GitHub API 数据为 Project 模型
            project = self._convert_repo_to_project(repo)
            projects.append(project)

        return projects

    def get_repository_readme(
        self, repo_name: str, ref: Optional[str] = None
    ) -> Optional[str]:
        """
        获取指定仓库的 README 内容

        Args:
            repo_name: 仓库全名 "owner/repo"
            ref: 分支名或 commit sha（可选）

        Returns:
            README 文本，如果不存在返回 None
        """
        return self.github_client.get_repository_readme(repo_name, ref)

    def _convert_repo_to_project(self, repo: Dict) -> Project:
        """
        将 GitHub 仓库数据转换为 Project 模型
        
        Args:
            repo: GitHub API 返回的仓库数据
            
        Returns:
            Project 对象
        """
        # 获取作者（通常是仓库所有者的用户名）
        authors = repo.get("owner", {}).get("login", "Unknown")
        full_name = repo.get("full_name", "")

        # 格式化日期（使用 updated_at，因为这是 trending 的依据）
        updated_at = repo.get("updated_at", "")
        date_str = self._format_date(updated_at)

        # 获取描述
        description = repo.get("description", "") or "无描述"

        # 获取标签（topics + language）
        tags = repo.get("topics", [])
        language = repo.get("language")
        if language and language not in tags:
            tags.append(language.lower())

        # 生成 GitHub Open Graph 图片 URL
        # 使用 GitHub 的 Open Graph 图片服务
        image_url = self._get_repository_image_url(full_name) if full_name else None

        return Project(
            # 使用仓库全名作为稳定 ID，避免列表重排导致 ID 变化
            id=full_name or repo.get("html_url", ""),
            title=full_name,
            authors=authors,
            date=date_str,
            description=description,
            tags=tags[:10],  # 限制标签数量
            stars=repo.get("stargazers_count", 0),
            forks=repo.get("forks_count", 0),
            image_url=image_url,
        )

    def _get_repository_image_url(self, full_name: str) -> Optional[str]:
        """
        生成 GitHub 仓库的 Open Graph 图片 URL
        
        Args:
            full_name: 仓库的完整名称，格式为 "owner/repo"
            
        Returns:
            Open Graph 图片 URL 或 None
        """
        if not full_name:
            return None
        
        # 使用 GitHub 的 Open Graph 图片服务
        # GitHub 会自动为每个仓库生成 Open Graph 图片
        # URL 格式: https://opengraph.githubassets.com/{hash}/{owner}/{repo}
        # hash 可以是任意值（如 1），GitHub 会自动处理
        try:
            owner, repo = full_name.split("/", 1) if "/" in full_name else (full_name, "")
            if not repo:
                return None
            
            # 使用 GitHub 的 Open Graph 图片服务
            # 这个服务会自动生成仓库的预览图（包含 README 内容）
            return f"https://opengraph.githubassets.com/1/{owner}/{repo}"
        except Exception:
            return None
    
    def _format_date(self, date_str: str) -> str:
        """
        格式化日期字符串为相对时间
        
        Args:
            date_str: ISO 格式的日期字符串
            
        Returns:
            格式化的相对时间字符串
        """
        if not date_str:
            return "未知时间"

        try:
            # 解析 ISO 格式日期
            date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            now = datetime.now(date_obj.tzinfo) if date_obj.tzinfo else datetime.now()
            delta = now - date_obj

            # 计算相对时间
            if delta.days > 0:
                return f"{delta.days} 天前"
            elif delta.seconds >= 3600:
                hours = delta.seconds // 3600
                return f"{hours} 小时前"
            elif delta.seconds >= 60:
                minutes = delta.seconds // 60
                return f"{minutes} 分钟前"
            else:
                return "刚刚"
        except Exception:
            return "未知时间"

