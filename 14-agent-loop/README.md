# Lesson 14: Agent loop

## Goal

Let each analyst choose whether another tool would help after seeing the first result.

## What's here

```text
14-agent-loop/
├── README.md
├── lesson.py
├── models.py
├── orchestrator.py  # changed
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── peter_lynch.py  # changed
│   ├── research.py  # changed
│   └── warren_buffett.py  # changed
├── llm/
│   ├── __init__.py
│   └── client.py
└── tools/
    ├── __init__.py
    └── market_data.py  # changed
```

## New idea

Both analysts now reuse `research`, which offers business-summary and
annual-revenue tools. The first request must use a tool; the prompt asks for
the business summary first. Later requests use automatic tool selection, so
the model can request revenue history or finish without another tool call.

The Python loop preserves requests and results as messages. It stops when the
model responds without a tool call or after three tool-request rounds. Python
then asks for a structured judgment using the gathered evidence. This limit
gives the lesson a definite ending, even if the model keeps requesting tools.

Revenue history lists available annual totals oldest first, in reported
currency units. Missing revenue data returns an empty list. The prompt asks
each analyst to use the input ticker and avoid repeating a tool. `tool_calls`
records what actually ran; tool choices can differ between analysts and runs.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`,
run from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 14
```

This fetches live Yahoo data and makes up to eight model calls. It needs internet
access; the model and endpoint must support tool calling from lesson 13 onward.

Expected output: JSON with both analyst decisions, their averaged recommendation, and tool traces labeled by analyst. Each analyst executes at least one tool; revenue-history requests depend on the model.
Live data and model responses can vary.
