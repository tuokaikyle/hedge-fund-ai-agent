# Lesson 5: First Real Persona, Warren Buffett

## Goal

Meet the first named investor persona. By now the `analyze(snapshot) ->
AnalystDecision` shape (lesson 3) and the "score sub-factors, sum them"
pattern (lesson 4) should feel familiar — this lesson is entirely about
persona-specific domain logic: which metrics a "Buffett style" investor
actually cares about, and how they're weighted and framed.

## What's here

```text
05-warren-buffett-agent/
├── pyproject.toml
├── try_it.py
└── src/simple_hedge_fund/
    ├── __init__.py
    ├── models.py                    # unchanged from lesson 3
    ├── data/
    │   └── yfinance_service.py      # unchanged from lesson 2
    └── agents/
        ├── __init__.py
        ├── junior.py                # unchanged from lesson 3
        ├── senior.py                # unchanged from lesson 4
        └── warren_buffett.py        # new
```

- `agents/warren_buffett.py`: `WarrenBuffettAgent.analyze(snapshot)` scores
  four sub-factors — ROE, debt-to-equity, margins, and a simple valuation
  check (trailing PE) — weighted out of 30/25/25/20, sums them into a
  0-100 score, and maps that to a signal.
- `junior.py` and `senior.py` are kept around unchanged. Nothing about
  Warren Buffett required touching them — they're here so you can compare
  three agents that all implement the same shape with different
  sophistication.

## What's actually new here

The method signature is identical to `JuniorAgent` and `SeniorAgent`:

```python
def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
```

What's new is entirely about investing judgment:

- **Which metrics matter.** A Buffett-style investor cares about capital
  efficiency (ROE), balance-sheet discipline (debt-to-equity), durable
  profitability (margins), and paying a fair price (a simple PE check).
  Senior's three metrics were arbitrary teaching choices; Buffett's four
  are a deliberate reflection of a specific investing philosophy.
- **How they're weighted.** ROE and leverage get the biggest share of the
  score (30 and 25 points) because capital efficiency and balance-sheet
  safety are central to the Buffett profile — not because they were
  convenient to code.
- **How the reasoning reads.** The `reasoning` string is framed in
  Buffett's own language ("quality, leverage, and valuation") rather than
  generic score commentary.

This split — shape learned once, judgment layered on per persona — is
exactly what makes it straightforward to add a second, differently-weighted
persona next.

## A note on scope

This is a simplified, four-factor Buffett score. The real
`simple-hedge-fund` project also weighs liquidity (current ratio) and
blends in analyst price targets for a fuller valuation picture. Keeping
this lesson to four factors keeps the file focused on the *pattern*
(persona-specific metrics and weights) rather than an exhaustive scoring
model — a later lesson revisits robustness once every core idea is in
place.

## Run it

```bash
cd ../05-warren-buffett-agent
uv sync
uv run python try_it.py AAPL
```

Expected output: Junior's, Senior's, and Warren Buffett's calls for the
same ticker, one after another — worth comparing, since a more
sophisticated agent can reach a different conclusion than a simpler one.

## Next

[Lesson 6](../06-peter-lynch-agent) introduces a second real persona, Peter
Lynch, whose investing philosophy — growth at a reasonable price — leads to
different metrics and weights than Buffett's, using the exact same shape.
