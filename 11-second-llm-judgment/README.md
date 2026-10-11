# Lesson 11: Second LLM judgment

## Goal

Give Lynch the same model-based assessment path as Buffett.

## What's here

```text
11-second-llm-judgment/
├── README.md
├── lesson.py
├── models.py  # changed
├── orchestrator.py
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── peter_lynch.py  # changed
│   └── warren_buffett.py
└── llm/
    ├── __init__.py
    └── client.py
```

## New idea

Lynch now returns the same `LLMJudgment` as Buffett. Each analyst receives
the same snapshot and returns the same `AnalystDecision`, but their prompts
focus on different evidence. Buffett emphasizes business quality and price;
Lynch emphasizes growth relative to price.

The rule-scoring methods are gone. The old explanation-only `ModelDecision`
is removed because neither analyst uses it. The client and orchestrator stay
unchanged: Python still derives signals and averages the two scores.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`,
run from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 11
```

This fetches live Yahoo data and makes two model calls. It needs internet
access.

Expected output: JSON with two model-based analyst decisions and their averaged final recommendation. Both scores and explanations can vary.
Live data and model responses can vary.
