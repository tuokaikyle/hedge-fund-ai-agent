# Lesson 6: Data completeness and confidence

## Goal

Add two measures to each agent's decision: how much expected data was
available and how strongly its rules support the final signal. Keep the
stock scores and buy/hold/sell rules from lesson 5.

## What's here

```text
06-data-completeness-and-confidence/
├── README.md
├── lesson.py                      # changed: prints both measures
├── models.py                      # changed: adds both fields to AnalystDecision
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── junior.py                  # changed: reports both measures
│   ├── peter_lynch.py             # changed: reports both measures
│   └── warren_buffett.py          # changed: reports both measures
└── utils/
    ├── __init__.py                # new
    ├── confidence.py              # new: estimates strength of the final signal
    └── data_completeness.py       # new: counts available inputs
```

Every agent calls `data_completeness` with the fields it expects. The helper
counts fields that are present and returns a percentage. For example, if
Buffett receives four of its five fields, its data completeness is 80%.
Junior can report 100% from just one ROE field: that means its *own* input
is present, not that its call is certain or as well informed as Buffett's.

`decision_confidence` asks how far the score is from the nearest decision
cutoff: 70 for `buy`, 45 for `sell`, or either edge of the `hold` range.
Confidence cannot exceed data completeness, so a decision with no input data
has confidence 0. For complete data, a `buy` score of 71 gives confidence 51,
while a `buy` score of 90 gives confidence 70.

Both percentages are teaching rules, not measured probabilities of being
correct. A stock can have complete data but low confidence when its score
barely crosses a decision cutoff. Later, an orchestrator can use the two
measures when combining agents' opinions.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 6
```

This fetches live data and needs internet access. Expected output: the same
three signals, scores, and explanations as lesson 5, now with data
completeness and confidence beside each score. Values depend on the data
Yahoo returns.
