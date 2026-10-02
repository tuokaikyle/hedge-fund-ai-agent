# Lesson 3: First Agent (Junior), Pure Heuristics

## Goal

Write the smallest possible "agent" and see that at its core, an agent is
just a deterministic function: data in, decision out. No LLM, no prompt, no
API call, and — for this lesson — no real investor persona either. That
comes later; here we isolate the shape.

## What's here

```text
03-first-agent-junior/
├── pyproject.toml
├── try_it.py
└── src/simple_hedge_fund/
    ├── __init__.py
    ├── models.py                    # modified: StockSnapshot unchanged, AnalystDecision added
    ├── data/
    │   └── yfinance_service.py      # unchanged from lesson 2
    └── agents/
        ├── __init__.py
        └── junior.py                # new
```

- `models.py`: `StockSnapshot` is untouched (see lesson 1 for why it's
  already at its full shape). A new `AnalystDecision` model is added — the
  shape every agent's output will use, from Junior all the way through the
  real personas in later lessons.
- `agents/junior.py`: `JuniorAgent.analyze(snapshot)` looks at exactly
  **one** field — return on equity (ROE) — and maps it to a score and a
  `buy` / `hold` / `sell` signal.


## Why "Junior", not Warren Buffett, first

It's tempting to jump straight to a named persona like Warren Buffett. But
a realistic persona agent usually combines several metrics with
persona-specific weighting and framing — which mixes two things a beginner
has to learn at once: *the mechanical shape of an agent* (read structured
input, produce structured output) and *the domain judgment* (what makes a
"Buffett-style" view). `JuniorAgent` deliberately strips away the domain
judgment and keeps only the shape:

```python
def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
    ...
```

Every agent in this course — Junior, Senior in lesson 4, and Warren
Buffett / Peter Lynch starting lesson 5 — implements this exact same
method signature. Once that shape feels obvious, adding domain logic on
top of it is much easier to follow.

Junior still uses a **real** field from `StockSnapshot` (ROE), not an
invented one — the point isn't to fake a rule for its own sake, it's to
practice the one-metric-in, one-decision-out pattern on data you already
know how to fetch.

## Run it

```bash
cd ../03-first-agent-junior
uv sync
uv run python try_it.py AAPL
```

Expected output: a BUY/HOLD/SELL call for the ticker with a one-line
reasoning string based on ROE alone.

## Next

[Lesson 4](../04-second-agent-senior) introduces `SeniorAgent`, which uses
the same shape but combines a few metrics into one score — the natural next
step before meeting real personas.
