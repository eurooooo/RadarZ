"""ReAct 框架的节点实现

包含三个核心节点：
1. think - 思考下一步行动
2. act - 执行动作（搜索、过滤、总结）
3. observe - 观察结果并更新状态
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from langchain.chat_models import init_chat_model
from tavily import TavilyClient

from .state import ReActState
from .schemas import ThoughtAction, SearchQueryList, RelevanceAssessmentList, FinalSummary
from .prompts import (
    react_system_prompt,
    search_query_prompt,
    relevance_assessment_prompt,
    final_summary_prompt
)

MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER") or None

def get_llm():
    return init_chat_model(model=MODEL_NAME, model_provider=MODEL_PROVIDER, temperature=0)


def think(state: ReActState) -> ReActState:
    """思考节点：分析当前状态，决定下一步行动
    
    这是 ReAct 框架的核心，Agent 会思考：
    - 当前已经收集了什么信息
    - 还需要什么信息
    - 下一步应该执行什么动作
    """
    # 构建已完成步骤的描述
    completed_steps = []
    if state.get('search_queries'):
        completed_steps.append(f"已生成 {len(state['search_queries'])} 个搜索查询")
    if state.get('search_results'):
        completed_steps.append(f"已收集 {len(state['search_results'])} 个搜索结果")
    if state.get('filtered_results'):
        completed_steps.append(f"已过滤得到 {len(state['filtered_results'])} 个相关结果")
    if not completed_steps:
        completed_steps.append("刚开始，尚未执行任何步骤")
    
    # 准备提示词
    messages = react_system_prompt.format_messages(
        project_name=state['project_name'],
        readme=state['readme'],
        completed_steps="; ".join(completed_steps),
        search_results_count=len(state.get('search_results', [])),
        filtered_results_count=len(state.get('filtered_results', [])),
        step_count=state.get('step_count', 0),
        max_steps=state.get('max_steps', 10)
    )
    
    # 调用 LLM 进行思考
    llm = get_llm()
    response = llm.with_structured_output(ThoughtAction).invoke(messages)
    
    # 记录思考内容
    thought_text = f"步骤 {state.get('step_count', 0) + 1}: {response.thought}"
    print(f"💭 {thought_text}")
    print(f"   📋 行动: {response.action}")
    if response.action_input:
        print(f"   📥 输入: {response.action_input}")
    
    # 更新状态
    return {
        'current_thought': response.thought,
        'current_action': response.action,
        'action_input': response.action_input,
        'thoughts': [thought_text],
        'should_continue': response.action != 'finish'
    }


def act(state: ReActState) -> ReActState:
    """行动节点：根据思考结果执行相应的动作
    
    支持的动作：
    - search: 执行网络搜索
    - filter: 过滤搜索结果
    - summarize: 生成最终总结
    - finish: 完成任务
    """
    action = state.get('current_action', '')
    
    print(f"🎬 执行动作: {action}")
    
    # 根据动作类型执行相应的操作
    if action == 'search':
        return _act_search(state)
    elif action == 'filter':
        return _act_filter(state)
    elif action == 'summarize':
        return _act_summarize(state)
    elif action == 'finish':
        return {'should_continue': False}
    else:
        # 如果没有明确动作，根据状态自动决定
        if not state.get('search_queries'):
            return _act_search(state)
        elif not state.get('filtered_results') and state.get('search_results'):
            return _act_filter(state)
        elif not state.get('final_summary') and state.get('filtered_results'):
            return _act_summarize(state)
        else:
            return {'should_continue': False}


def _act_search(state: ReActState) -> ReActState:
    """执行搜索动作：生成搜索查询并执行网络搜索"""
    print(f"🔍 执行搜索动作...")

    # 如果之前已经搜索过，就不再重复搜索，直接复用结果，加快速度
    if state.get("search_results"):
        print("   ℹ️ 已有搜索结果，本次跳过重新搜索")
        return {}
    
    # 生成搜索查询
    messages = search_query_prompt.format_messages(
        project_name=state['project_name'],
        readme=state['readme']
    )
    
    llm = get_llm()
    response = llm.with_structured_output(SearchQueryList).invoke(messages)
    
    # 只保留前 1~2 个查询，避免生成太多查询导致搜索太慢
    raw_queries = response.queries
    # 去重并保证顺序
    seen = set()
    deduped = []
    for q in raw_queries:
        q = q.strip()
        if not q:
            continue
        if q in seen:
            continue
        seen.add(q)
        deduped.append(q)

    # 最多只用 2 个查询
    search_queries = deduped[:2] or [state["project_name"]]
    print(f"   ✅ 生成搜索查询（已精简）: {search_queries}")
    
    # 执行网络搜索
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    all_results = []
    
    for query in search_queries:
        print(f"   🔍 搜索: {query}")
        try:
            results = tavily_client.search(
                query=query,
                # 每个查询最多拿少量结果，避免结果数量爆炸
                max_results=5,
                include_raw_content=True
            )
            search_results = results.get('results', [])
            all_results.extend(search_results)
            print(f"      ✅ 找到 {len(search_results)} 个结果")
        except Exception as e:
            print(f"      ❌ 搜索失败: {e}")
    
    print(f"   ✅ 总共收集到 {len(all_results)} 个搜索结果")
    
    return {
        'search_queries': search_queries,
        'search_results': all_results,
        'observations': [f"执行搜索，收集到 {len(all_results)} 个搜索结果"]
    }


def _act_filter(state: ReActState) -> ReActState:
    """执行过滤动作：过滤掉不相关的搜索结果"""
    print(f"🔍 执行过滤动作...")
    
    results = state.get('search_results', [])
    if not results:
        print("   ⚠️ 没有搜索结果需要过滤")
        return {'filtered_results': []}
    
    # 简化版过滤逻辑：不用再调用 LLM，一个项目一般也没那么多高质量外部信息
    # 规则：
    # 1. 只取前 N 条结果（按搜索引擎排序），N 默认 20
    # 2. 优先保留标题或 URL 中包含项目名 / 仓库名的结果
    max_keep = 20
    project_name = state.get("project_name", "").lower()
    repo_short = project_name.split("/")[-1] if project_name else ""

    strong_match: List[Dict[str, Any]] = []
    weak_match: List[Dict[str, Any]] = []

    for r in results:
        title = str(r.get("title", "")).lower()
        url = str(r.get("url", "")).lower()
        content = str((r.get("raw_content") or r.get("content") or "")).lower()

        text = title + " " + url + " " + content
        # 强匹配：包含完整仓库名或短名
        if project_name and project_name in text:
            strong_match.append(r)
        elif repo_short and repo_short in text:
            strong_match.append(r)
        else:
            weak_match.append(r)

    # 先放强匹配，再补充少量弱匹配，最多 max_keep 条
    filtered: List[Dict[str, Any]] = (strong_match + weak_match)[:max_keep]

    print(
        f"   ✅ 过滤完成：强匹配 {len(strong_match)} 条，总共保留 {len(filtered)} 条 "
        f"(原始 {len(results)} 条，仅依据简单规则快速筛选，不再调用 LLM)"
    )
    
    return {
        'filtered_results': filtered,
        'observations': [f"过滤搜索结果，保留 {len(filtered)} 个相关结果"]
    }


def _act_summarize(state: ReActState) -> ReActState:
    """执行总结动作：生成最终的项目总结"""
    print(f"📝 执行总结动作...")
    
    filtered_results = state.get('filtered_results', [])
    
    # 构建搜索结果的文本表示
    if filtered_results:
        results_text = "\n\n---\n\n".join([
            f"标题: {r.get('title', 'N/A')}\n"
            f"URL: {r.get('url', 'N/A')}\n"
            f"内容: {(r.get('raw_content') or r.get('content') or 'N/A')[:2000]}"
            for r in filtered_results
        ])
    else:
        results_text = "未找到相关的搜索结果。"
    
    # 构建提示词
    messages = final_summary_prompt.format_messages(
        project_name=state['project_name'],
        readme=state['readme'],
        filtered_results=results_text
    )
    
    # 调用 LLM 生成总结
    llm = get_llm()
    response = llm.with_structured_output(FinalSummary).invoke(messages)
    
    final_summary = response.summary
    print(f"   ✅ 生成总结 ({len(final_summary)} 字符)")
    
    # 将总结写入文件
    output_dir = Path(__file__).parent.parent.parent.parent / "summaries"
    output_dir.mkdir(exist_ok=True)
    
    # 生成安全的文件名
    safe_project_name = state['project_name'].replace("/", "_").replace("\\", "_")
    safe_project_name = "".join(c for c in safe_project_name if c.isalnum() or c in ('_', '-', '.'))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_project_name}_react_{timestamp}.md"
    filepath = output_dir / filename
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {state['project_name']} (ReAct 框架)\n\n")
        f.write(f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write(final_summary)
    
    print(f"   💾 总结已保存到: {filepath}")
    
    return {
        'final_summary': final_summary,
        'observations': [f"生成最终总结，共 {len(final_summary)} 字符"],
        'should_continue': False
    }


def observe(state: ReActState) -> ReActState:
    """观察节点：观察行动结果，更新状态，决定是否继续"""
    step_count = state.get('step_count', 0) + 1
    max_steps = state.get('max_steps', 10)
    
    # 检查是否应该继续
    should_continue = state.get('should_continue', True)
    
    # 检查是否超过最大步骤数
    if step_count >= max_steps:
        print(f"⚠️ 已达到最大步骤数 {max_steps}，停止执行")
        should_continue = False
    
    # 如果已经生成总结，则完成任务
    if state.get('final_summary'):
        should_continue = False
    
    print(f"👁️ 观察结果 - 步骤 {step_count}/{max_steps}, 继续: {should_continue}")
    
    return {
        'step_count': step_count,
        'should_continue': should_continue
    }


def should_continue(state: ReActState) -> str:
    """条件函数：决定是否继续执行 ReAct 循环"""
    if not state.get('should_continue', True):
        return "end"
    
    # 如果已经生成总结，结束
    if state.get('final_summary'):
        return "end"
    
    # 如果超过最大步骤数，结束
    if state.get('step_count', 0) >= state.get('max_steps', 10):
        return "end"
    
    return "continue"

