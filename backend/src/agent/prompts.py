from langchain_core.prompts import ChatPromptTemplate

query_writer_instructions = ChatPromptTemplate.from_messages([
  ("system", """你是一个专业的技术研究助手，擅长分析GitHub项目并生成有效的搜索查询。
  
  指令：
  - 生成 3 个不同维度的搜索查询，用于从不同角度了解这个项目。
  - 每个查询应专注于一个特定方面：
    - 项目评价和比较：搜索项目的评论、与其他项目的比较、优缺点分析
    - 实际使用案例：搜索项目的实际应用场景、案例研究、使用教程
    - 技术讨论和问题：搜索项目的技术讨论、已知问题、限制或改进建议
  - 查询应该具体且针对性强，避免过于宽泛的搜索词。
  - 可以包含项目名称、主要功能关键词、技术栈等相关信息。
  - 查询应使用中文或英文，根据项目的主要语言和受众选择。
  
  返回一个包含3个搜索查询的列表。"""),
  ("user", """项目信息：
  - 项目名称：{project_name}
  - GitHub 地址：{github_url}
  - README 预览：{readme_preview}
  """)
])

relevance_assessment_system_prompt = ChatPromptTemplate.from_messages([
  ("system", """You are a relevance assessment expert. 
Evaluate if search results are relevant to understanding a GitHub project.

Relevant results include:
- Reviews, opinions, or comparisons of the project
- Real-world usage examples or case studies
- Technical discussions or tutorials
- Issues, limitations, or criticisms

Irrelevant results include:
- Completely unrelated topics
- Generic programming tutorials not specific to this project
- Spam or low-quality content

For each search result, provide:
1. is_relevant: boolean indicating if the result is relevant
2. relevance_score: a float between 0 and 1 indicating how relevant it is
"""),

  ("user", """Project: {project_name}
  README: {readme_preview}
  
  Search Results:
  {search_results}
  
  Please assess the relevance of each search result to the project. Return a list of assessments, one for each result in the same order."""
)
])
