import requests
from datetime import datetime, timedelta

# 获取最近7天创建的 Python 项目
start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

url = "https://api.github.com/search/repositories"
params = {
    "q": f"created:>{start_date} stars:>100",
    "sort": "stars",
    "order": "desc",
    "per_page": 10
}

response = requests.get(url, params=params)
data = response.json()

print(f"\n找到 {data['total_count']} 个项目，显示前 10 个:\n")

for i, repo in enumerate(data['items'], 1):
    print(f"{i}. {repo['full_name']}")
    print(f"   ⭐ {repo['stargazers_count']} stars")
    print(f"   📝 {repo['description']}")
    print(f"   🔗 {repo['html_url']}\n")