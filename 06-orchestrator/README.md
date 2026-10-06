# Lesson 6: Orchestrator

## Goal

Move the shared fetch and agent loop into an orchestrator that returns Buffett's
and Lynch's independent decisions for one stock.

## What's here

```text
06-orchestrator/
├── README.md
├── lesson.py                      # changed: prints the collected result
├── models.py                      # changed: adds TickerAnalysis
├── orchestrator.py                # new
├── yfinance_service.py
└── agents/
    ├── __init__.py
    ├── peter_lynch.py
    └── warren_buffett.py
```

## New idea

Junior taught the agent interface and scoring steps. It does not take part in
decision making from this lesson onward, so `junior.py` is gone. The course
follows the two investor perspectives instead.

`HedgeFundOrchestrator.run(ticker)` fetches one `StockSnapshot`, passes it to
Buffett and Lynch, and collects their `AnalystDecision` objects in a
`TickerAnalysis`. The agents still know nothing about one another. A later
lesson can combine their calls.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 6
```

This fetches live data and needs internet access. Expected output: JSON with
one `snapshot` and two entries in `analyst_decisions`, each containing its
signal, score, and reasoning. Values depend on the data Yahoo returns.
