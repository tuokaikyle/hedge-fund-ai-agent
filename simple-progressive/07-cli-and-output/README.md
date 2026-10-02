# Lesson 7: A Real CLI

## Goal

Replace the one-off `try_it.py` script with a real command you can run on
any tickers you like:

```bash
uv run simple-hedge-fund AAPL MSFT KO
```

No new agent logic in this lesson. The agents are the same ones from
lessons 5-6 — this lesson is only about the *front door* of the app: how
arguments come in and how results go out.

## What's here

```text
07-cli-and-output/
├── pyproject.toml                   # modified: adds typer and a [project.scripts] entry
└── src/simple_hedge_fund/
    ├── __init__.py
    ├── cli.py                       # new
    ├── output.py                    # new
    ├── models.py                    # unchanged from lesson 3
    ├── data/
    │   └── yfinance_service.py      # unchanged from lesson 2
    └── agents/
        ├── __init__.py
        ├── junior.py                # unchanged from lesson 3
        ├── senior.py                # unchanged from lesson 4
        ├── warren_buffett.py        # unchanged from lesson 5
        └── peter_lynch.py           # unchanged from lesson 6
```

- `cli.py`: the command itself. It takes one or more tickers plus a
  `--explanation/--no-explanation` flag, fetches a snapshot for each ticker,
  runs the Warren Buffett and Peter Lynch agents on it, and prints the
  result.
- `output.py`: one function, `render_analysis(snapshot, decisions, ...)`,
  that turns the data into a readable block of text.
- `pyproject.toml`: adds [Typer](https://typer.tiangolo.com/) as a
  dependency, and a `[project.scripts]` entry that tells `uv` to install a
  `simple-hedge-fund` command pointing at `cli.py`'s `app()` function.
- `try_it.py` is gone — the CLI replaces it.

## How Typer turns a function into a command

You write an ordinary Python function with type hints:

```python
def main(
    tickers: list[str] = typer.Argument(..., help="Ticker symbols to analyze, for example AAPL MSFT."),
    explanation: bool = typer.Option(True, "--explanation/--no-explanation", help="Show each analyst's key points."),
) -> None:
```

Typer reads those hints and builds the command-line parser for you:

- `tickers: list[str]` becomes "one or more positional arguments". The
  `...` means *required* — run the command with no tickers and you get a
  clear error instead of a crash.
- `explanation: bool` with `"--explanation/--no-explanation"` becomes an on/off
  flag, on by default.
- The `help=` strings and the function's docstring become the `--help`
  page, for free.

Then `app()` just calls `typer.run(main)`, and `pyproject.toml` points the
`simple-hedge-fund` command at `app()`.

## Why output lives in its own file

It would be shorter to `print(...)` straight from inside the loop in
`cli.py`. Splitting the formatting out keeps each file doing one job:

- `cli.py` decides **what to run** — which tickers, which agents, which
  flags.
- `output.py` decides **what it looks like** — and it only *returns* a
  string, it never prints.

That split pays off soon. Lesson 8 adds an orchestrator that combines the
agents into one final call; that'll be a change to what `cli.py` runs and
a couple of extra lines in `output.py`, without the two getting tangled
together.

## Why only Buffett and Lynch

`JuniorAgent` and `SeniorAgent` were training wheels for learning the agent
shape in lessons 3-4. The CLI is the "real" app, so it runs the two real
personas — the same two the finished `simple-hedge-fund` project uses. The
Junior and Senior files are still in the folder, unchanged, if you want to
compare them; nothing imports them anymore.

Notice how the CLI calls the agents:

```python
agents = [WarrenBuffettAgent(), PeterLynchAgent()]
decisions = [agent.analyze(snapshot) for agent in agents]
```

The loop doesn't care *which* agent it's holding — only that each one has
an `analyze(snapshot)` method returning an `AnalystDecision`. That's the
shape from lesson 3 paying off, and it's exactly what the orchestrator in
lesson 8 builds on.

## Run it

```bash
cd ../07-cli-and-output
uv sync
uv run simple-hedge-fund --help
uv run simple-hedge-fund AAPL MSFT
uv run simple-hedge-fund KO --no-explanation
```

Expected output: for each ticker, a short block with its price, sector, and
key metrics, then one line per analyst (`BUY` / `HOLD` / `SELL` and a
score). With `--explanation` (the default), each analyst's key points are
listed underneath.

A ticker that doesn't exist won't crash the run: yfinance prints a `404`
message, the snapshot comes back mostly empty, and the agents score it as
"unavailable" — you'll see `n/a` for every metric.

## Next

[Lesson 8](../08-orchestrator) adds an orchestrator that combines the Buffett and
Lynch calls into one final recommendation per ticker — the "multi" in
multi-agent system.
