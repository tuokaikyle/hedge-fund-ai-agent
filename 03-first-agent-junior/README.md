# Lesson 3: First agent

## Goal

Turn the `StockSnapshot` from lesson 2 into a simple, structured decision.
This first agent reads only return on equity (ROE). Its decision is a fixed
rule, with no LLM or investor persona.

## What's here

```text
03-first-agent-junior/
├── README.md
├── lesson.py                      # changed from lesson 2
├── models.py                      # changed: adds Signal and AnalystDecision
├── yfinance_service.py            # unchanged from lesson 2
└── agents/
    ├── __init__.py                # new
    └── junior.py                  # new
```

`JuniorAgent.analyze(snapshot)` returns an `AnalystDecision`: a buy, hold, or
sell signal, a score, and a short explanation. `lesson.py` fetches the
snapshot and prints that decision. The agent itself does not fetch data.

## Why one metric

Using only ROE makes the agent's shape easy to see: structured data goes in,
and a structured decision comes out. The example thresholds and scores are
teaching rules, not investment advice. If ROE is unavailable, the agent
returns `hold` with a neutral score of 50 rather than treating missing data
as a negative signal.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 3
```

This uses the root Python environment and fetches live data, so internet
access is required. Expected output: Junior's signal and score for the
requested ticker, followed by a one-line explanation based on ROE.

## Next

[Lesson 4](../04-second-agent-senior/README.md) combines three metrics in a
second agent and compares its decision with Junior's.
