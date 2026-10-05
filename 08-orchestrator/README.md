# Lesson 8: Run the agents together

## Goal

Move the shared fetch and agent loop into an orchestrator that returns all four
independent decisions for one stock.

## What's here

```text
08-orchestrator/
├── README.md
├── lesson.py                      # changed: prints the collected result
├── models.py                      # changed: adds TickerAnalysis
├── orchestrator.py                # new
├── yfinance_service.py            # unchanged from lesson 7
├── agents/
│   ├── __init__.py                # unchanged from lesson 7
│   ├── junior.py                  # unchanged from lesson 7
│   ├── peter_lynch.py             # unchanged from lesson 7
│   ├── senior.py                  # unchanged from lesson 7
│   └── warren_buffett.py          # unchanged from lesson 7
└── utils/
    ├── __init__.py                # unchanged from lesson 7
    ├── confidence.py              # unchanged from lesson 7
    └── data_completeness.py       # unchanged from lesson 7
```

## New idea

`HedgeFundOrchestrator.run(ticker)` fetches one `StockSnapshot`, passes it to
each agent, and collects their `AnalystDecision` objects in a
`TickerAnalysis`. The agents still know nothing about one another. This
lesson collects their opinions without combining them; a later lesson can
decide how to make one final call.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 8
```

This fetches live data and needs internet access. Expected output: JSON with
one `snapshot` and four entries in `analyst_decisions`, each containing its
signal, score, data completeness, confidence, and reasoning. Values depend on
the data Yahoo returns.
