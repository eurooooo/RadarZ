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

final_summary_prompt = ChatPromptTemplate.from_messages([
  ("system", """你是一个专业的技术项目分析专家，擅长综合项目文档和外部信息生成全面的项目总结。

你的任务是基于项目的 README 文档和从网络搜索获得的相关信息，生成一份全面、客观的项目总结报告。

总结应该包括：
1. 项目概述：项目的核心功能、定位和目标
2. 技术特点：主要技术栈、架构特点、技术亮点
3. 项目评价：来自社区的反馈、评价、优缺点分析
4. 使用场景：实际应用案例、适用场景
5. 潜在问题：已知的限制、问题或改进建议
6. 总结：对项目的整体评价和建议

要求：
- 内容要客观、全面，基于提供的 README 和搜索结果
- 如果搜索结果提供了有价值的外部视角，要整合进去
- 如果搜索结果不够充分，主要基于 README 进行分析
- 使用清晰的结构和专业的语言
- 总结应该对想要了解或使用这个项目的人有帮助"""),

  ("user", """项目信息：
- 项目名称：{project_name}
- GitHub 地址：{github_url}

README 内容：
{readme}

相关搜索结果：
{filtered_results}

请基于以上信息生成一份全面的项目总结报告。"""
)
])

test_summary_prompt = ChatPromptTemplate.from_messages([
  ("system", """你是一个专业的技术项目分析专家，擅长综合项目文档生成全面的项目总结。

你的任务是基于项目的 README 文档，生成一份全面、客观的项目总结报告。

总结应该包括：
1. 项目概述：项目的核心功能、定位和目标
2. 技术特点：主要技术栈、架构特点、技术亮点
3. 项目评价：来自社区的反馈、评价、优缺点分析
4. 使用场景：实际应用案例、适用场景
5. 潜在问题：已知的限制、问题或改进建议
6. 总结：对项目的整体评价和建议

要求：
- 内容要客观、全面，基于提供的 README
- 使用清晰的结构和专业的语言
- 总结应该对想要了解或使用这个项目的人有帮助"""),

  ("user", """项目信息：
- 项目名称：{project_name}
- GitHub 地址：{github_url}

README 内容：
{readme}

请基于以上信息生成一份全面的项目总结报告。"""
)
])