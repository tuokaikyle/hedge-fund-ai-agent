# Lesson 15: Complete report

## Goal

Show the completed analysis as a readable terminal report.

## What's here

```text
15-complete-report/
├── README.md
├── output.py                      # new: renders the analysis as text
├── lesson.py                      # changed: prints the report instead of JSON
├── config.py                      # unchanged from lesson 14
├── config.toml                    # unchanged from lesson 14
├── models.py                      # unchanged from lesson 14
├── orchestrator.py                # unchanged from lesson 14
├── yfinance_service.py            # unchanged from lesson 14
├── agents/
│   ├── __init__.py                # unchanged from lesson 14
│   ├── peter_lynch.py             # unchanged from lesson 14
│   └── warren_buffett.py          # unchanged from lesson 14
├── llm/
│   ├── __init__.py                # unchanged from lesson 14
│   ├── interface.py               # unchanged from lesson 14
│   └── openai_client.py           # unchanged from lesson 14
└── utils/
    ├── __init__.py                # unchanged from lesson 14
    ├── confidence.py              # unchanged from lesson 14
    └── data_completeness.py       # unchanged from lesson 14
```

## New idea

The orchestrator still returns a `TickerAnalysis`. `render_report()` takes
that object and returns text; `lesson.py` prints it. Keeping presentation in
`output.py` lets us change how results look without changing agent logic.

The report shows the company, price, and metrics used by the agents, then each
agent's signal, score, data completeness, confidence, and model reasoning.
Ratios such as return on equity are formatted as percentages; missing snapshot
metrics appear as `n/a`. Reasoning wraps across lines for easier reading.

The final section shows both the equal and confidence-weighted averages.
The weighted signal is the final recommendation, as in previous lessons.
Completeness measures available inputs and confidence measures rule support;
neither is a measured probability of being correct.

This lesson changes the terminal output from JSON to text. It uses the same
settings and analysis logic as lesson 14 and makes no extra model calls.
The CLI overrides from lesson 14 still work.

## Run

With `LLM_API_KEY` set in the root `.env` (and the model and endpoint set for
your provider), run from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 15
```

Expected output has this shape (values and reasoning will vary):

```text
Hedge Fund Mini
===============
Ticker: AAPL | Apple Inc.
Sector: Technology
Price: ...

Snapshot metrics
  Trailing P/E: ...
  ...

Agent decisions
  Warren Buffett: BUY | score .../100
  Data completeness: ...% | confidence: ...%
  Reasoning: ...

  Peter Lynch: BUY | score .../100
  Data completeness: ...% | confidence: ...%
  Reasoning: ...

Combined result
  Equal average: BUY | score .../100
  Confidence-weighted average: BUY | score .../100
  Final recommendation: BUY

Data completeness measures input coverage; confidence measures rule support.
Neither is a measured probability of being correct.
```

The run fetches live Yahoo data and makes two model calls. Signals can be
`BUY`, `HOLD`, or `SELL`.
