from typing import List, Dict, Optional
from openai import OpenAI
import os
import re

class AIRecommender:
    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("需要设置 OPENAI_API_KEY 环境变量")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # 使用更经济的模型
    
    def generate_recommendations(self, 
                                repositories: List[Dict],
                                user_profile: Dict,
                                top_n: int = 10) -> List[Dict]:
        """使用AI生成个性化推荐"""
        
        if not repositories:
            return []
        
        # 构建提示词
        prompt = self._build_prompt(repositories, user_profile, top_n)
        
        try:
            # 调用AI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "你是一个专业的GitHub项目推荐助手，能够根据用户偏好推荐合适的开源项目。请用中文回复，并严格按照指定格式输出。"
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            
            # 解析AI返回的推荐结果
            ai_response = response.choices[0].message.content
            recommendations = self._parse_recommendations(ai_response, repositories)
            
            return recommendations[:top_n]
        except Exception as e:
            print(f"❌ AI推荐生成失败: {e}")
            # 降级方案：返回按stars排序的前N个
            return sorted(repositories, key=lambda x: x['stars'], reverse=True)[:top_n]
    
    def _build_prompt(self, repos: List[Dict], profile: Dict, top_n: int) -> str:
        """构建AI提示词"""
        # 限制项目数量以节省token
        repos_to_analyze = repos[:50]
        
        repos_summary = "\n".join([
            f"- {r['name']}: {r['description']} (⭐{r['stars']}, 语言: {r['language']}, 主题: {', '.join(r.get('topics', [])[:3])})"
            for r in repos_to_analyze
        ])
        
        interests = ', '.join(profile.get('interests', [])) or '未指定'
        languages = ', '.join(profile.get('languages', [])) or '未指定'
        
        return f"""请根据以下用户偏好，从这些GitHub项目中推荐最合适的 {top_n} 个项目：

用户偏好：
- 兴趣领域：{interests}
- 编程语言：{languages}
- 最小stars数：{profile.get('min_stars', 10)}

可用项目列表：
{repos_summary}

请为每个推荐项目提供以下信息（严格按照格式）：
项目名称: [完整的项目名称，如 owner/repo]
推荐理由: [为什么这个项目适合该用户，2-3句话]
项目亮点: [项目的1-2个主要特点]

示例格式：
项目名称: owner/repo-name
推荐理由: 这个项目符合用户的兴趣领域，使用了用户熟悉的编程语言...
项目亮点: 项目活跃度高，文档完善

---
[继续列出其他推荐项目]
"""
    
    def _parse_recommendations(self, ai_response: str, repos: List[Dict]) -> List[Dict]:
        """解析AI返回的推荐结果"""
        recommendations = []
        repo_dict = {r['name']: r for r in repos}
        
        # 使用正则表达式提取推荐信息
        pattern = r'项目名称:\s*(.+?)\n推荐理由:\s*(.+?)\n项目亮点:\s*(.+?)(?=\n项目名称:|\n---|$)'
        matches = re.findall(pattern, ai_response, re.DOTALL)
        
        for match in matches:
            repo_name = match[0].strip()
            reason = match[1].strip()
            highlights = match[2].strip()
            
            if repo_name in repo_dict:
                recommendations.append({
                    **repo_dict[repo_name],
                    'recommendation_reason': reason,
                    'highlights': highlights,
                })
        
        # 如果正则解析失败，尝试简单匹配
        if not recommendations:
            for repo in repos:
                if repo['name'] in ai_response:
                    recommendations.append({
                        **repo,
                        'recommendation_reason': 'AI推荐的项目',
                        'highlights': '请查看项目详情',
                    })
        
        return recommendations

