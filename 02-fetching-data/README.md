# Lesson 2: Fetching data

## Goal

Lesson 1 created a `StockSnapshot` by hand. This lesson fills one from live
market data using yfinance.

## What's here

```text
02-fetching-data/
├── README.md
├── lesson.py                      # changed from lesson 1
├── models.py
└── yfinance_service.py            # new
```

`YFinanceService` asks yfinance for a ticker's `info` dictionary and maps its
keys into the snapshot. It fills every field the later agents will read:
company name, sector, price, market cap, return on equity, debt-to-equity,
profit and operating margins, trailing P/E, and revenue and earnings growth.
This is the only version of the service in the course, so later lessons never
change it. Yahoo reports debt-to-equity as a percentage, so the service divides
it by 100 to match the other ratios. The printed JSON omits fields set to
`None` so the fetched values are easy to see.

## Why use a service

Keeping the yfinance field names in `yfinance_service.py` gives every agent
one consistent `StockSnapshot` to use, and no agent needs to know about Yahoo.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 2
```

This uses the same root Python environment as lesson 1. It needs internet
access. The values returned by Yahoo Finance can change between runs.

Expected output: a JSON snapshot with the requested ticker and the company
fields Yahoo Finance returned.
