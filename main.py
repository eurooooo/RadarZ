import os
from dotenv import load_dotenv
from src.github_client import GitHubClient
from src.ai_recommender import AIRecommender
from src.user_profile import UserProfileManager

load_dotenv()

def setup_user_profile(profile_manager: UserProfileManager):
    """首次运行时设置用户偏好"""
    if not os.path.exists("user_profile.json"):
        print("=" * 60)
        print("🎯 欢迎使用 RadarZ！首次使用需要设置您的偏好")
        print("=" * 60)
        
        print("\n请输入您感兴趣的领域（用逗号分隔，直接回车跳过）：")
        print("例如: machine-learning, web-development, data-science")
        interests_input = input("> ").strip()
        if interests_input:
            interests = [i.strip() for i in interests_input.split(',')]
            profile_manager.update_interests(interests)
        
        print("\n请输入您偏好的编程语言（用逗号分隔，直接回车跳过）：")
        print("例如: Python, JavaScript, TypeScript")
        languages_input = input("> ").strip()
        if languages_input:
            languages = [l.strip() for l in languages_input.split(',')]
            profile_manager.update_languages(languages)
        
        print("\n✅ 偏好设置已保存！")
        print("=" * 60 + "\n")

def main():
    # 初始化组件
    print("🚀 正在初始化 RadarZ...\n")
    
    github = GitHubClient(token=os.getenv("GITHUB_TOKEN"))
    profile_manager = UserProfileManager()
    
    # 首次运行设置偏好
    setup_user_profile(profile_manager)
    
    # 检查AI API密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 错误: 未设置 OPENAI_API_KEY 环境变量")
        print("请在 .env 文件中设置，或运行: export OPENAI_API_KEY=your_key")
        return
    
    try:
        recommender = AIRecommender(api_key=os.getenv("OPENAI_API_KEY"))
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    # 获取用户偏好
    user_profile = profile_manager.to_dict()
    
    # 获取新项目
    print("🔍 正在获取GitHub新项目...")
    days = 7
    min_stars = user_profile.get('min_stars', 10)
    
    repos = github.get_new_repositories(days=days, min_stars=min_stars, limit=50)
    
    if not repos:
        print("❌ 未找到符合条件的项目")
        return
    
    repo_details = [github.get_repository_details(repo) for repo in repos]
    
    print(f"✅ 找到 {len(repo_details)} 个新项目（最近{days}天，至少{min_stars} stars）\n")
    
    # AI推荐
    print("🤖 AI正在分析并生成个性化推荐...\n")
    recommendations = recommender.generate_recommendations(
        repo_details,
        user_profile,
        top_n=10
    )
    
    if not recommendations:
        print("❌ 未能生成推荐，显示热门项目：\n")
        recommendations = sorted(repo_details, key=lambda x: x['stars'], reverse=True)[:10]
    
    # 显示推荐结果
    print("=" * 60)
    print("🎯 为您推荐的GitHub项目：\n")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['name']}")
        print(f"   ⭐ {rec['stars']} stars | 📝 {rec['language']}")
        print(f"   {rec['description']}")
        
        if 'recommendation_reason' in rec:
            print(f"   💡 推荐理由: {rec['recommendation_reason']}")
        if 'highlights' in rec:
            print(f"   ✨ 项目亮点: {rec['highlights']}")
        
        print(f"   🔗 {rec['url']}\n")
    
    print("=" * 60)
    print(f"\n💡 提示: 您可以编辑 user_profile.json 来更新偏好设置")

if __name__ == "__main__":
    main()
