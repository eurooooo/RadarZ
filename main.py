import os
import sys
from dotenv import load_dotenv
from src.github_client import GitHubClient
from src.ai_recommender import AIRecommender
from src.user_profile import UserProfileManager
from src.email_service import EmailService
from src.subscription_manager import SubscriptionManager

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

def print_repositories(repo_details: list, title: str = "GitHub项目列表"):
    """打印项目列表"""
    if not repo_details:
        print("❌ 未找到符合条件的项目")
        return
    
    print("=" * 80)
    print(f"📦 {title}：\n")
    
    for i, repo in enumerate(repo_details, 1):
        print(f"{i}. {repo['name']}")
        print(f"   ⭐ {repo['stars']} stars | 📝 {repo['language']} | 🍴 {repo['forks']} forks")
        print(f"   📅 创建时间: {repo['created_at']}")
        print(f"   📝 描述: {repo['description']}")
        
        if repo.get('topics'):
            topics_str = ', '.join(repo['topics'][:5])  # 最多显示5个主题
            print(f"   🏷️  主题: {topics_str}")
        
        if 'recommendation_reason' in repo:
            print(f"   💡 推荐理由: {repo['recommendation_reason']}")
        if 'highlights' in repo:
            print(f"   ✨ 项目亮点: {repo['highlights']}")
        
        print(f"   🔗 {repo['url']}")
        print()  # 空行分隔
    
    print("=" * 80)
    print(f"\n💡 提示: 您可以编辑 user_profile.json 来更新偏好设置")

def mode_trending(github: GitHubClient, since: str = "daily", limit: int = 25):
    """Trending模式：获取GitHub trending项目"""
    print(f"🔥 正在获取GitHub Trending项目（{since}）...\n")
    
    repos = github.get_trending_repositories(since=since, limit=limit)
    
    if not repos:
        print("❌ 未找到trending项目")
        return
    
    repo_details = [github.get_repository_details(repo) for repo in repos]
    print(f"✅ 找到 {len(repo_details)} 个trending项目\n")
    print_repositories(repo_details, "GitHub Trending项目")

def mode_new(github: GitHubClient, profile_manager: UserProfileManager, 
             days: int = 7, limit: int = 50):
    """New模式：获取按star数筛选的新项目"""
    print("🔍 正在获取GitHub新项目...\n")
    
    user_profile = profile_manager.to_dict()
    min_stars = user_profile.get('min_stars', 10)
    languages = user_profile.get('languages', [])
    
    # 如果用户设置了语言偏好，可以按语言筛选
    language_filter = languages[0] if languages else None
    
    repos = github.get_new_repositories(
        days=days, 
        min_stars=min_stars, 
        language=language_filter,
        limit=limit
    )
    
    if not repos:
        print("❌ 未找到符合条件的项目")
        return
    
    repo_details = [github.get_repository_details(repo) for repo in repos]
    print(f"✅ 找到 {len(repo_details)} 个新项目（最近{days}天，至少{min_stars} stars）\n")
    print_repositories(repo_details, "GitHub新项目")

def mode_ai(github: GitHubClient, profile_manager: UserProfileManager,
            source: str = "new", days: int = 7, limit: int = 50, top_n: int = 10):
    """AI模式：基于用户偏好的AI推荐"""
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
    
    # 根据source获取项目
    if source == "trending":
        print("🔥 正在获取GitHub Trending项目...")
        repos = github.get_trending_repositories(since="daily", limit=limit)
    else:  # source == "new"
        print("🔍 正在获取GitHub新项目...")
        user_profile = profile_manager.to_dict()
        min_stars = user_profile.get('min_stars', 10)
        languages = user_profile.get('languages', [])
        language_filter = languages[0] if languages else None
        
        repos = github.get_new_repositories(
            days=days, 
            min_stars=min_stars, 
            language=language_filter,
            limit=limit
        )
    
    if not repos:
        print("❌ 未找到符合条件的项目")
        return
    
    repo_details = [github.get_repository_details(repo) for repo in repos]
    print(f"✅ 找到 {len(repo_details)} 个项目\n")
    
    # AI推荐
    print("🤖 AI正在分析并生成个性化推荐...\n")
    user_profile = profile_manager.to_dict()
    recommendations = recommender.generate_recommendations(
        repo_details,
        user_profile,
        top_n=top_n
    )
    
    if not recommendations:
        print("❌ 未能生成推荐，显示热门项目：\n")
        recommendations = sorted(repo_details, key=lambda x: x['stars'], reverse=True)[:top_n]
    
    print_repositories(recommendations, "为您推荐的GitHub项目")

def mode_subscribe():
    """订阅模式：用户输入邮箱并验证"""
    print("=" * 60)
    print("📧 RadarZ 邮件订阅")
    print("=" * 60)
    
    # 检查邮件服务配置
    try:
        email_service = EmailService()
    except ValueError as e:
        print(f"❌ {e}")
        print("\n请配置 Resend API：")
        print("  1. 访问 https://resend.com 注册账号（免费）")
        print("  2. 进入 Dashboard → API Keys → Create API Key")
        print("  3. 在 .env 文件中设置：")
        print("     RESEND_API_KEY=re_xxxxx")
        print("     FROM_EMAIL=onboarding@resend.dev (测试) 或已验证的域名邮箱")
        return
    
    subscription_manager = SubscriptionManager()
    
    # 输入邮箱
    print("\n请输入您的邮箱地址：")
    email = input("> ").strip().lower()
    
    if not email or '@' not in email:
        print("❌ 邮箱格式不正确")
        return
    
    # 检查是否已订阅
    if subscription_manager.is_subscribed(email):
        print(f"\n✅ 邮箱 {email} 已经订阅！")
        return
    
    # 生成验证码
    print(f"\n📧 正在向 {email} 发送验证码...")
    code = subscription_manager.start_verification(email)
    
    if not email_service.send_verification_code(email, code):
        print("❌ 发送验证码失败，请检查邮件服务配置")
        return
    
    print("✅ 验证码已发送！请查看您的邮箱。")
    print("💡 验证码有效期为 10 分钟")
    
    # 输入验证码
    print("\n请输入验证码：")
    user_code = input("> ").strip()
    
    if subscription_manager.verify_code(email, user_code):
        # 发送欢迎邮件
        print(f"\n✅ 验证成功！正在发送欢迎邮件...")
        if email_service.send_welcome_email(email):
            print(f"🎉 欢迎邮件已发送到 {email}！")
            print("\n您将每天收到 GitHub Trending 项目的精选推荐。")
        else:
            print("⚠️ 订阅成功，但发送欢迎邮件失败")
    else:
        print("❌ 验证码错误或已过期，请重新订阅")

def mode_unsubscribe():
    """退订模式"""
    print("=" * 60)
    print("📧 RadarZ 邮件退订")
    print("=" * 60)
    
    subscription_manager = SubscriptionManager()
    
    print("\n请输入要退订的邮箱地址：")
    email = input("> ").strip().lower()
    
    if not email or '@' not in email:
        print("❌ 邮箱格式不正确")
        return
    
    if not subscription_manager.is_subscribed(email):
        print(f"\n⚠️ 邮箱 {email} 未订阅")
        return
    
    # 确认退订
    print(f"\n⚠️ 确认要退订 {email} 吗？(y/n)")
    confirm = input("> ").strip().lower()
    
    if confirm == 'y' or confirm == 'yes':
        if subscription_manager.unsubscribe(email):
            print(f"\n✅ 已成功退订 {email}")
            print("您将不再收到每日推送邮件。")
        else:
            print("❌ 退订失败")
    else:
        print("已取消退订")

def show_usage():
    """显示使用说明"""
    print("=" * 60)
    print("🚀 RadarZ - GitHub项目推荐系统")
    print("=" * 60)
    print("\n使用方法:")
    print("  python main.py [模式] [选项]")
    print("\n可用模式:")
    print("  subscribe        订阅邮件推送（需要邮箱验证）")
    print("  unsubscribe     退订邮件推送")
    print("  trending        获取GitHub trending项目")
    print("  new             获取按star数筛选的新项目")
    print("  ai              基于用户偏好的AI推荐（默认基于new模式）")
    print("\n选项:")
    print("  --source SOURCE  AI模式下指定数据源: trending 或 new (默认: new)")
    print("  --days DAYS     新项目模式下的天数 (默认: 7)")
    print("  --limit LIMIT    获取项目数量限制 (默认: 50)")
    print("  --top-n N        AI推荐返回数量 (默认: 10)")
    print("  --since SINCE    Trending模式时间范围: daily/weekly/monthly (默认: daily)")
    print("\n示例:")
    print("  python main.py subscribe")
    print("  python main.py unsubscribe")
    print("  python main.py trending")
    print("  python main.py new --days 14")
    print("  python main.py ai --source trending --top-n 15")
    print("=" * 60 + "\n")

def main():
    """主函数"""
    # 解析命令行参数
    args = sys.argv[1:]
    
    if not args or args[0] in ['-h', '--help', 'help']:
        show_usage()
        return
    
    mode = args[0]
    
    # 解析选项
    source = "new"
    days = 7
    limit = 50
    top_n = 10
    since = "daily"
    
    i = 1
    while i < len(args):
        if args[i] == '--source' and i + 1 < len(args):
            source = args[i + 1]
            i += 2
        elif args[i] == '--days' and i + 1 < len(args):
            days = int(args[i + 1])
            i += 2
        elif args[i] == '--limit' and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        elif args[i] == '--top-n' and i + 1 < len(args):
            top_n = int(args[i + 1])
            i += 2
        elif args[i] == '--since' and i + 1 < len(args):
            since = args[i + 1]
            i += 2
        else:
            i += 1
    
    # 根据模式执行
    if mode == "subscribe":
        mode_subscribe()
        return
    elif mode == "unsubscribe":
        mode_unsubscribe()
        return
    
    # 初始化组件（其他模式需要）
    print("🚀 正在初始化 RadarZ...\n")
    
    github = GitHubClient(token=os.getenv("GITHUB_TOKEN"))
    profile_manager = UserProfileManager()
    
    # 首次运行设置偏好
    setup_user_profile(profile_manager)
    
    if mode == "trending":
        mode_trending(github, since=since, limit=limit)
    elif mode == "new":
        mode_new(github, profile_manager, days=days, limit=limit)
    elif mode == "ai":
        mode_ai(github, profile_manager, source=source, days=days, limit=limit, top_n=top_n)
    else:
        print(f"❌ 未知模式: {mode}")
        show_usage()

if __name__ == "__main__":
    main()
