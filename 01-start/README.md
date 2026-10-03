# Lesson 1: Start

## Goal

Before we fetch data or build an agent, we need one clear shape for the stock
information that will move between them. That shape is `StockSnapshot`.

## What's here

```text
01-start/
├── README.md
├── models.py
└── lesson.py
```

- `models.py` defines `StockSnapshot` with Pydantic. `ticker` and
  `company_name` are required; the other fields may be missing.
- `lesson.py` creates a small example and prints it as JSON.

## Why start here

The model includes fields later lessons will use, but this lesson only needs
to show how to create one snapshot. Later code can use the same data shape.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 1
```

This uses the root Python environment. Lesson 1 has no `pyproject.toml` or
`uv.lock` of its own. The example uses made-up data and needs no API key or
internet connection.

Expected output: a JSON snapshot with the ticker you entered and the example
company data.

## Next

[Lesson 2](../02-fetching-data/README.md) fetches real data and puts it into
a `StockSnapshot`.
