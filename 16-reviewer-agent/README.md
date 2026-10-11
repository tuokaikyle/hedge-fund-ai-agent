# Lesson 16: Reviewer agent

## Goal

Have a separate agent check whether the manager’s recommendation follows from the evidence.

## What's here

```text
16-reviewer-agent/
├── README.md
├── lesson.py
├── models.py  # changed
├── orchestrator.py  # changed
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── manager.py
│   ├── peter_lynch.py
│   ├── research.py
│   ├── reviewer.py  # new
│   └── warren_buffett.py
├── llm/
│   ├── __init__.py
│   └── client.py
└── tools/
    ├── __init__.py
    └── market_data.py
```

## New idea

`ReviewerAgent.review` reads the completed analysis and returns `Review`.
Its `issue` contains one concrete evidence problem and how to address it, or
exactly `"no issue"`. The reviewer checks unsupported claims, contrary evidence,
and missing data presented as known; it does not invent more research.

The orchestrator adds the review to the output. The recommendation is still
the manager's original assessment. Review is a model judgment too, so it can
be mistaken; this lesson makes the feedback visible before acting on it.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`,
run from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 16
```

This fetches live Yahoo data and makes up to ten model calls. It needs internet
access; the model and endpoint must support tool calling from lesson 13 onward.

Expected output: JSON with the manager’s recommendation and a `review.issue` containing one concrete issue or "no issue".
Live data and model responses can vary.
