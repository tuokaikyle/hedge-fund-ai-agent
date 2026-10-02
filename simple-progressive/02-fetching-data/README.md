# Lesson 2: Fetching Real Data

## Goal

Get real market data flowing into the `StockSnapshot` contract from lesson 1,
without letting the messiness of a third-party API leak into the rest of the
app.

## What's here

```text
02-fetching-data/
├── pyproject.toml
├── try_it.py
└── src/simple_hedge_fund/
    ├── __init__.py
    ├── models.py                  # unchanged from lesson 1
    └── data/
        ├── __init__.py
        └── yfinance_service.py    # new
```

- `data/yfinance_service.py` defines `YFinanceService`, a thin wrapper around
  [yfinance](https://github.com/ranaroussi/yfinance) with one method:
  `get_snapshot(ticker) -> StockSnapshot`. Since `StockSnapshot` is already
  fully widened as of lesson 1, this service populates the whole snapshot
  in one pass — company info, valuation, profitability, leverage, and
  growth — instead of only fetching a handful of fields.
- `models.py` is untouched. That's the point of widening the model up front
  in lesson 1: this lesson only adds a new file, it never needs to touch
  the shared contract.

Note: `recent_headlines` is left empty here (`yfinance`'s news payload needs
some annoying shape-handling to parse reliably). It stays an easy hook for
a later lesson to fill in if an agent ends up wanting headlines.

## Why wrap the third-party library

`yfinance`'s `Ticker.info` returns a loosely-typed dict with dozens of
inconsistently-named fields (`currentPrice` vs `regularMarketPrice`,
fields that are sometimes missing entirely, etc.). If every agent called
`yfinance` directly, that messiness would spread everywhere.

Instead, `YFinanceService` is the *only* place in the app that knows
`yfinance`'s field names. Everything downstream — agents, the CLI, output
formatting — only ever sees a clean `StockSnapshot`. If we swapped in a
different data provider later, this is the only file that would change.

## A units gotcha, fixed at the boundary

Look closely at the raw numbers yfinance returns and they're not in
consistent units:

| yfinance field | Example (AAPL) | Means |
|---|---|---|
| `returnOnEquity` | `1.49` | 149% — a fraction |
| `profitMargins` | `0.276` | 27.6% — a fraction |
| `revenueGrowth` | `0.164` | 16.4% — a fraction |
| `debtToEquity` | `78.4` | 0.784× — **a percentage** |

Everything is a fraction except debt-to-equity. Left alone, that quirk
would leak into every agent: one threshold would read `>= 0.18` while the
one next to it read `<= 50`, and nothing would tell you why.

So `get_snapshot` divides `debtToEquity` by 100 before building the
snapshot. After that, every ratio in `StockSnapshot` follows one rule —
**fraction-style, where `0.5` means 50% or 0.5×** — and the agents in later
lessons can compare against thresholds like `0.18` (ROE) and `0.5`
(debt-to-equity) without knowing anything about yfinance. This is the
"wrap the messy API" idea in miniature: the service absorbs the quirk so
nothing downstream has to.

## Run it

```bash
cd ../02-fetching-data
uv sync
uv run python try_it.py AAPL
```

Expected output: a `StockSnapshot` populated with Apple's real company name,
sector, valuation, and profitability metrics, printed both as a Python repr
and as JSON.

Requires internet access, since this hits Yahoo Finance's public data feed.

## Next

[Lesson 3](../03-first-agent-junior) writes the first agent: `JuniorAgent`,
a deliberately generic one-metric scorer that reads a `StockSnapshot` and
produces a buy/hold/sell call. No LLM, and no named investor persona yet —
those arrive in lesson 5, once the agent shape is familiar.
