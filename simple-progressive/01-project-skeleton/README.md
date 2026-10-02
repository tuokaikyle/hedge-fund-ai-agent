# Lesson 1: Project Skeleton + the Data Contract

## Goal

Before writing any agent logic or fetching any data, define the shape of the
data everything else will pass around. This is the contract every later
lesson builds on.

## What's here

```text
01-project-skeleton/
├── pyproject.toml
├── try_it.py
└── src/simple_hedge_fund/
    ├── __init__.py
    └── models.py
```

- `models.py` defines `StockSnapshot`, a [Pydantic](https://docs.pydantic.dev/)
  model with the full set of fields the finished app ever uses: company
  info, valuation, profitability, leverage, growth, and recent headlines.
  Only `ticker` and `company_name` are required — everything else is
  optional, since no single lesson (or even the real yfinance API) fills in
  all of it at once.
- `try_it.py` constructs a snapshot using just a few fields and prints it,
  then shows what happens when a required field is missing.

## Why the model is fully widened here, not grown gradually

You might expect to start with 3-4 fields and add more as later lessons
need them. We do the opposite here on purpose: `StockSnapshot` is defined
at its full, final shape from lesson 1. That means:

- later lessons never need to revisit this file to add a field — they just
  read more of what's already there
- every lesson's `models.py` for `StockSnapshot` is identical, so there's
  nothing to diff or reconcile as new agents are introduced
- it reflects how a shared contract is usually designed in practice once
  you know the target shape: agree on the full data shape once, then let
  each consumer opt into the subset it needs

## Why Pydantic, and why first

- **Validation for free.** If a field is missing or the wrong type, you get
  an error immediately at construction time, not a confusing `KeyError`
  three functions later.
- **A single source of truth.** Every later lesson (data fetching, agents,
  the CLI, output formatting) will import `StockSnapshot` instead of passing
  around raw dicts. Defining it first means every other file has something
  concrete to code against.
- **Self-documenting.** Anyone reading `models.py` can see exactly what data
  the app works with, without tracing through fetch/parse logic.

## Run it

```bash
cd ../01-project-skeleton
uv sync   # or: pip install -e .
uv run python try_it.py
```

Expected output: a printed `StockSnapshot`, its JSON form, and a validation
error demonstrating that `ticker` is required.

## Next

[Lesson 2](../02-fetching-data) will fetch real data from yfinance and map it
onto this same `StockSnapshot` model.
