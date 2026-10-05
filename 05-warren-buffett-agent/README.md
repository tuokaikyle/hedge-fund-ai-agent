# Lesson 5: Buffett-style agent

## Goal

Add the first investor perspective. Junior and Senior show how to score one or
several metrics; this agent chooses metrics and weights them for a particular
style while keeping `analyze(snapshot) -> AnalystDecision`.

## What's here

```text
05-warren-buffett-agent/
├── README.md
├── lesson.py                      # changed: compares three agents
├── models.py                      # unchanged from lesson 4
├── yfinance_service.py            # changed: adds operating margin and trailing P/E
└── agents/
    ├── __init__.py                # unchanged from lesson 4
    ├── junior.py                  # unchanged from lesson 4
    ├── senior.py                  # unchanged from lesson 4
    └── warren_buffett.py          # new
```

The Buffett-style agent scores ROE (30 points), debt-to-equity (25), profit
and operating margins (25), and trailing P/E (20). A score of 70 or more means
`buy`, 45–69 means `hold`, and below 45 means `sell`, as with the earlier
agents. Price affects the score rather than overriding the final signal, so
the decision stays easy to trace. Missing fields receive partial points;
when every field is missing, the result is `hold`.

Trailing P/E is only a simple price check. One current snapshot cannot show
a durable competitive moat or calculate intrinsic value and margin of safety.
Those ideas are deliberately outside this lesson's small rule-based agent.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 5
```

This fetches live data and needs internet access. Expected output: Junior's,
Senior's, and the Buffett-style agent's signal, score, and explanation for
the same ticker. They can reach different calls.
