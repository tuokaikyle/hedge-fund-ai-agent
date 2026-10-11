# Lesson 17: Revise after feedback

## Goal

Let the manager respond to review while preserving the result before feedback.

## What's here

```text
17-revise-after-feedback/
├── README.md
├── lesson.py
├── models.py  # changed
├── orchestrator.py  # changed
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── manager.py  # changed
│   ├── peter_lynch.py
│   ├── research.py
│   ├── reviewer.py
│   └── warren_buffett.py
├── llm/
│   ├── __init__.py
│   └── client.py
└── tools/
    ├── __init__.py
    └── market_data.py
```

## New idea

The orchestrator saves `original_recommendation` and sends the completed
analysis, including its review, to `ManagerAgent.revise`. If the reviewer
returned `"no issue"`, the manager keeps the original result without another
model call. Otherwise, it makes one revision call using the same evidence.

The revision prompt asks the manager to check the feedback, address valid
issues, and explain any change. It can correct the explanation while keeping
the score. It can also retain an assessment when the review is mistaken.

`final_recommendation` contains the result after feedback. Printing it beside
`original_recommendation` and `review` makes agent interaction visible. There
is no repeated review cycle: this lesson ends after one opportunity to revise.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`,
run from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 17
```

This fetches live Yahoo data and makes up to eleven model calls. It needs internet
access; the model and endpoint must support tool calling from lesson 13 onward.

Expected output: JSON with `original_recommendation`, `review`, and `final_recommendation`, alongside the snapshot, analyst decisions, and tool traces. With "no issue", both recommendations match.
Live data and model responses can vary.
