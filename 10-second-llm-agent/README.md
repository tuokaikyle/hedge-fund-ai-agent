# Lesson 10: Second LLM agent

## Goal

Let Lynch use the same `LLMClient` to make his own growth-focused assessment.

## What's here

```text
10-second-llm-agent/
├── README.md
├── lesson.py
├── models.py                      # changed: adds LynchModelDecision
├── orchestrator.py                # changed: gives the same client to both agents
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── peter_lynch.py             # changed: asks the model for a decision
│   └── warren_buffett.py
├── llm/
│   ├── __init__.py
│   └── client.py
└── utils/
    ├── __init__.py
    ├── confidence.py
    └── data_completeness.py
```

## New idea

Both agents now follow the same path: score their own metrics with rules, pass
the rule score and notes to the client, and receive a typed `score` and
`reasoning`. Lynch's prompt focuses on growth and PEG; Buffett's prompt still
focuses on business quality and price. Each agent turns its model score into
`buy`, `hold`, or `sell` with the same cutoffs and computes completeness and
confidence in code. The orchestrator combines their decisions as before.

The client needed no change: a second agent only supplies its own prompt and
response model.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`, run
from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 10
```

Expected output is JSON with one `snapshot`, two model-backed
`analyst_decisions`, and a `final_recommendation`. This run fetches live Yahoo
data and makes two model calls, so scores and explanations can vary.

## What you've built

A small agent system: one data service, two investor agents that share a
decision shape and an LLM client, and an orchestrator that fetches once and
combines their opinions.
