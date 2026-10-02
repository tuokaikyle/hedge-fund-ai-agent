# Lesson 8: Combining Opinions with an Orchestrator

## Goal

Until now the app has shown two separate opinions per ticker and left you
to decide. This lesson adds an **orchestrator**: one component that runs
every agent and combines their calls into a single final recommendation.
That's the "multi" in multi-agent system.

## What's here

```text
08-orchestrator/
├── pyproject.toml                   # modified: version and description only
└── src/simple_hedge_fund/
    ├── __init__.py
    ├── cli.py                       # modified: calls the orchestrator instead of running agents itself
    ├── orchestrator.py              # new
    ├── output.py                    # modified: takes a TickerAnalysis, prints the final recommendation
    ├── models.py                    # modified: StockSnapshot/AnalystDecision unchanged, FinalRecommendation and TickerAnalysis added
    ├── data/
    │   └── yfinance_service.py      # unchanged from lesson 2
    └── agents/
        ├── __init__.py
        ├── junior.py                # unchanged from lesson 3
        ├── senior.py                # unchanged from lesson 4
        ├── warren_buffett.py        # unchanged from lesson 5
        └── peter_lynch.py           # unchanged from lesson 6
```

- `orchestrator.py`: `SimpleHedgeFundOrchestrator.run(tickers)` fetches a
  snapshot for each ticker, asks every agent for a decision, and combines
  those decisions into one `FinalRecommendation`.
- `models.py`: two new models.
  - `FinalRecommendation` — the combined call: `signal`, `score`, and a
    one-line `summary`.
  - `TickerAnalysis` — everything for one ticker bundled together: the
    snapshot, each analyst's decision, and the final recommendation.
- `cli.py` gets *shorter*. The loop that fetched data and ran agents moved
  into the orchestrator; the CLI now just calls `orchestrator.run(tickers)`
  and prints what comes back.
- `output.py` now takes a `TickerAnalysis` and adds two lines at the
  bottom of each ticker: the final recommendation and its summary.

## How the opinions are combined

The rule is deliberately simple: **average the analysts' scores, then use
the same buy/hold/sell cut-offs the agents use** (70+ is buy, 45+ is hold,
below that is sell).

```python
average_score = round(sum(decision.score for decision in decisions) / len(decisions))
signal = self._score_to_signal(average_score)
```

Coca-Cola (KO) is a good example of why this is more interesting than it
sounds:

```text
Warren Buffett: BUY | score 74/100
Peter Lynch: HOLD | score 60/100
Final recommendation: HOLD | average score 67/100
```

Buffett says buy, but only just (74, where 70 is the cut-off). Lynch says
hold. Averaging the *scores* rather than the *labels* keeps that nuance: a
barely-buy plus a solid hold lands on hold. If both analysts had been
confidently positive — like MSFT, at 93 and 89 — the average stays well
inside buy.

There are plenty of fancier rules (weighting some analysts more than
others, letting one veto, and so on). The real `simple-hedge-fund` project
has each agent report a confidence level and weights by it. We skip that on
purpose — it's an investing refinement, not an agent-system idea. The
architecture lesson is *where* the combining happens, and averaging is
enough to show it.

## Why an orchestrator, and not just more code in the CLI

In lesson 7 the CLI held the list of agents and looped over them. That
worked for printing two opinions, but combining them is a different job,
and the CLI shouldn't grow to do every job. After this lesson each file
knows about one thing:

| File | Knows about |
|---|---|
| `yfinance_service.py` | where the data comes from |
| each agent | how *one* investor judges *one* snapshot |
| `orchestrator.py` | that there are several agents, and how to combine them |
| `output.py` | how the results look on screen |
| `cli.py` | what the user typed |

Notice what *didn't* change: none of the agents. Buffett and Lynch have no
idea they're being combined — each still just takes a snapshot and returns
an `AnalystDecision`. Adding a third persona later would mean writing one
new agent file and adding it to the orchestrator's `self._agents` list.
Nothing else would change.

## Run it

```bash
cd ../08-orchestrator
uv sync
uv run simple-hedge-fund AAPL KO
uv run simple-hedge-fund MSFT --no-explanation
```

Expected output: the same per-ticker blocks as lesson 7, now ending with a
`Final recommendation` line and a one-line summary explaining how it was
reached.

One small difference you may spot: the orchestrator analyzes *all* tickers
before the CLI prints anything, so any yfinance `404` message for a bad
ticker now shows up above the report instead of in the middle of it.

## Next

Lesson 9 *(coming)* defines an LLM interface — a small protocol the agents
can optionally call — without tying the app to any particular provider yet.
