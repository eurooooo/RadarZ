import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {"Authorization": f"token {token}"} if token else {}
    
    def get_new_repositories(self, days: int = 7, min_stars: int = 10, 
                            language: Optional[str] = None, limit: int = 50) -> List[Dict]:
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
            "per_page": min(limit, 100)
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取GitHub项目失败: {e}")
            return []
    
    def get_repository_details(self, repo: Dict) -> Dict:
        """获取项目详细信息"""
        return {
            "name": repo['full_name'],
            "description": repo.get('description', '') or '无描述',
            "stars": repo['stargazers_count'],
            "language": repo.get('language', 'Unknown'),
            "topics": repo.get('topics', []),
            "url": repo['html_url'],
            "created_at": repo['created_at'],
            "updated_at": repo['updated_at'],
            "size": repo.get('size', 0),
            "forks": repo.get('forks_count', 0),
        }

