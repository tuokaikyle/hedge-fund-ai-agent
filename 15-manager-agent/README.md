# Lesson 15: Manager agent

## Goal

Use an agent to combine the analysts’ assessments into a reasoned recommendation.

## What's here

```text
15-manager-agent/
├── README.md
├── lesson.py
├── models.py  # changed
├── orchestrator.py  # changed
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── manager.py  # new
│   ├── peter_lynch.py
│   ├── research.py
│   └── warren_buffett.py
├── llm/
│   ├── __init__.py
│   └── client.py
└── tools/
    ├── __init__.py
    └── market_data.py
```

## New idea

`ManagerAgent.combine` receives the snapshot, both analyst decisions,
and all tool results. It asks the model to explain agreement, disagreement,
and the tradeoff behind one final assessment. Analyst opinions are inputs to
consider, rather than additional facts.

The manager replaces arithmetic averaging. `FinalRecommendation` now includes
`reasoning` as well as score and signal. The manager supplies the score and
reasoning; Python derives the signal using the same cutoffs. The analyst code,
tool loop, and data functions are unchanged.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`,
run from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 15
```

This fetches live Yahoo data and makes up to nine model calls. It needs internet
access; the model and endpoint must support tool calling from lesson 13 onward.

Expected output: JSON with analyst decisions and tool traces, plus a manager-generated `final_recommendation` containing score, signal, and reasoning.
Live data and model responses can vary.
