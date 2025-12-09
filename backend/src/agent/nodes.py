from datetime import datetime
from schemas import SearchQueryList
from state import ResearchState
from prompts import query_writer_instructions
from langchain.chat_models import init_chat_model

def generate_queries(state: ResearchState) -> ResearchState:
    """生成3个不同维度的搜索查询"""
    
    llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", temperature=0)
    
    prompt = query_writer_instructions.format(
        project_name=state['project_name'],
        github_url=state['github_url'],
        language=state['repo_stats'].get('language', 'Unknown'),
        topics=', '.join(state['repo_stats'].get('topics', [])),
        readme_preview=state['readme'][:500]
    )
    
    response = llm.with_structured_output(SearchQueryList).invoke(prompt)
    
    state['search_queries'] = response.query
    return state

from tavily import TavilyClient
import asyncio
from collections import defaultdict

async def search_and_deduplicate(state: ResearchState) -> ResearchState:
    """并行搜索多个查询，然后去重"""
    
    tavily_client = TavilyClient(api_key="your-tavily-key")
    
    # 并行搜索所有查询
    async def search_single_query(query: str) -> List[Dict]:
        print(f"🔍 Searching: {query}")
        
        results = tavily_client.search(
            query=query,
            search_depth="advanced",  # 获取完整内容
            max_results=5,  # 每个查询最多5个结果
            include_raw_content=True  # ⭐ 包含完整网页内容
        )
        
        return results.get('results', [])
    
    # 并行执行所有搜索
    tasks = [search_single_query(q) for q in state['search_queries']]
    all_results = await asyncio.gather(*tasks)
    
    # 展平结果
    flat_results = []
    for results in all_results:
        flat_results.extend(results)
    
    print(f"📊 Total search results before deduplication: {len(flat_results)}")
    
    # 去重逻辑
    seen_urls = set()
    deduplicated = []
    
    for result in flat_results:
        url = result['url']
        
        # 规范化 URL（去掉 query params 和 fragments）
        from urllib.parse import urlparse
        parsed = urlparse(url)
        normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        if normalized_url not in seen_urls:
            seen_urls.add(normalized_url)
            deduplicated.append({
                'url': result['url'],
                'title': result['title'],
                'content': result.get('raw_content', result.get('content', '')),
                'score': result.get('score', 0)
            })
    
    print(f"✅ After deduplication: {len(deduplicated)} unique results")
    
    state['raw_search_results'] = flat_results
    state['deduplicated_results'] = deduplicated
    return state

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

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