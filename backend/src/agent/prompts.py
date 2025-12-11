from langchain_core.prompts import ChatPromptTemplate

query_writer_instructions = ChatPromptTemplate.from_messages([
  ("system", """你是在擅长使用搜索引擎进行搜索的专家，擅长使用搜索引擎进行搜索。
  你现在需要根据项目信息，生成搜索查询来了解这个项目。
  
  指令：
  - 优先只生成一个搜索查询，即项目名称本身的搜索查询。
  - 大多数情况下，都只需要使用项目名称这一个搜索查询即可。
  - 如果项目名称不明确或者很通用，比如是常见的名词，则生成除了项目名称以外的另一个查询，添加一些描述关键词来缩小搜索范围。

  返回一个包含搜索查询的列表。"""),
  ("user", """项目信息：
  - 项目名称：{project_name}
  - GitHub 地址：{github_url}
  - README ：{readme_preview}
  """)
])

relevance_assessment_system_prompt = ChatPromptTemplate.from_messages([
  ("system", """你是一个相关性评估专家，评估搜索结果是否与理解 GitHub 项目相关。

相关的结果包括：
- 项目的介绍、功能、特点。
- 使用场景、应用案例等。
- 技术讨论或教程

不相关的结果包括：
- 完全无关的主题
- 不针对该项目的通用编程教程
- 垃圾信息或低质量内容

对于每个搜索结果，请提供：
1. is_relevant: 布尔值，表示结果是否相关
2. relevance_score: 0 到 1 之间的浮点数，表示相关性分数
"""),

  ("user", """
  项目信息：
  - 项目名称：{project_name}
  - GitHub 地址：{github_url}
  - README ：{readme_preview}
  
  搜索结果：
  {search_results}
  
  请评估每个搜索结果与项目的相关性。返回一个评估列表，按顺序为每个结果提供一个评估。"""
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
- 总结应该对想要了解或使用这个项目的人有帮助
- **重要：输出必须使用 Markdown 格式**
"""),

  ("user", """项目信息：
- 项目名称：{project_name}
- GitHub 地址：{github_url}

README 内容：
{readme}

相关搜索结果：
{filtered_results}

请基于以上信息生成一份全面的项目总结报告。**请确保输出格式为 Markdown。**"""
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
- 总结应该对想要了解或使用这个项目的人有帮助
- **重要：输出必须使用 Markdown 格式**
"""),

  ("user", """项目信息：
- 项目名称：{project_name}
- GitHub 地址：{github_url}

README 内容：
{readme}

请基于以上信息生成一份全面的项目总结报告。**请确保输出格式为 Markdown。**"""
)
])