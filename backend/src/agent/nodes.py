from datetime import datetime
import os
from langgraph.types import Send
from .schemas import SearchQueryList, RelevanceAssessmentList
from .state import ResearchState, WebSearchState
from .prompts import query_writer_instructions, relevance_assessment_system_prompt
from langchain.chat_models import init_chat_model

from tavily import TavilyClient
from typing import Dict

def get_llm():
    return init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", temperature=0)

def generate_queries(state: ResearchState) -> ResearchState:
    """生成3个不同维度的搜索查询"""
    
    messages = query_writer_instructions.format_messages(
        project_name=state['project_name'],
        github_url=state['github_url'],
        readme_preview=state['readme'][:500]
    )

    llm = get_llm()
    
    response = llm.with_structured_output(SearchQueryList).invoke(messages)
    
    # return {'search_queries': response.query}
    return {'search_queries': [state['project_name']]}

def to_web_research(state: ResearchState):
    """LangGraph node that sends the search queries to the web research node.

    This is used to spawn n number of web research nodes, one for each search query.
    """
    return [
        Send("web_research", {"search_query": search_query})
        for search_query in state["search_queries"]
    ]

def web_research(state: WebSearchState) -> ResearchState:
    """处理单个搜索查询（由 Send 并行调用）"""
    
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    # 从 Send 传递的 state 中获取单个查询
    query = state['search_query']
    
    print(f"🔍 Searching: {query}")
    
    # 执行单个查询的搜索
    results = tavily_client.search(
        query=query,
        max_results=10,
        include_raw_content=True  # 包含完整网页内容
    )
    
    search_results = results.get('results', [])
    # 只返回原始结果，LangGraph 会自动合并（使用 operator.add）
    return {
        'search_results': search_results
    }

def filter_irrelevant_results(state: ResearchState) -> ResearchState:
    """用 LLM 过滤掉不相关的搜索结果（一次性处理所有结果）"""
    
    # 构建所有搜索结果的文本表示
    results = state['search_results']
    search_results_text = "\n\n---\n\n".join([
        f"Result {i+1}:\nTitle: {r['title']}\nURL: {r['url']}\nContent Preview:\n{(r.get('raw_content') or r.get('content') or 'None')[:1000]}"
        for i, r in enumerate(results)
    ])
    
    prompt = relevance_assessment_system_prompt.format_messages(
        project_name=state['project_name'],
        readme_preview=state['readme'][:500],
        search_results=search_results_text
    )
    
    print(f"🔍 Filtering {len(results)} results...")
    
    # 一次性评估所有结果
    response = get_llm().with_structured_output(RelevanceAssessmentList).invoke(prompt)
    
    assessments = response.assessments
    
    # 确保评估结果数量与搜索结果数量一致
    if len(assessments) != len(results):
        print(f"⚠️ Warning: Expected {len(results)} assessments, got {len(assessments)}")
        # 如果数量不匹配，只处理匹配的部分
        min_len = min(len(assessments), len(results))
        assessments = assessments[:min_len]
        results = results[:min_len]
    
    # 只保留相关的结果（relevance_score > 0.6）
    filtered = []
    for result, assessment in zip(results, assessments):
        if assessment.is_relevant and assessment.relevance_score > 0.6:
            filtered.append(result)
            print(f"   ✅ {result['title'][:60]}... url: {result['url']} (score: {assessment.relevance_score:.2f})")
        else:
            print(f"   ❌ {result['title'][:60]}... url: {result['url']} (score: {assessment.relevance_score:.2f})")
    
    print(f"✅ Filtered down to {len(filtered)} relevant results")
    
    return {'filtered_results': filtered}

def generate_final_summary(state: ResearchState) -> ResearchState:
    """基于 README 和搜索结果生成最终总结"""
    
    llm = init_chat_model(
        model="claude-3-5-sonnet-20241022",
        model_provider="anthropic",
        temperature=0
    )
    
    # 构建搜索结果的上下文
    search_context = "\n\n---\n\n".join([
        f"Source: {r['title']}\nURL: {r['url']}\nRelevance: {r['relevance_score']:.2f}\n\nContent:\n{r['content'][:3000]}..."
        for r in state['filtered_results'][:10]  # 最多用前10个结果
    ])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a technical writer creating a comprehensive project summary.
        
        Your summary should include:
        1. **Overview**: What the project does (1-2 sentences)
        2. **Key Features**: Main functionalities (bullet points)
        3. **Technical Highlights**: Interesting technical approaches or innovations
        4. **Real-World Reception**: What users/community think (based on search results)
        5. **Pros**: Strengths of the project
        6. **Cons**: Limitations or issues (if any mentioned)
        7. **Comparison**: How it differs from alternatives (if discussed)
        8. **Use Cases**: Who should use this and when
        
        Be objective and cite sources when making claims.
        Use markdown formatting."""),
        
        ("user", """Project: {project_name}
        GitHub: {github_url}
        Stars: {stars} | Language: {language}
        
        === PROJECT README ===
        {readme}
        
        === EXTERNAL RESEARCH (from web search) ===
        {search_context}
        
        Generate a comprehensive summary:""")
    ])
    
    print("📝 Generating final summary...")
    
    response = llm.invoke(prompt.format_messages(
        project_name=state['project_name'],
        github_url=state['github_url'],
        stars=state['repo_stats'].get('stars', 'N/A'),
        language=state['repo_stats'].get('language', 'Unknown'),
        readme=state['readme'][:5000],  # README 限制长度避免超 token
        search_context=search_context
    ))
    
    state['final_summary'] = response.content
    print("✅ Summary generated!")
    
    return state