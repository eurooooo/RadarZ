from datetime import datetime
import os
from pathlib import Path
from langgraph.types import Send
from .schemas import FinalSummary, SearchQueryList, RelevanceAssessmentList
from .state import ResearchState, WebSearchState
from .prompts import query_writer_instructions, relevance_assessment_system_prompt, final_summary_prompt, test_summary_prompt
from langchain.chat_models import init_chat_model

from tavily import TavilyClient

MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER") or None

def get_llm():
    return init_chat_model(model=MODEL_NAME, model_provider=MODEL_PROVIDER, temperature=0)
    
def generate_queries(state: ResearchState) -> ResearchState:
    """生成搜索查询"""
    
    messages = query_writer_instructions.format_messages(
        project_name=state['project_name'],
        readme=state['readme']
    )

    llm = get_llm()
    
    response = llm.with_structured_output(SearchQueryList).invoke(messages)

    print(f"🔍 Generated search queries: {response.query}")

    return {'search_queries': response.query}
    # return {'search_queries': [state['project_name']]}

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
        readme=state['readme'],
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
    
    # 构建搜索结果的文本表示
    filtered_results = state.get('filtered_results', [])
    
    if filtered_results:
        results_text = "\n\n---\n\n".join([
            f"标题: {r.get('title', 'N/A')}\n"
            f"URL: {r.get('url', 'N/A')}\n"
            f"内容: {(r.get('raw_content') or r.get('content') or 'N/A')[:2000]}"
            for r in filtered_results
        ])
    else:
        results_text = "未找到相关的搜索结果。"
    
    # 构建 prompt
    messages = final_summary_prompt.format_messages(
        project_name=state['project_name'],
        readme=state['readme'],
        filtered_results=results_text
    )
    
    print(f"📝 Generating final summary for {state['project_name']}...")
    
    # 调用 LLM 生成总结
    llm = get_llm()
    response = llm.with_structured_output(FinalSummary).invoke(messages)
    
    final_summary = response.summary
    
    print(f"✅ Final summary generated ({len(final_summary)} characters)")
    
    # 将总结写入文件
    output_dir = Path(__file__).parent.parent.parent / "summaries"
    output_dir.mkdir(exist_ok=True)
    
    # 生成安全的文件名（处理特殊字符如 /）
    safe_project_name = state['project_name'].replace("/", "_").replace("\\", "_")
    safe_project_name = "".join(c for c in safe_project_name if c.isalnum() or c in ('_', '-', '.'))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_project_name}_{timestamp}.md"
    filepath = output_dir / filename
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {state['project_name']}\n\n")
        f.write(f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write(final_summary)
    
    print(f"💾 Summary saved to: {filepath}")
    
    return {'final_summary': final_summary}

def test_generate_final_summary(state: ResearchState) -> ResearchState:
    """基于 README 生成最终总结（测试用）"""
    
    # 构建 prompt
    messages = test_summary_prompt.format_messages(
        project_name=state['project_name'],
        readme=state['readme']
    )
    
    print(f"📝 Generating test summary for {state['project_name']}...")
    
    llm = get_llm()
    response = llm.invoke(messages)
    
    final_summary = response.content if hasattr(response, 'content') else str(response)
    
    print(f"✅ Test summary generated ({len(final_summary)} characters)")
    
    # 将总结写入文件（测试版本）
    output_dir = Path(__file__).parent.parent.parent / "summaries"
    output_dir.mkdir(exist_ok=True)
    
    # 生成安全的文件名（处理特殊字符如 /），并添加 test 标识
    safe_project_name = state['project_name'].replace("/", "_").replace("\\", "_")
    safe_project_name = "".join(c for c in safe_project_name if c.isalnum() or c in ('_', '-', '.'))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_project_name}_test_{timestamp}.md"
    filepath = output_dir / filename
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {state['project_name']} (测试版)\n\n")
        f.write(f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("**注意：** 这是基于 README 的测试版本总结，未包含网络搜索结果。\n\n")
        f.write("---\n\n")
        f.write(final_summary)
    
    print(f"💾 Test summary saved to: {filepath}")
    
    return {'final_summary': final_summary}