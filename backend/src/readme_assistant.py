from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model


class ReadmeAssistant:
    """使用 LangChain 对 README 文本生成摘要"""

    def __init__(self, model: str = "gemini-2.5-flash", temperature: float = 0.2):
        # 构建简单的 LCEL chain：prompt -> LLM -> 纯文本解析
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "你是资深技术解读助手。"
                        "请用简洁中文总结项目 README，包含："
                        "1) 项目定位/核心功能；2) 主要特性或技术栈；"
                        "3) 安装/运行方式（如有）；4) 适用场景或价值。"
                        "保持条理清晰，避免冗长。"
                    ),
                ),
                ("user", "{readme_text}"),
            ]
        )

        # 使用新版工厂函数创建聊天模型
        llm = init_chat_model(model=model, temperature=temperature)
        self.chain = prompt | llm | StrOutputParser()

    def summarize(self, readme_text: str) -> str:
        """生成 README 摘要"""
        if not readme_text:
            return "README 内容为空，无法生成摘要。"

        # 避免异常导致调用方崩溃
        try:
            return self.chain.invoke({"readme_text": readme_text})
        except Exception as exc:
            return f"生成摘要时出错：{exc}"

