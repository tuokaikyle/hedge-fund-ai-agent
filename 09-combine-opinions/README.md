# Lesson 9: Combine opinions

## Goal

Turn Buffett's and Lynch's independent decisions into one final signal, and
compare equal averaging with confidence-weighted averaging.

## What's here

```text
09-combine-opinions/
├── README.md
├── lesson.py                      # unchanged from lesson 8
├── models.py                      # changed: adds FinalRecommendation
├── orchestrator.py                # changed: combines the two decisions
├── yfinance_service.py            # unchanged from lesson 8
├── agents/
│   ├── __init__.py                # unchanged from lesson 8
│   ├── peter_lynch.py             # unchanged from lesson 8
│   └── warren_buffett.py          # unchanged from lesson 8
└── utils/
    ├── __init__.py                # unchanged from lesson 8
    ├── confidence.py              # unchanged from lesson 8
    └── data_completeness.py       # unchanged from lesson 8
```

## New idea

The orchestrator first averages the two scores equally. It then averages them
again using each agent's confidence as its weight. Lesson 7 already caps
confidence by data completeness, so missing inputs lower a weight without a
second completeness multiplier.

Both scores use the familiar cutoffs: 70 or more is `buy`, 45–69 is `hold`,
and below 45 is `sell`. `FinalRecommendation` shows the plain score and signal
beside the weighted score and final signal. These weights are teaching rules,
not probabilities that an agent is correct.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 9
```

This fetches live data and needs internet access. Expected output: JSON with
one `snapshot`, two `analyst_decisions`, and a `final_recommendation` containing
`plain_score`, `plain_signal`, `weighted_score`, and `signal`. Values depend on
the data Yahoo returns.
