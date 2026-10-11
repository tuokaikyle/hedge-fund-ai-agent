"""Ask for one tool call, execute it, and assess its evidence."""

import json

from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool

from llm.client import LLMClient
from models import LLMJudgment, StockSnapshot, ToolCall


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
    response = llm.request_tools(
        system_prompt=system_prompt + "\nFetch the business summary for this ticker.",
        messages=messages,
        tools=tools,
        require_tool=True,
    )
    messages.append(response)
    call = response.tool_calls[0]
    tool_by_name = {tool.name: tool for tool in tools}
    result = tool_by_name[call["name"]].invoke(call["args"])
    messages.append(ToolMessage(content=json.dumps(result), tool_call_id=call["id"]))
    trace = ToolCall(
        analyst=analyst, tool=call["name"], arguments=call["args"], result=result
    )
    messages.append(HumanMessage(content="Now assess the stock using the supplied evidence."))
    judgment = llm.invoke_messages(
        system_prompt=system_prompt,
        messages=messages,
        response_model=LLMJudgment,
    )
    return judgment, [trace]
