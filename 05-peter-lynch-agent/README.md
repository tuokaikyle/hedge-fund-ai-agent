# Lesson 5: Lynch-style agent

## Goal

Add a second investor perspective. Buffett and Lynch use the same
`analyze(snapshot) -> AnalystDecision` shape, but judge the same stock with
different metrics and weights.

## What's here

```text
05-peter-lynch-agent/
├── README.md
├── lesson.py                      # changed: compares three agents
├── models.py
├── yfinance_service.py
└── agents/
    ├── __init__.py
    ├── junior.py
    ├── peter_lynch.py             # new
    └── warren_buffett.py
```

Buffett's price check uses P/E alone. Lynch asks whether growth might justify
that price. The new agent scores revenue growth (35 points), estimated PEG
(40), and earnings growth (25). PEG divides P/E by earnings growth in whole
percentage points: a P/E of 30 with 30% growth gives an estimated PEG of 1.
The total score uses the same buy/hold/sell cutoffs as the other agents. PEG
affects the score without a separate veto, and this agent does not add a debt
warning. That keeps the focus on growth relative to price and makes the final
signal easy to follow. Missing growth or price data receives partial points;
if all three scoring inputs are missing, the result is `hold`.

This is a teaching estimate, using Yahoo's reported earnings growth. A single
growth figure does not establish how fast earnings will grow in the future.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 5
```

This fetches live data and needs internet access. Expected output: Junior's,
Buffett's, and Lynch's signals, scores, and explanations for one ticker. The
two investor perspectives can disagree.
