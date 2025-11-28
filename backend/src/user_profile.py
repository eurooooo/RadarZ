from typing import List, Optional
from dataclasses import dataclass, asdict
import json
import os

@dataclass
class UserProfile:
    """用户偏好配置"""
    interests: List[str] = None  # 兴趣领域，如 ["machine-learning", "web-development"]
    languages: List[str] = None  # 编程语言偏好
    min_stars: int = 10  # 最小stars数
    exclude_keywords: List[str] = None  # 排除关键词
    
    def __post_init__(self):
        if self.interests is None:
            self.interests = []
        if self.languages is None:
            self.languages = []
        if self.exclude_keywords is None:
            self.exclude_keywords = []

class UserProfileManager:
    def __init__(self, profile_file: str = "user_profile.json"):
        self.profile_file = profile_file
        self.profile = self.load_profile()
    
    def load_profile(self) -> UserProfile:
        """加载用户偏好"""
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return UserProfile(**data)
            except Exception as e:
                print(f"⚠️ 加载用户偏好失败: {e}，使用默认配置")
        return UserProfile()
    
    def save_profile(self):
        """保存用户偏好"""
        try:
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.profile), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 保存用户偏好失败: {e}")
    
    def update_interests(self, interests: List[str]):
        """更新兴趣领域"""
        self.profile.interests = interests
        self.save_profile()
    
    def update_languages(self, languages: List[str]):
        """更新语言偏好"""
        self.profile.languages = languages
        self.save_profile()
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'interests': self.profile.interests,
            'languages': self.profile.languages,
            'min_stars': self.profile.min_stars,
        }

