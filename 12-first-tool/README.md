# Lesson 12: First tool

## Goal

Give the analysts an additional source of evidence through an ordinary Python function.

## What's here

```text
12-first-tool/
├── README.md
├── lesson.py
├── models.py
├── orchestrator.py  # changed
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── peter_lynch.py
│   └── warren_buffett.py
├── llm/
│   ├── __init__.py
│   └── client.py
└── tools/
    ├── __init__.py  # new
    └── market_data.py  # new
```

## New idea

`get_business_summary(ticker)` fetches Yahoo's business description and
returns a dictionary. The orchestrator calls it directly, adds its result to
the snapshot, and gives that snapshot to both analysts.

This function is a capability the agents can use as a tool. For now, Python
chooses when to call it; the model only reads its result. A missing description
stays `None`. A company description alone does not demonstrate a durable moat.
The existing `YFinanceService` is unchanged.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`,
run from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 12
```

This fetches live Yahoo data and makes two model calls. It needs internet
access.

Expected output: JSON with `business_summary` in the snapshot when Yahoo provides it, two analyst decisions, and the averaged final recommendation.
Live data and model responses can vary.
