import json
import os
import random
import string
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

@dataclass
class Subscription:
    """订阅信息"""
    email: str
    subscribed: bool = True
    subscribed_at: str = None
    verification_code: str = None
    verification_expires_at: str = None
    
    def __post_init__(self):
        if self.subscribed_at is None:
            self.subscribed_at = datetime.now().isoformat()

class SubscriptionManager:
    """订阅管理器，管理用户邮箱和订阅状态"""
    
    def __init__(self, data_file: str = "subscriptions.json"):
        self.data_file = data_file
        self.subscriptions = self.load_subscriptions()
    
    def load_subscriptions(self) -> Dict[str, Subscription]:
        """加载订阅数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        email: Subscription(**sub_data)
                        for email, sub_data in data.items()
                    }
            except Exception as e:
                print(f"⚠️ 加载订阅数据失败: {e}，使用空数据")
        return {}
    
    def save_subscriptions(self):
        """保存订阅数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                data = {
                    email: asdict(sub)
                    for email, sub in self.subscriptions.items()
                }
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 保存订阅数据失败: {e}")
    
    def generate_verification_code(self) -> str:
        """生成6位数字验证码"""
        return ''.join(random.choices(string.digits, k=6))
    
    def start_verification(self, email: str) -> str:
        """开始验证流程，生成并返回验证码"""
        code = self.generate_verification_code()
        expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()
        
        if email not in self.subscriptions:
            self.subscriptions[email] = Subscription(
                email=email,
                subscribed=False
            )
        
        self.subscriptions[email].verification_code = code
        self.subscriptions[email].verification_expires_at = expires_at
        self.save_subscriptions()
        
        return code
    
    def verify_code(self, email: str, code: str) -> bool:
        """验证验证码"""
        if email not in self.subscriptions:
            return False
        
        sub = self.subscriptions[email]
        
        # 检查验证码是否存在
        if not sub.verification_code:
            return False
        
        # 检查验证码是否过期
        if sub.verification_expires_at:
            expires_at = datetime.fromisoformat(sub.verification_expires_at)
            if datetime.now() > expires_at:
                return False
        
        # 检查验证码是否匹配
        if sub.verification_code != code:
            return False
        
        # 验证成功，清除验证码并激活订阅
        sub.verification_code = None
        sub.verification_expires_at = None
        sub.subscribed = True
        sub.subscribed_at = datetime.now().isoformat()
        self.save_subscriptions()
        
        return True
    
    def subscribe(self, email: str) -> bool:
        """订阅（已验证后调用）"""
        if email not in self.subscriptions:
            self.subscriptions[email] = Subscription(
                email=email,
                subscribed=True
            )
        else:
            self.subscriptions[email].subscribed = True
            self.subscriptions[email].subscribed_at = datetime.now().isoformat()
        
        self.save_subscriptions()
        return True
    
    def unsubscribe(self, email: str) -> bool:
        """退订"""
        if email not in self.subscriptions:
            return False
        
        self.subscriptions[email].subscribed = False
        self.save_subscriptions()
        return True
    
    def is_subscribed(self, email: str) -> bool:
        """检查是否已订阅"""
        if email not in self.subscriptions:
            return False
        return self.subscriptions[email].subscribed
    
    def get_all_subscribers(self) -> List[str]:
        """获取所有订阅者邮箱"""
        return [
            email for email, sub in self.subscriptions.items()
            if sub.subscribed
        ]
    
    def get_subscription(self, email: str) -> Optional[Subscription]:
        """获取订阅信息"""
        return self.subscriptions.get(email)

