import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup


class GitHubClient:
    """GitHub API 客户端，用于获取 trending 项目和其他 GitHub 数据"""

    def __init__(self, token: Optional[str] = None):
        """
        初始化 GitHub 客户端
        
        Args:
            token: GitHub Personal Access Token (可选，用于提高 API 限制)
        """
        # https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        
        # 如果提供了 token，使用 Bearer 认证
        # https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def get_new_repositories(
        self,
        days: int = 7,
        min_stars: int = 10,
        language: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict]:
        """获取新项目"""
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        query = f"created:>{start_date} stars:>={min_stars}"
        if language:
            query += f" language:{language}"

        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": min(limit, 100),
        }

        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取GitHub项目失败: {e}")
            return []

    def get_trending_repositories(
        self, since: str = "daily", limit: int = 25
    ) -> List[Dict]:
        """从GitHub trending页面获取trending项目

        Args:
            since: 时间范围，可选 "daily", "weekly", "monthly"
            limit: 返回项目数量限制

        Returns:
            项目详细信息列表
        """
        try:
            url = f"https://github.com/trending?since={since}"
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            html_text = res.text
            soup = BeautifulSoup(html_text, "html.parser")
            repo_elements = soup.select("h2.h3.lh-condensed")
            repo_names = []
            for element in repo_elements[:limit]:
                a_tag = element.find("a")
                if a_tag:
                    href = a_tag.get("href", "").strip()
                    repo_name = (
                        href[1:] if href.startswith("/") else href
                    )  # 去掉开头的 "/"
                    repo_names.append(repo_name)

            # 通过API获取详细信息
            repos = []
            for repo_name in repo_names:
                try:
                    api_url = f"https://api.github.com/repos/{repo_name}"
                    response = requests.get(
                        api_url, headers=self.headers, timeout=5
                    )
                    if response.status_code == 200:
                        repos.append(response.json())
                except Exception as e:
                    print(f"⚠️ 获取 {repo_name} 详情失败: {e}")
                    continue

            return repos
        except Exception as e:
            print(f"❌ 获取trending项目失败: {e}")
            return []

    def get_repository_details(self, repo: Dict) -> Dict:
        """获取项目详细信息"""
        return {
            "name": repo["full_name"],
            "description": repo.get("description", "") or "无描述",
            "stars": repo["stargazers_count"],
            "language": repo.get("language", "Unknown"),
            "topics": repo.get("topics", []),
            "url": repo["html_url"],
            "created_at": repo["created_at"],
            "updated_at": repo["updated_at"],
            "size": repo.get("size", 0),
            "forks": repo.get("forks_count", 0),
        }

    def get_repository_readme(
        self, repo_name: str, ref: Optional[str] = None
    ) -> Optional[str]:
        """
        获取指定仓库的 README 文本内容

        Args:
            repo_name: 仓库全名，格式 "owner/repo"
            ref: 分支名或 commit sha（可选）

        Returns:
            README 纯文本内容；如果未找到则返回 None
        """
        if not repo_name:
            return None

        api_url = f"https://api.github.com/repos/{repo_name}/readme"
        params = {"ref": ref} if ref else None

        try:
            res = requests.get(api_url, headers=self.headers, params=params, timeout=10)
            if res.status_code == 404:
                return None
            res.raise_for_status()
            data = res.json()

            # README content 默认 base64 编码
            content = data.get("content")
            encoding = data.get("encoding")
            if not content:
                return None

            if encoding == "base64":
                import base64

                return base64.b64decode(content).decode("utf-8", errors="ignore")

            return content
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取 README 失败: {e}")
            return None

