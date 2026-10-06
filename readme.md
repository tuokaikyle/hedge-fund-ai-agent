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

| #   | Lesson                                                                            | Main idea                                                                                |
| --- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 1   | [Start](01-start/README.md)                                                       | Define the shared `StockSnapshot` data shape.                                            |
| 2   | [Fetching data](02-fetching-data/README.md)                                       | Translate yfinance fields into that shape.                                               |
| 3   | [First agent: Junior](03-first-agent-junior/README.md)                            | Turn one metric into a structured decision.                                              |
| 4   | [Second agent: Senior](04-second-agent-senior/README.md)                          | Combine several metrics while keeping the same agent interface.                          |
| 5   | [Buffett-style agent](05-warren-buffett-agent/README.md)                          | Give one agent its own choice and weighting of metrics.                                  |
| 6   | [Lynch-style agent](06-peter-lynch-agent/README.md)                               | Show how the same data can support a different perspective.                              |
| 7   | [Data Completeness and Confidence](07-data-completeness-and-confidence/README.md) | Separate available inputs from the strength of an agent's final rule-based signal.       |
| 8   | [Run the investor agents together](08-orchestrator/README.md)                     | Have an orchestrator fetch once and collect Buffett's and Lynch's decisions.             |
| 9   | [Combine opinions](09-combine-opinions/README.md)                                 | Compare equal and confidence-weighted averages of the two decisions.                     |
| 10  | [First LLM decision](10-first-llm-call/README.md)                                 | Let Buffett return a typed model score and explanation for the orchestrator to combine.  |
| 11  | [Shared LLM interface](11-shared-llm-interface/README.md)                         | Move model-specific code behind a small reusable interface.                              |
| 12  | [Second LLM-backed agent](12-second-llm-backed-agent/README.md)                   | Reuse the interface for the other investor perspective.                                  |
| 13  | [Runtime settings](13-runtime-settings/README.md)                                 | Collect model settings in one config object.                                             |
| 14  | [Configuration precedence](14-configuration-precedence/README.md)                 | Add a TOML file and explain how defaults, environment, file, and CLI values combine.     |
| 15  | [Complete report](15-complete-report/README.md)                                   | Render agent decisions, the final result, completeness, confidence, and model reasoning. |

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
uv run python run.py --ticker AAPL --lesson 11
uv run python run.py --ticker AAPL --lesson 12
uv run python run.py --ticker AAPL --lesson 13
uv run python run.py --ticker AAPL --lesson 14 --temperature 0
uv run python run.py --ticker AAPL --lesson 15
```

## Compare the lessons

Each lesson README marks files changed from the previous lesson. Some classes
and functions also have comments marking where they were introduced or changed.
To compare the code directly, run:

```bash
diff -u 09-combine-opinions/agents/warren_buffett.py 10-first-llm-call/agents/warren_buffett.py
```
