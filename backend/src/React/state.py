from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator

class ReActState(TypedDict, total=False):
    """ReAct 框架的状态定义
    
    状态包含：
    - 输入信息（项目名称、README）
    - 思考过程（当前思考内容、已完成的步骤）
    - 行动结果（搜索查询、搜索结果、过滤结果）
    - 最终输出（总结）
    """
    # 输入信息
    project_name: str
    readme: str
    
    # 思考过程
    thoughts: Annotated[List[str], operator.add]  # 思考历史记录
    current_thought: str  # 当前思考内容
    current_action: str  # 当前要执行的动作（search/filter/summarize/finish）
    action_input: Optional[str]  # 动作的输入参数
    action_plan: List[str]  # 行动计划
    
    # 行动结果
    search_queries: Annotated[List[str], operator.add]  # 搜索查询列表
    search_results: Annotated[List[Dict[str, Any]], operator.add]  # 搜索结果
    filtered_results: Annotated[List[Dict[str, Any]], operator.add]  # 过滤后的结果
    
    # 观察结果
    observations: Annotated[List[str], operator.add]  # 观察记录
    
    # 最终输出
    final_summary: str
    
    # 控制流程
    step_count: int  # 步骤计数，防止无限循环
    max_steps: int  # 最大步骤数
    should_continue: bool  # 是否应该继续执行

