# Lesson 6: Second Real Persona, Peter Lynch

## Goal

Add a second named investor persona and see two agents with the exact same
mechanical shape reach different conclusions — not because one is more
sophisticated than the other (that was lesson 5's point), but because they
value different things. That's the real point of a multi-agent system:
independent perspectives, not one "smarter" answer.

## What's here

```text
06-peter-lynch-agent/
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
        ├── warren_buffett.py        # unchanged from lesson 5
        └── peter_lynch.py           # new
```

- `agents/peter_lynch.py`: `PeterLynchAgent.analyze(snapshot)` scores three
  sub-factors — revenue growth, the PEG ratio, and earnings growth —
  weighted out of 35/40/25, sums them, and maps the total to a signal.
- Every other file is an unchanged carry-forward. Adding a second persona
  required touching exactly one new file, which is the whole point of
  having agreed on the `analyze(snapshot) -> AnalystDecision` shape back in
  lesson 3.

## Buffett vs. Lynch: same shape, different philosophy

Both agents implement:

```python
def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
```

But they read almost entirely different fields off the same
`StockSnapshot`, because they're chasing different things:

| | Warren Buffett (lesson 5) | Peter Lynch (this lesson) |
|---|---|---|
| Philosophy | Quality at a fair price | Growth at a reasonable price (GARP) |
| Rewards | High ROE, low debt, strong margins | Strong revenue/earnings growth |
| Views a high PE as | A red flag, unless the business is exceptional | Acceptable, if growth justifies it |
| Signature metric | Trailing PE on its own | **PEG ratio** — PE divided by growth rate |

The PEG ratio is the clearest illustration of "same data, different
lens": Buffett's agent treats a high trailing PE as expensive, full stop.
Lynch's agent asks the follow-up question a growth investor would ask —
*expensive relative to what?* — by dividing that same PE by the earnings
growth rate. A PE of 35 looks alarming to Buffett; to Lynch, it's a
non-issue if earnings are growing at 35%+ a year.

## A note on scope

This is a simplified, three-factor Lynch score. The real
`simple-hedge-fund` project's philosophy also considers simpler,
easy-to-understand businesses and analyst sentiment. Keeping this lesson to
growth, PEG, and earnings growth keeps the file focused on Lynch's most
distinctive idea (paying for growth, not just avoiding expense) rather than
trying to capture every nuance of his investing style.

## Run it

```bash
cd ../06-peter-lynch-agent
uv sync
uv run python try_it.py AAPL
```

Try a high-growth, high-PE ticker too (e.g. a smaller tech company) to see
Buffett and Lynch disagree more sharply than they do on a mature company
like AAPL.

## Next

[Lesson 7](../07-cli-and-output) wraps the app in a real command-line
interface with proper argument parsing and readable terminal output,
instead of a one-off script that always runs every agent on a hardcoded
ticker.
