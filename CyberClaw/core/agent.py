from typing import List, Optional
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage
from .context import AgentState, trim_context_messages
from .provider import get_provider
from .tools.builtins import BUILTIN_TOOLS
from .logger import audit_logger
from langchain_core.runnables import RunnableConfig

def create_agent_app(
    provider_name: str = "openai",
    model_name: str = "gpt-4o-mini",
    tools: Optional[List[BaseTool]] = None,
    checkpointer = None
):
 
    actual_tools = tools if tools is not None else BUILTIN_TOOLS
    
    tool_node = ToolNode(actual_tools)

    llm = get_provider(provider_name=provider_name, model_name=model_name)
    llm_with_tools = llm.bind_tools(actual_tools)

    def agent_node(state: AgentState, config: RunnableConfig) -> dict:
        """
        核心大脑：读取状态托盘里的历史消息，决定是直接回答，还是调用工具。
        """
        thread_id = config.get("configurable", {}).get("thread_id", "system_default")

        raw_messages = state["messages"]

        # 记录工具调用结果
        if raw_messages:
            last_msg = raw_messages[-1]
            if last_msg.type == "tool":
                audit_logger.log_event(
                    thread_id=thread_id,
                    event="tool_result",
                    tool=last_msg.name,
                    result_summary=last_msg.content[:200]
                )

        current_summary = state.get("summary", "")
        final_msgs, discarded_msgs = trim_context_messages(raw_messages, trigger_turns=8, keep_turns=4)
        state_updates = {}

        if discarded_msgs:
            print("\n到达记忆水位线, 正在将早期对话写入摘要记忆")
            discarded_text = "\n".join([f"{m.type}: {m.content}" for m in discarded_msgs if m.content])
        
            summary_prompt = (
                    f"你是一个负责维护 AI 长期记忆的后台模块。\n\n"
                    f"【现有的记忆档案】\n{current_summary if current_summary else '暂无记录'}\n\n"
                    f"【刚刚过去的旧对话】\n{discarded_text}\n\n"
                    f"任务：请仔细阅读旧对话，提取其中的关键信息（如用户的名字、偏好、重要事实或得出的结论）。\n"
                    f"动作：将这些新信息与【现有的记忆档案】进行无缝融合，输出一份最新的、全局的记忆摘要。\n"
                    f"要求：客观、精简，不要输出任何解释性废话，直接返回最新的记忆文本。"
                )
        
            # 这里可以用便宜模型
            new_summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
            active_summary = new_summary_response.content

            # 更新摘要
            state_updates["summary"] = active_summary

            # 从状态机中删除信息
            delete_cmds = [RemoveMessage(id=m.id) for m in discarded_msgs if m.id]
            state_updates["messages"] = delete_cmds
        else:
            active_summary = current_summary

        sys_prompt = (
            "你是 CyberClaw，一个聪明、高效、说话自然的 AI 助手。\n\n"
            "【对话核心原则】\n"
            "1. 像人类一样自然对话。\n"
            "2. 回答用户问题时, 需要参考你的长期记忆档案\n"
            "3. 保持简练，直接回应用户【最新】的一句话。"
        )

        if active_summary:
            sys_prompt += f"\n\n[你的长期记忆档案]\n{active_summary}\n\n(请在对话时参考上述记忆, 但不要主动提起你有一个记忆档案)"

        msgs_for_llm = [SystemMessage(content=sys_prompt)] + \
        [m for m in final_msgs if not isinstance(m, SystemMessage)]

        # 记录即将发送给发模型的消息 (监控Token)
        audit_logger.log_event(
            thread_id=thread_id,
            event="llm_input",
            message_count=len(msgs_for_llm)
        )

        response = llm_with_tools.invoke(msgs_for_llm)

        # 解析大模型的回答并记录到日志
        if response.tool_calls:
            for tool_call in response.tool_calls:
                audit_logger.log_event(
                    thread_id=thread_id,
                    event="tool_call",
                    tool=tool_call["name"],
                    args=tool_call["args"]
                )
        elif response.content:
            audit_logger.log_event(
                thread_id=thread_id,
                event="ai_message",
                content=response.content
            )

        if "messages" not in state_updates:
            state_updates["messages"] = []
        state_updates["messages"].append(response)

        return state_updates

    workflow = StateGraph(AgentState)


    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)


    workflow.add_edge(START, "agent")

    # 每次 agent 思考完，检查它有没有发出工具调用指令。
    # tools_condition 会自动判断：有指令 -> 走向 "tools" 节点；没指令 -> 走向 END。
    workflow.add_conditional_edges("agent", tools_condition)

    workflow.add_edge("tools", "agent")

    app = workflow.compile(checkpointer=checkpointer)

    return app
