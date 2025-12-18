"""ReAct 框架的工作流图定义

ReAct 工作流：
1. think -> 思考下一步行动
2. act -> 执行动作
3. observe -> 观察结果
4. 根据观察结果决定是否继续循环或结束
"""

from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from .nodes import think, act, observe, should_continue
from .state import ReActState

load_dotenv()

# 创建 ReAct 工作流图
graph = StateGraph(ReActState)

# 添加节点
graph.add_node("think", think)  # 思考节点
graph.add_node("act", act)  # 行动节点
graph.add_node("observe", observe)  # 观察节点

# 定义流程
graph.add_edge(START, "think")  # 从开始到思考
graph.add_edge("think", "act")  # 思考后执行行动
graph.add_edge("act", "observe")  # 行动后观察结果

# 根据观察结果决定是否继续循环
graph.add_conditional_edges(
    "observe",
    should_continue,
    {
        "continue": "think",  # 继续思考下一步
        "end": END  # 结束流程
    }
)

# 编译图
graph = graph.compile()

