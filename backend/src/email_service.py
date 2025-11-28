import os
from typing import List, Dict
from datetime import datetime
import resend

class EmailService:
    """邮件服务类，使用Resend API发送邮件"""
    
    def __init__(self):
        self.resend_api_key = os.getenv("RESEND_API_KEY")
        if not self.resend_api_key:
            raise ValueError("需要设置 RESEND_API_KEY 环境变量")
        
        # 设置 API key（官网方式）
        resend.api_key = self.resend_api_key
        
        self.from_email = os.getenv("FROM_EMAIL")
        if not self.from_email:
            raise ValueError("需要设置 FROM_EMAIL 环境变量")
    
    def send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """发送邮件"""
        try:
            # 使用官网的 API 格式：resend.Emails.send (注意是大写 Emails)
            r = resend.Emails.send({
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "html": html_content,
            })
            return r is not None
        except Exception as e:
            print(f"❌ 发送邮件失败: {e}")
            return False
    
    def send_verification_code(self, to_email: str, code: str) -> bool:
        """发送验证码邮件"""
        subject = "RadarZ 邮箱验证码"
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">RadarZ 邮箱验证</h2>
                <p>您好！</p>
                <p>感谢您订阅 RadarZ！您的验证码是：</p>
                <div style="background-color: #f4f4f4; padding: 20px; text-align: center; margin: 20px 0; border-radius: 5px;">
                    <h1 style="color: #3498db; margin: 0; font-size: 32px; letter-spacing: 5px;">{code}</h1>
                </div>
                <p>验证码有效期为 10 分钟。</p>
                <p>如果您没有请求此验证码，请忽略此邮件。</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="color: #999; font-size: 12px;">RadarZ - GitHub项目推荐系统</p>
            </div>
        </body>
        </html>
        """
        return self.send_email(to_email, subject, html_content)
    
    def send_welcome_email(self, to_email: str) -> bool:
        """发送欢迎邮件"""
        subject = "🎉 欢迎订阅 RadarZ！"
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">🎉 欢迎订阅 RadarZ！</h2>
                <p>您好！</p>
                <p>感谢您订阅 <strong>RadarZ</strong>！从今天开始，您将每天收到 GitHub Trending 项目的精选推荐。</p>
                <p>我们会在每天为您推送 <strong>5 个精选项目</strong>，帮助您发现有趣的开源项目。</p>
                <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>📧 订阅邮箱：</strong>{to_email}</p>
                    <p style="margin: 10px 0 0 0;"><strong>📅 推送时间：</strong>每天</p>
                </div>
                <p>如果您想退订，请回复此邮件或使用退订命令。</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="color: #999; font-size: 12px;">RadarZ - GitHub项目推荐系统</p>
            </div>
        </body>
        </html>
        """
        return self.send_email(to_email, subject, html_content)
    
    def send_daily_push(self, to_email: str, repos: List[Dict]) -> bool:
        """发送每日推送邮件"""
        if not repos:
            return False
        
        subject = f"📦 RadarZ 每日推荐 - {datetime.now().strftime('%Y年%m月%d日')}"
        
        # 生成项目列表HTML
        repos_html = ""
        for i, repo in enumerate(repos, 1):
            language = repo.get('language', 'Unknown')
            stars = repo.get('stars', 0)
            forks = repo.get('forks', 0)
            description = repo.get('description', '无描述')
            url = repo.get('url', '#')
            
            repos_html += f"""
            <div style="background-color: #f9f9f9; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #3498db;">
                <h3 style="margin: 0 0 10px 0; color: #2c3e50;">
                    <a href="{url}" style="color: #3498db; text-decoration: none;">{i}. {repo['name']}</a>
                </h3>
                <p style="margin: 5px 0; color: #666;">{description}</p>
                <div style="margin-top: 10px; color: #999; font-size: 14px;">
                    <span>⭐ {stars} stars</span> | 
                    <span>📝 {language}</span> | 
                    <span>🍴 {forks} forks</span>
                </div>
                <a href="{url}" style="display: inline-block; margin-top: 10px; color: #3498db; text-decoration: none;">查看项目 →</a>
            </div>
            """
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">📦 GitHub Trending 每日推荐</h2>
                <p>您好！</p>
                <p>这是您今天的 GitHub Trending 项目推荐：</p>
                {repos_html}
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="color: #999; font-size: 12px;">
                    如果您想退订，请回复此邮件或使用退订命令。<br>
                    RadarZ - GitHub项目推荐系统
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)
