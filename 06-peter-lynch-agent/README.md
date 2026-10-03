# Lesson 6: Lynch-style agent

## Goal

Add a second investor perspective. Buffett and Lynch use the same
`analyze(snapshot) -> AnalystDecision` shape, but judge the same stock with
different metrics and price rules.

## What's here

```text
06-peter-lynch-agent/
├── README.md
├── junior.py             # unchanged from lesson 5
├── lesson.py             # changed: compares four agents
├── models.py             # unchanged from lesson 5
├── peter_lynch.py        # new
├── senior.py             # unchanged from lesson 5
├── warren_buffett.py     # unchanged from lesson 5
└── yfinance_service.py   # changed: adds revenue and earnings growth
```

Buffett's price check uses P/E alone. Lynch asks whether growth might justify
that price. The new agent scores revenue growth (35 points), estimated PEG
(40), and earnings growth (25). PEG divides P/E by earnings growth in whole
percentage points: a P/E of 30 with 30% growth gives an estimated PEG of 1.
A `buy` needs a total score of at least 70, a fair or better PEG estimate,
and no high-debt warning. Debt-to-equity above 1.0 changes an otherwise
positive call to `hold`, without changing the growth score. Learners have
already seen this metric in lessons 4 and 5. Missing growth or price data
receives partial points; if all three scoring inputs are missing, the result
is `hold`.

This is a teaching estimate, using Yahoo's reported earnings growth. A single
growth figure does not establish how fast earnings will grow in the future.

## Run

From the repository root:

```bash
uv run python run.py --course 6 --ticker AAPL
```

This fetches live data and needs internet access. Expected output: Junior's,
Senior's, Buffett's, and Lynch's signals, scores, and explanations for one
ticker. The two investor perspectives can disagree.
