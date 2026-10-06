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

## Branches

- **`v0.3`** has 9 lessons and aims to provide a gentle learning curve.
- **`v0.2`** has 15 lessons, with a more gradual learning curve than `v0.3`
  and slightly more content.

## Course plan

**This plan is subject to change.** 

| #   | Lesson                                                                | Main idea                                                                       |
| --- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 1   | [Start](01-start/README.md)                                           | Define the shared `StockSnapshot` data shape.                                   |
| 2   | [Fetching data](02-fetching-data/README.md)                           | Translate yfinance fields into that shape.                                      |
| 3   | [Junior agent](03-junior-agent/README.md)                             | Turn one metric into a structured decision.                                     |
| 4   | [Buffett-style agent](04-warren-buffett-agent/README.md)              | Give one agent its own choice and weighting of metrics.                         |
| 5   | [Lynch-style agent](05-peter-lynch-agent/README.md)                   | Show how the same data can support a different perspective.                     |
| 6   | [Orchestrator](06-orchestrator/README.md)                             | Fetch once and collect Buffett's and Lynch's decisions.                         |
| 7   | [Combine opinions](07-combine-opinions/README.md)                     | Average the two agents' scores to produce one final signal.                     |
| 8   | [First LLM agent](08-first-llm-agent/README.md)                       | Let an LLM explain Buffett's rule-based score through an `LLMClient`.           |
| 9   | [Second LLM agent](09-second-llm-agent/README.md)                     | Reuse the same client and response shape for Lynch's explanation.              |

## Code added and learning difficulty

Line counts compare each lesson with the previous one and include added Python
code lines, excluding blank lines, comments, docstrings, and unchanged copied
code. Replacement lines count as additions; the shared `run.py` is excluded.

Difficulty estimates assume basic Python knowledge: **1 = easy; 5 = demanding**.

| # | Lesson | Lines added | Difficulty | Main learning challenge |
|---|---|---:|---|---|
| 1 | Start | 29 | 2/5 | Pydantic models, type hints, and optional fields |
| 2 | Fetching data | 31 | 2/5 | Mapping API fields into a consistent data shape |
| 3 | Junior agent | 39 | 2/5 | Turning a metric into a score and structured decision |
| 4 | Buffett-style agent | 62 | 3/5 | Combining several scoring functions and weights |
| 5 | Lynch-style agent | 48 | 2/5 | Reusing the agent pattern; understanding the PEG calculation |
| 6 | Orchestrator | 18 | 2/5 | Moving fetching and the agent loop into one coordinating class |
| 7 | Combine opinions | 20 | 2/5 | Averaging scores and producing a final recommendation |
| 8 | First LLM agent | 63 | 4/5 | Client setup, prompts, structured output, and passing dependencies |
| 9 | Second LLM agent | 29 | 2/5 | Applying the established LLM pattern to another agent |

Lesson 6 also removes 38 code lines, so its net change is −20, mainly from
removing Junior and replacing the previous lesson's loop.

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
```

## Compare the lessons

Each lesson README marks files changed from the previous lesson. Classes and
functions that a lesson adds to an existing file or changes carry a comment such
as `# changed in lesson 6, 7`, listing every lesson that touched them.
To compare the code directly, run:

```bash
diff -u 07-combine-opinions/agents/warren_buffett.py 08-first-llm-agent/agents/warren_buffett.py
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
- **Confidence measures and weighted aggregation.** The final score is a plain
  average of the two analyst scores. The course does not estimate confidence or
  assign different weights to the agents.
- **Rich data and real analysis.** The only source is a yfinance snapshot, with no
  financial statements, price history, or insider trades. The scoring rules are
  simple teaching rules. They do not model a moat, intrinsic value, or margin of
  safety.
- **Advanced agent machinery.** The orchestrator is a plain loop, with no graph,
  parallel runs, or tool use. Each LLM-backed agent makes one structured model
  call, with no retries, fallback, or multi-step reasoning.
- **The original's wider scope.** There is no portfolio or risk management,
  trading, backtesting, or web interface. There are only two investor agents,
  Buffett and Lynch, and they analyze one ticker at a time.
- **Production concerns.** There is no caching, rate limiting, logging, or
  automated tests, and little error handling. Missing metrics receive partial
  points and are noted in the explanation instead of stopping the run.
