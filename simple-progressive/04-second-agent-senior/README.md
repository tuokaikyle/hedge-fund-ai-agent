# Lesson 4: Second Agent (Senior), Combining Metrics

## Goal

Take the exact same agent shape from lesson 3 and add the one thing Junior
was missing: combining more than one metric into a single score. Still no
real persona, still no LLM — just the next small step in complexity.

## What's here

```text
04-second-agent-senior/
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
        └── senior.py                # new
```

- `agents/junior.py` is carried forward unchanged, so you can compare it
  side by side with `senior.py` and see exactly what got added.
- `agents/senior.py`: `SeniorAgent.analyze(snapshot)` scores three real
  metrics — ROE, debt-to-equity, and profit margin — each out of a
  sub-total (40/30/30), sums them into one 0-100 score, and maps that to a
  signal. Same method signature as `JuniorAgent`.

## What actually changed from Junior to Senior

Nothing about the *shape* changed:

```python
def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
```

What changed is that Senior scores three things instead of one, and adds
them together instead of returning a single sub-score directly. That's the
whole idea of this lesson: an agent's sophistication comes from *how many
things it looks at and how it weighs them*, not from a different interface
or a fundamentally different kind of code. This is exactly the pattern
Warren Buffett and Peter Lynch (lessons 5-6) use — more metrics, more
persona-specific framing in the reasoning text, but the same
`analyze(snapshot) -> AnalystDecision` shape and the same
"sub-score-then-sum" structure.

## Run it

```bash
cd ../04-second-agent-senior
uv sync
uv run python try_it.py AAPL
```

Expected output: Junior's single-metric call, followed by Senior's
three-metric call, for the same ticker — worth comparing, since they can
disagree.

## Next

[Lesson 5](../05-warren-buffett-agent) introduces the first real persona:
a Warren Buffett agent. It uses the same shape you've now built twice, so
this lesson is where that pattern should already feel familiar — the new
part is entirely about Buffett-specific investing logic and framing.
