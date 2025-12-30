"""
升级版验证流程的工具函数
"""
import os
from langchain_core.tools import tool
from src.github.github_client import GitHubClient


@tool
def get_file_content(repo_full_name: str, file_path: str) -> str:
    """
    读取仓库中特定文件的内容
    
    Args:
        repo_full_name: 仓库全名，格式 "owner/repo"
        file_path: 文件路径（相对于仓库根目录）
    
    Returns:
        文件内容的字符串表示（已优化，去除无关内容）
    """
    github_token = os.getenv("GITHUB_TOKEN")
    github_client = GitHubClient(token=github_token)
    content = github_client.get_file_content(repo_full_name, file_path)
    
    if not content:
        return f"无法读取文件 {repo_full_name}/{file_path} 的内容（文件不存在或无法访问）"
    
    # 对于大文件，只返回关键部分
    max_length = 8000  # 增加一些长度，但仍有上限
    original_length = len(content)
    
    # 如果是代码文件，尝试提取关键部分（去除注释和空行）
    if file_path.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.go', '.rs')):
        lines = content.split('\n')
        # 过滤掉纯注释行和空行（保留一些关键注释）
        filtered_lines = []
        for line in lines:
            stripped = line.strip()
            # 保留非空行，以及包含关键信息的注释（如 TODO, FIXME, 函数说明等）
            if stripped and (not stripped.startswith('#') or 
                           any(keyword in stripped.lower() for keyword in ['todo', 'fixme', 'note', 'warning', 'def ', 'class ', 'function', 'export'])):
                filtered_lines.append(line)
        
        # 如果过滤后仍然太长，只取前一部分
        if len(filtered_lines) > 200:
            filtered_lines = filtered_lines[:200]
            content = '\n'.join(filtered_lines) + f"\n\n...(文件内容已截断，原始行数: {len(lines)} 行)"
        else:
            content = '\n'.join(filtered_lines)
    
    # 最终长度限制
    if len(content) > max_length:
        content = content[:max_length] + f"\n\n...(文件内容已截断，原始长度: {original_length} 字符)"
    
    return f"文件 {file_path} 的内容:\n\n{content}"


@tool
def search_code_in_repo(repo_full_name: str, keyword: str) -> str:
    """
    在仓库内搜索包含特定关键词的代码
    当需要查找特定功能、模块或实现时，应该先使用此工具进行精准搜索。
    - 示例：查找登录功能 → 搜索 "login" 或 "auth" 或 "authentication"
    - 示例：查找数据库配置 → 搜索 "database" 或 "db" 或 "sql"
    
    注意：每次调用只能搜索一个关键词。如果需要搜索多个关键词，请分别调用此工具。
    
    Args:
        repo_full_name: 仓库全名，格式 "owner/repo"
        keyword: 单个搜索关键词，例如 "login" 或 "auth"
    
    Returns:
        搜索结果，包含匹配的文件路径和相关信息。如果找到相关文件，可以使用 get_file_content 读取具体内容。
    """
    github_token = os.getenv("GITHUB_TOKEN")
    github_client = GitHubClient(token=github_token)
    
    results = github_client.search_code_in_repo(repo_full_name, keyword, limit=10)
    
    if not results:
        return f"在仓库 {repo_full_name} 中未找到包含关键词 '{keyword}' 的代码。\n建议：尝试使用其他相关关键词，或者检查关键词拼写是否正确。"
    
    # 格式化结果，突出显示文件路径
    result_text = f"✅ 在仓库 {repo_full_name} 中找到 {len(results)} 个包含关键词 '{keyword}' 的文件:\n\n"
    for i, result in enumerate(results, 1):
        result_text += f"{i}. 📄 {result['path']}\n"
        if result['name'] != result['path'].split('/')[-1]:
            result_text += f"   文件名: {result['name']}\n"
        result_text += f"   链接: {result['url']}\n\n"
    
    return result_text


# 创建工具列表（搜索优先）
validation_tools = [search_code_in_repo, get_file_content]

