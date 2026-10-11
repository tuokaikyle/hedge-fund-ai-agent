# Lesson 13: Model calls a tool

## Goal

Let Buffett request a tool and use the returned evidence in his assessment.

## What's here

```text
13-model-calls-tool/
├── README.md
├── lesson.py
├── models.py  # changed
├── orchestrator.py  # changed
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── peter_lynch.py
│   ├── research.py  # new
│   └── warren_buffett.py  # changed
├── llm/
│   ├── __init__.py
│   └── client.py  # changed
└── tools/
    ├── __init__.py
    └── market_data.py  # changed
```

## New idea

The `@tool` decorator exposes the function's name, docstring, and typed
arguments to the model. `LLMClient.request_tools` asks the model for one tool
request. This lesson requires a tool call and offers only the business-summary
tool, so the sequence is easy to follow.

`research` keeps the model's request, executes the named Python tool, and sends
a `ToolMessage` back with the matching call ID. A final structured model call
produces `LLMJudgment`. The model requests an action; Python executes it.

The printed `tool_calls` list shows Buffett's tool name, arguments, and result.
Lynch still assesses the initial snapshot without requesting tools. The client
keeps provider settings and model calls in one place.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`,
run from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 13
```

This fetches live Yahoo data and makes three model calls. It needs internet
access; the model and endpoint must support tool calling from lesson 13 onward.

Expected output: JSON with two analyst decisions, the averaged recommendation, and one Buffett business-summary entry in `tool_calls`.
Live data and model responses can vary.
