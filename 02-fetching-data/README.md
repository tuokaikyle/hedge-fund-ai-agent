# Lesson 2: Fetching data

## Goal

Lesson 1 created a `StockSnapshot` by hand. This lesson fills one from live
market data using yfinance.

## What's here

```text
02-fetching-data/
├── README.md
├── lesson.py             # changed from lesson 1
├── models.py             # unchanged from lesson 1
└── yfinance_service.py   # new
```

`YFinanceService` asks yfinance for a ticker's `info` dictionary and maps a
few keys into the snapshot: company name, sector, current price, market cap,
and return on equity. The other snapshot fields remain empty for now. The
printed JSON omits fields set to `None` so the fetched values are easy to see.

## Why use a service

Keeping the yfinance field names in `yfinance_service.py` gives later code
one consistent `StockSnapshot` to use.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 2
```

This uses the same root Python environment as lesson 1. It needs internet
access. The values returned by Yahoo Finance can change between runs.

Expected output: a JSON snapshot with the requested ticker and the company
fields Yahoo Finance returned.

## Next

[Lesson 3](../03-first-agent-junior/README.md) reads this `StockSnapshot` to
make a simple decision from ROE.
