"""
每日推送脚本 - 向所有订阅用户发送GitHub Trending项目推荐
可以通过定时任务（如cron）每天运行此脚本
"""
import os
from dotenv import load_dotenv
from src.github_client import GitHubClient
from src.email_service import EmailService
from src.subscription_manager import SubscriptionManager

load_dotenv()

def main():
    """每日推送主函数"""
    print("=" * 60)
    print("📧 RadarZ 每日推送")
    print("=" * 60)
    
    # 初始化组件
    try:
        email_service = EmailService()
    except ValueError as e:
        print(f"❌ 邮件服务配置错误: {e}")
        return
    
    github = GitHubClient(token=os.getenv("GITHUB_TOKEN"))
    subscription_manager = SubscriptionManager()
    
    # 获取所有订阅者
    subscribers = subscription_manager.get_all_subscribers()
    
    if not subscribers:
        print("ℹ️ 当前没有订阅用户")
        return
    
    print(f"\n📋 找到 {len(subscribers)} 个订阅用户")
    
    # 获取trending项目（取前5个）
    print("\n🔥 正在获取GitHub Trending项目...")
    repos = github.get_trending_repositories(since="daily", limit=5)
    
    if not repos:
        print("❌ 未找到trending项目")
        return
    
    repo_details = [github.get_repository_details(repo) for repo in repos]
    print(f"✅ 获取到 {len(repo_details)} 个trending项目\n")
    
    # 向每个订阅者发送邮件
    success_count = 0
    fail_count = 0
    
    for email in subscribers:
        print(f"📧 正在向 {email} 发送推送...")
        if email_service.send_daily_push(email, repo_details):
            print(f"  ✅ 发送成功")
            success_count += 1
        else:
            print(f"  ❌ 发送失败")
            fail_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 推送完成：成功 {success_count}，失败 {fail_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()

