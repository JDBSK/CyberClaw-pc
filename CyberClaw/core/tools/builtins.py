from datetime import datetime
from .base import cyberclaw_tool, CyberClawBaseTool

@cyberclaw_tool
def get_current_time() -> str:
    """
    获取当前的系统时间和日期。
    当用户询问“现在几点”、“今天星期几”、“今天几号”等与当前时间相关的问题时，调用此工具。
    """
    now = datetime.now()
    return f"当前本地系统时间是: {now.strftime('%Y-%m-%d %H:%M:%S')}"


@cyberclaw_tool
def calculator(expression: str) -> str:
    """
    一个简单的数学计算器。
    用于计算基础的数学表达式，例如: '3 * 5' 或 '100 / 4'。
    注意：参数 expression 必须是一个合法的 Python 数学表达式字符串。
    """
    try:
        # 警告: eval 在真实的生产环境中存在注入风险！
        # 这里仅为了搭建核心层做快速 Demo。未来在生产级扩展中，
        # 应该替换为基于 AST 的安全解析器，或者更专业的数学库（如 numexpr）。
        result = eval(expression, {"__builtins__": {}}, {})
        return f"表达式 '{expression}' 的计算结果是: {result}"
    except Exception as e:
        return f"计算出错，请检查表达式格式。错误信息: {str(e)}"


BUILTIN_TOOLS = [get_current_time, calculator]