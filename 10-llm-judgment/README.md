# Lesson 10: LLM judgment

## Goal

Let Buffett make a model-based assessment instead of explaining a rule score.

## What's here

```text
10-llm-judgment/
├── README.md
├── lesson.py
├── models.py  # changed
├── orchestrator.py
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── peter_lynch.py
│   └── warren_buffett.py  # changed
└── llm/
    ├── __init__.py
    └── client.py
```

## New idea

Buffett now sends the snapshot to the model and asks for `LLMJudgment`:
a score from 0 to 100 and concise reasoning. Python still maps the score to
the familiar buy/hold/sell cutoffs and returns `AnalystDecision`.

Lynch still calculates his score with rules. This makes the change in
responsibility visible: Buffett's score can now vary between model calls.
The score expresses an assessment, not a probability or confidence measure.
The prompt asks the model to use supplied facts and treat missing data as unknown.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`,
run from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 10
```

This fetches live Yahoo data and makes two model calls. It needs internet
access.

Expected output: JSON with two analyst decisions and their averaged final recommendation. Buffett’s score and reasoning come from the model; Lynch’s score still comes from rules.
Live data and model responses can vary.
