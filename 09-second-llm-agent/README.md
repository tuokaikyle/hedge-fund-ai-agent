# Lesson 9: Second LLM agent

## Goal

Let Lynch use the same `LLMClient` and `ModelDecision` to explain his
growth-focused rule score.

## What's here

```text
09-second-llm-agent/
├── README.md
├── lesson.py
├── models.py
├── orchestrator.py                # changed: gives the same client to both agents
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── peter_lynch.py             # changed: asks the model for an explanation
│   └── warren_buffett.py
└── llm/
    ├── __init__.py
    └── client.py
```

## New idea

Both agents now follow the same path: score their own metrics with rules, pass
the rule score and notes to the client, and receive a `ModelDecision` containing
only `model_reasoning`. Lynch's prompt focuses on growth and PEG; Buffett's
prompt still focuses on business quality and price. Each agent puts the model's
explanation in `AnalystDecision.reasoning`. Scores and signals remain
calculated in code. The orchestrator averages their rule-based scores as before.

The client and response model needed no change: Lynch supplies his own prompt
and reuses the same `ModelDecision` shape introduced in lesson 8.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`, run
from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 9
```

Expected output is JSON with one `snapshot`, two `analyst_decisions` with
model-generated explanations, and a `final_recommendation`. This run fetches
live Yahoo data and makes two model calls. Scores depend on the live data;
explanations can vary with the model responses.

## What you've built

A small agent system: one data service, two investor agents that share a
decision shape and an LLM client, and an orchestrator that fetches once and
combines their opinions.
