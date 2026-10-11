"""Gather evidence in a bounded tool loop, then assess the stock."""

import json

from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool

from llm.client import LLMClient
from models import LLMJudgment, StockSnapshot, ToolCall


MAX_TOOL_ROUNDS = 3


# changed in lesson 13, 14
def research(
    llm: LLMClient,
    system_prompt: str,
    snapshot: StockSnapshot,
    tools: list[BaseTool],
    *,
    analyst: str,
) -> tuple[LLMJudgment, list[ToolCall]]:
    messages: list[BaseMessage] = [
        HumanMessage(content=snapshot.model_dump_json(exclude_none=True))
    ]
    tool_by_name = {tool.name: tool for tool in tools}
    traces: list[ToolCall] = []
    research_prompt = system_prompt + (
        "\nFirst fetch the business summary. Then decide whether annual revenue "
        "history would help your assessment. Use only this snapshot's ticker. "
        "Do not request the same tool twice. When you have enough evidence, "
        "reply 'ready' without a tool call."
    )
    for step in range(MAX_TOOL_ROUNDS):
        response = llm.request_tools(
            system_prompt=research_prompt,
            messages=messages,
            tools=tools,
            require_tool=step == 0,
        )
        messages.append(response)
        if not response.tool_calls:
            break
        for call in response.tool_calls:
            result = tool_by_name[call["name"]].invoke(call["args"])
            messages.append(ToolMessage(content=json.dumps(result), tool_call_id=call["id"]))
            traces.append(ToolCall(
                analyst=analyst, tool=call["name"], arguments=call["args"], result=result
            ))

    messages.append(HumanMessage(content=(
        "Research is finished. Assess the stock using only the evidence gathered. "
        "Mention any important information that is still missing."
    )))
    judgment = llm.invoke_messages(
        system_prompt=system_prompt,
        messages=messages,
        response_model=LLMJudgment,
    )
    return judgment, traces
