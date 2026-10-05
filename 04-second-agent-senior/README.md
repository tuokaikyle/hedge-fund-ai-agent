# Lesson 4: Second agent

## Goal

Compare Junior's one-metric decision with a Senior agent that combines three
metrics into one score. Both agents use the same `analyze(snapshot)` input and
return an `AnalystDecision`.

## What's here

```text
04-second-agent-senior/
├── README.md
├── lesson.py                      # changed: runs both agents
├── models.py                      # unchanged from lesson 3
├── yfinance_service.py            # changed: adds debt-to-equity and profit margin
└── agents/
    ├── __init__.py                # unchanged from lesson 3
    ├── junior.py                  # unchanged from lesson 3
    └── senior.py                  # new
```

Senior scores ROE out of 40, debt-to-equity out of 30, and profit margin out of
30. It adds the three scores and uses the same buy/hold/sell thresholds as
Junior. Missing metrics receive partial points. Yahoo reports debt-to-equity
as a percentage, so the service divides it by 100 before Senior compares it
with ratio thresholds.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 4
```

This fetches live data and needs internet access. Expected output: Junior's
signal, score, and ROE explanation, followed by Senior's signal, score, and
three-metric explanation. Their calls may differ.

## Next

[Lesson 5](../05-warren-buffett-agent/README.md) gives an agent its first
investor perspective and a simple price check.
