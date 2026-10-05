# Lesson 12: Second LLM-backed agent

## Goal

Let Lynch use the shared LLM interface to make his own growth-focused assessment.

## What's here

```text
12-second-llm-backed-agent/
├── README.md
├── lesson.py                      # unchanged from lesson 11
├── models.py                      # changed: adds LynchModelDecision
├── orchestrator.py                # changed: gives the same client to both agents
├── yfinance_service.py            # unchanged from lesson 11
├── agents/
│   ├── __init__.py                # unchanged from lesson 11
│   ├── peter_lynch.py             # changed: requests a model score and explanation
│   └── warren_buffett.py          # unchanged from lesson 11
├── llm/
│   ├── __init__.py                # unchanged from lesson 11
│   ├── interface.py               # unchanged from lesson 11
│   └── openai_client.py           # unchanged from lesson 11
└── utils/
    ├── __init__.py                # unchanged from lesson 11
    ├── confidence.py              # unchanged from lesson 11
    └── data_completeness.py       # unchanged from lesson 11
```

## New idea

Both agents now follow the same path: score their own metrics with rules, pass
the rule score and notes to the shared client, and receive a typed `score` and
`reasoning`. Lynch's prompt focuses on growth and PEG; Buffett's prompt still
focuses on business quality and price. Each agent turns its model score into
`buy`, `hold`, or `sell` with the same cutoffs and computes completeness and
confidence in code. The orchestrator combines their decisions as before.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`, run
from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 12
```

Expected output is JSON with one `snapshot`, two model-backed
`analyst_decisions`, and a `final_recommendation`. This run fetches live Yahoo
data and makes two model calls, so scores and explanations can vary.
