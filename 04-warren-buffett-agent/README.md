# Lesson 4: Buffett-style agent

## Goal

Add the first investor perspective. Junior scores one metric; this agent
chooses several metrics and weights them for a particular style while keeping
`analyze(snapshot) -> AnalystDecision`.

## What's here

```text
04-warren-buffett-agent/
├── README.md
├── lesson.py                      # changed: compares Junior with Buffett
├── models.py
├── yfinance_service.py
└── agents/
    ├── __init__.py
    ├── junior.py
    └── warren_buffett.py          # new
```

The Buffett-style agent scores ROE (30 points), debt-to-equity (25), profit
and operating margins (25), and trailing P/E (20). A score of 70 or more means
`buy`, 45–69 means `hold`, and below 45 means `sell`, as with Junior. Price
affects the score rather than overriding the final signal, so the decision
stays easy to trace. Missing fields receive partial points; when every field
is missing, the result is `hold`.

Trailing P/E is only a simple price check. One current snapshot cannot show
a durable competitive moat or calculate intrinsic value and margin of safety.
Those ideas are deliberately outside this lesson's small rule-based agent.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 4
```

This fetches live data and needs internet access. Expected output: Junior's
and the Buffett-style agent's signal, score, and explanation for the same
ticker. They can reach different calls.
