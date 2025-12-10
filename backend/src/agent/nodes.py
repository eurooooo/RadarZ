from datetime import datetime
import os
from langgraph.types import Send
from .schemas import SearchQueryList
from .state import ResearchState, WebSearchState
from .prompts import query_writer_instructions
from langchain.chat_models import init_chat_model

from tavily import TavilyClient
from typing import Dict

def generate_queries(state: ResearchState) -> ResearchState:
    """生成3个不同维度的搜索查询"""
    
    llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", temperature=0)
    
    prompt = query_writer_instructions.format(
        project_name=state['project_name'],
        github_url=state['github_url'],
        readme_preview=state['readme'][:500]
    )
    
    response = llm.with_structured_output(SearchQueryList).invoke(prompt)
    
    return {'search_queries': response.query}

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
        search_depth="advanced",  # 获取完整内容
        max_results=10,
        include_raw_content=True  # 包含完整网页内容
    )
    
    search_results = {
        'query': results.get('query'),
        'title': results.get('results')[0].get('title'),
    }
    # 只返回原始结果，LangGraph 会自动合并（使用 operator.add）
    return {
        'raw_search_results': [search_results]
    }

def aggregate_and_deduplicate(state: ResearchState) -> ResearchState:
    """聚合所有搜索结果并去重"""
    from urllib.parse import urlparse
    
    # 展平所有结果（因为 operator.add 可能产生嵌套列表）
    flat_results = []
    raw_results = state.get('raw_search_results', [])
    
    # 处理 raw_search_results（可能是列表的列表，因为 operator.add 会合并列表）
    if raw_results:
        for item in raw_results:
            if isinstance(item, list):
                flat_results.extend(item)
            else:
                flat_results.append(item)
    
    print(f"📊 Total search results before deduplication: {len(flat_results)}")
    
    # 去重逻辑
    seen_urls = set()
    deduplicated = []
    
    for result in flat_results:
        url = result.get('url', '')
        
        # 规范化 URL（去掉 query params 和 fragments）
        parsed = urlparse(url)
        normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        if normalized_url and normalized_url not in seen_urls:
            seen_urls.add(normalized_url)
            deduplicated.append({
                'url': result.get('url', ''),
                'title': result.get('title', ''),
                'content': result.get('raw_content', result.get('content', '')),
                'score': result.get('score', 0)
            })
    
    print(f"✅ After deduplication: {len(deduplicated)} unique results")
    
    return {'deduplicated_results': deduplicated}

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import asyncio
class RelevanceAssessment(BaseModel):
    """相关性评估结果"""
    is_relevant: bool = Field(description="是否与项目相关")
    relevance_score: float = Field(description="相关性分数 0-1")
    reason: str = Field(description="判断理由")

async def filter_irrelevant_results(state: ResearchState) -> ResearchState:
    """用 LLM 过滤掉不相关的搜索结果"""
    
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0
    ).with_structured_output(RelevanceAssessment)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a relevance assessment expert. 
        Evaluate if a search result is relevant to understanding a GitHub project.
        
        Relevant results include:
        - Reviews, opinions, or comparisons of the project
        - Real-world usage examples or case studies
        - Technical discussions or tutorials
        - Issues, limitations, or criticisms
        
        Irrelevant results include:
        - Completely unrelated topics
        - Generic programming tutorials not specific to this project
        - Spam or low-quality content"""),
        
        ("user", """Project: {project_name}
        README: {readme_preview}
        
        Search Result:
        Title: {title}
        URL: {url}
        Content Preview (first 1000 chars):
        {content_preview}
        
        Assess relevance:""")
    ])
    
    # 并行评估所有结果
    async def assess_single_result(result: Dict) -> tuple[Dict, RelevanceAssessment]:
        assessment = await llm.ainvoke(prompt.format_messages(
            project_name=state['project_name'],
            readme_preview=state['readme'][:500],
            title=result['title'],
            url=result['url'],
            content_preview=result['content'][:1000]
        ))
        return result, assessment
    
    print(f"🔍 Filtering {len(state['deduplicated_results'])} results...")
    
    tasks = [assess_single_result(r) for r in state['deduplicated_results']]
    assessments = await asyncio.gather(*tasks)
    
    # 只保留相关的结果（relevance_score > 0.6）
    filtered = []
    for result, assessment in assessments:
        if assessment.is_relevant and assessment.relevance_score > 0.6:
            result['relevance_score'] = assessment.relevance_score
            result['relevance_reason'] = assessment.reason
            filtered.append(result)
            print(f"   ✅ {result['title'][:60]}... (score: {assessment.relevance_score:.2f})")
        else:
            print(f"   ❌ {result['title'][:60]}... (score: {assessment.relevance_score:.2f})")
    
    # 按相关性排序
    filtered.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    print(f"✅ Filtered down to {len(filtered)} relevant results")
    
    state['filtered_results'] = filtered
    return state

def generate_final_summary(state: ResearchState) -> ResearchState:
    """基于 README 和搜索结果生成最终总结"""
    
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    
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