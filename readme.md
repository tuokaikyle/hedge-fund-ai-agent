# Hedge Fund Mini

Inspired by [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund), this project:

- is a simplified version of it
- is a mini educational course
- shows how a small agent system is built
- aims for a gentle learning curve
- shows the core logic only and deliberately keeps it simple
- does not try to be super robust or production-ready
- prevents users from being distracted by content unrelated to the AI agent
- spares users the frustration of code that is repeatedly refactored


This project is for educational and research purposes only. It does not give real investment advice.

Each lesson is a runnable folder. It carries forward the previous lesson's
working code, and the root `run.py` runs every lesson with the same Python
environment. 

## Course plan

**This plan is subject to change.** 

| #   | Lesson                                                                | Main idea                                                                       |
| --- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 1   | [Start](01-start/README.md)                                           | Define the shared `StockSnapshot` data shape.                                   |
| 2   | [Fetching data](02-fetching-data/README.md)                           | Translate yfinance fields into that shape.                                      |
| 3   | [Junior agent](03-junior-agent/README.md)                             | Turn one metric into a structured decision.                                     |
| 4   | [Buffett-style agent](04-warren-buffett-agent/README.md)              | Give one agent its own choice and weighting of metrics.                         |
| 5   | [Lynch-style agent](05-peter-lynch-agent/README.md)                   | Show how the same data can support a different perspective.                     |
| 6   | [Data completeness and confidence](06-data-completeness-and-confidence/README.md) | Separate available inputs from the strength of an agent's rule-based signal. |
| 7   | [Orchestrator](07-orchestrator/README.md)                             | Fetch once and collect Buffett's and Lynch's decisions.                         |
| 8   | [Combine opinions](08-combine-opinions/README.md)                     | Compare equal and confidence-weighted averages of the two decisions.            |
| 9   | [First LLM agent](09-first-llm-agent/README.md)                       | Let Buffett return a typed model score and explanation through an `LLMClient`.  |
| 10  | [Second LLM agent](10-second-llm-agent/README.md)                     | Reuse the same client for Lynch's perspective.                                  |

## Run a built lesson

From the repository root:

```bash
uv sync
uv run python run.py --ticker AAPL --lesson 1
uv run python run.py --ticker AAPL --lesson 2
uv run python run.py --ticker AAPL --lesson 3
uv run python run.py --ticker AAPL --lesson 4
uv run python run.py --ticker AAPL --lesson 5
uv run python run.py --ticker AAPL --lesson 6
uv run python run.py --ticker AAPL --lesson 7
uv run python run.py --ticker AAPL --lesson 8
uv run python run.py --ticker AAPL --lesson 9
uv run python run.py --ticker AAPL --lesson 10
```

## Compare the lessons

Each lesson README marks files changed from the previous lesson. Classes and
functions that a lesson adds to an existing file or changes carry a comment such
as `# changed in lesson 3, 6`, listing every lesson that touched them.
To compare the code directly, run:

```bash
diff -u 08-combine-opinions/agents/warren_buffett.py 09-first-llm-agent/agents/warren_buffett.py
```

## Deliberately left out

To keep the focus on how a small agent system works, the course skips:

- **Configuration layers.** There is no `config.toml`, no CLI overrides such as
  `--model` or `--temperature`, no precedence rules (defaults, environment, file,
  CLI), and no settings object. The model, endpoint, and key come from
  environment variables, read in one place (`LLMClient`). Temperature and
  reasoning effort are fixed in code.
- **LLM abstractions.** There is no `Protocol` or abstract interface for the LLM.
  `LLMClient` is a plain class, because there is only one implementation. It
  talks to one OpenAI-compatible endpoint, with no provider switching. LangChain
  is used only to make the model call.
- **A formatted report.** The final output is the analysis as JSON. There is no
  report renderer.
- **Qualitative inputs.** `StockSnapshot` has fields for headlines and a business
  summary, but nothing fills them, so no agent reads news or company
  descriptions. The agents see only a few numbers.
- **Rich data and real analysis.** The only source is a yfinance snapshot, with no
  financial statements, price history, or insider trades. The scoring rules are
  simple teaching rules. They do not model a moat, intrinsic value, or margin of
  safety, and data completeness and confidence are not calibrated probabilities.
- **Advanced agent machinery.** The orchestrator is a plain loop, with no graph,
  parallel runs, or tool use. Each LLM-backed agent makes one structured model
  call, with no retries, fallback, or multi-step reasoning.
- **The original's wider scope.** There is no portfolio or risk management,
  trading, backtesting, or web interface. There are only two investor agents,
  Buffett and Lynch, and they analyze one ticker at a time.
- **Production concerns.** There is no caching, rate limiting, logging, or
  automated tests, and little error handling. Missing data lowers a score instead
  of stopping the run.
