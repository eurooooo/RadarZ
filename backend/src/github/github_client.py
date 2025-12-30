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
        """获取新项目
        
        Args:
            days: 查询最近几天的项目
            min_stars: 最小 star 数
            language: 编程语言过滤（可选）
            limit: 返回项目数量限制（最多1000，受GitHub API限制）
        
        Returns:
            项目列表
        """
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        query = f"created:>{start_date} stars:>={min_stars}"
        if language:
            query += f" language:{language}"

        url = "https://api.github.com/search/repositories"
        
        # GitHub API 限制：per_page 最大 100，总结果最多 1000
        max_per_page = 100
        max_total_results = 1000
        actual_limit = min(limit, max_total_results)
        
        all_items = []
        page = 1
        per_page = min(max_per_page, actual_limit)
        
        try:
            while len(all_items) < actual_limit:
                # 计算当前页需要获取的数量
                remaining = actual_limit - len(all_items)
                current_per_page = min(per_page, remaining)
                
                params = {
                    "q": query,
                    "per_page": current_per_page,
                    "page": page,
                }
                
                response = requests.get(url, params=params, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                items = data.get("items", [])
                
                if not items:
                    # 没有更多结果了
                    break
                
                all_items.extend(items)
                
                # 如果当前页返回的数量少于请求的数量，说明已经是最后一页
                if len(items) < current_per_page:
                    break
                
                page += 1
                
                # 防止无限循环（最多10页，因为最多1000条结果）
                if page > 10:
                    break
            
            return all_items[:actual_limit]
            
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
            "description": repo.get("description", "") or "",
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

    def search_repositories(
        self,
        query: str,
        limit: int = 30,
        sort: str = "stars",
        order: str = "desc"
    ) -> List[Dict]:
        """
        搜索 GitHub 仓库
        
        Args:
            query: 搜索查询字符串（支持 GitHub 搜索语法）
            limit: 返回结果数量限制（最多 1000，受 GitHub API 限制）
            sort: 排序方式，可选 "stars", "forks", "help-wanted-issues", "updated"
            order: 排序顺序，可选 "desc" 或 "asc"
        
        Returns:
            仓库列表
        """
        url = "https://api.github.com/search/repositories"
        
        # GitHub API 限制：per_page 最大 100，总结果最多 1000
        max_per_page = 100
        max_total_results = 1000
        actual_limit = min(limit, max_total_results)
        
        all_items = []
        page = 1
        per_page = min(max_per_page, actual_limit)
        
        try:
            while len(all_items) < actual_limit:
                remaining = actual_limit - len(all_items)
                current_per_page = min(per_page, remaining)
                
                params = {
                    "q": query,
                    "sort": sort,
                    "order": order,
                    "per_page": current_per_page,
                    "page": page,
                }
                
                response = requests.get(url, params=params, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                items = data.get("items", [])
                
                if not items:
                    break
                
                all_items.extend(items)
                
                if len(items) < current_per_page:
                    break
                
                page += 1
                
                # 防止无限循环
                if page > 10:
                    break
            
            return all_items[:actual_limit]
            
        except requests.exceptions.RequestException as e:
            print(f"❌ GitHub 搜索失败: {e}")
            return []

    def get_repo_structure(
        self, repo_full_name: str, branch: str = "main"
    ) -> Optional[List[Dict]]:
        """
        使用 GitHub Git Trees API 递归获取整个仓库的文件列表
        
        Args:
            repo_full_name: 仓库全名，格式 "owner/repo"
            branch: 分支名，默认为 "main"
        
        Returns:
            文件列表，每个文件包含 path, type, size 等信息；如果失败则返回 None
        """
        if not repo_full_name:
            return None
        
        # 首先获取分支的 SHA
        try:
            branch_url = f"https://api.github.com/repos/{repo_full_name}/branches/{branch}"
            branch_res = requests.get(branch_url, headers=self.headers, timeout=10)
            if branch_res.status_code == 404:
                # 尝试其他常见分支名
                for alt_branch in ["master", "develop"]:
                    branch_res = requests.get(
                        f"https://api.github.com/repos/{repo_full_name}/branches/{alt_branch}",
                        headers=self.headers,
                        timeout=10
                    )
                    if branch_res.status_code == 200:
                        branch = alt_branch
                        break
                else:
                    return None
            
            branch_res.raise_for_status()
            branch_data = branch_res.json()
            tree_sha = branch_data["commit"]["sha"]
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取分支信息失败 {repo_full_name}: {e}")
            return None
        
        # 获取递归的树结构
        try:
            tree_url = f"https://api.github.com/repos/{repo_full_name}/git/trees/{tree_sha}"
            params = {"recursive": "1"}
            tree_res = requests.get(tree_url, headers=self.headers, params=params, timeout=30)
            tree_res.raise_for_status()
            tree_data = tree_res.json()
            tree_items = tree_data.get("tree", [])
            
            # 优化返回数据，只保留必要字段（path 和 type），减少 token 占用
            optimized_tree = []
            for item in tree_items:
                optimized_tree.append({
                    "path": item.get("path", ""),
                    "type": item.get("type", ""),
                    "size": item.get("size", 0)  # 保留 size 可能有用
                })
            
            return optimized_tree
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取仓库结构失败 {repo_full_name}: {e}")
            return None

    def get_file_content(
        self, repo_full_name: str, file_path: str, ref: Optional[str] = None
    ) -> Optional[str]:
        """
        使用 GitHub Contents API 读取指定文件的内容
        
        Args:
            repo_full_name: 仓库全名，格式 "owner/repo"
            file_path: 文件路径（相对于仓库根目录）
            ref: 分支名或 commit sha（可选，默认为默认分支）
        
        Returns:
            文件内容（纯文本）；如果未找到或失败则返回 None
        """
        if not repo_full_name or not file_path:
            return None
        
        api_url = f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}"
        params = {"ref": ref} if ref else None
        
        try:
            res = requests.get(api_url, headers=self.headers, params=params, timeout=10)
            if res.status_code == 404:
                return None
            res.raise_for_status()
            data = res.json()
            
            # 文件内容默认 base64 编码
            content = data.get("content")
            encoding = data.get("encoding")
            if not content:
                return None
            
            if encoding == "base64":
                import base64
                return base64.b64decode(content).decode("utf-8", errors="ignore")
            
            return content
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取文件内容失败 {repo_full_name}/{file_path}: {e}")
            return None

    def search_code_in_repo(
        self, 
        repo_full_name: str, 
        keywords: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        在指定仓库内搜索代码
        
        Args:
            repo_full_name: 仓库全名，格式 "owner/repo"
            keywords: 搜索关键词（支持 GitHub 代码搜索语法）
            limit: 返回结果数量限制（最多 100，受 GitHub API 限制）
        
        Returns:
            搜索结果列表，每个结果包含文件路径、代码片段等信息
        """
        if not repo_full_name or not keywords:
            return []
        
        url = "https://api.github.com/search/code"
        
        # GitHub Code Search API 限制：per_page 最大 100，总结果最多 1000
        max_per_page = 100
        max_total_results = 1000
        actual_limit = min(limit, max_total_results, max_per_page)
        
        # 构建搜索查询：keywords + repo:owner/repo
        query = f"{keywords} repo:{repo_full_name}"
        
        try:
            params = {
                "q": query,
                "per_page": actual_limit,
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])
            
            # 格式化结果，提取关键信息
            # 注意：GitHub Code Search API 返回的 items 中，repository 可能是简化的对象
            results = []
            for item in items[:actual_limit]:
                # 处理 repository 字段（可能是对象或字符串）
                repo_info = item.get("repository", {})
                if isinstance(repo_info, dict):
                    repo_full = repo_info.get("full_name", repo_full_name)
                else:
                    repo_full = repo_full_name
                
                results.append({
                    "path": item.get("path", ""),
                    "name": item.get("name", ""),
                    "url": item.get("html_url", ""),
                    "repository": repo_full,
                    "score": item.get("score", 0),
                })
            
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 代码搜索失败 {repo_full_name}: {e}")
            return []

