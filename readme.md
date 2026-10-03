# Hedge Fund Mini

A small course on building an agent system one step at a time. The agents use
simple stock rules so the focus stays on data flow, agent interfaces, and
coordination. This is a learning project, not investment advice.

Each lesson is a runnable folder. It carries forward the previous lesson's
working code, and the root `run.py` runs every lesson with the same Python
environment. Comparing adjacent folders shows what changed.

## Course plan

**This plan is subject to change.** Lessons 1–6 are built; the remaining
lessons are proposed. We can split, merge, or reorder them as we learn what
makes each idea easiest to understand. Each planned lesson should add one
main idea and still run through `run.py`.

| # | Lesson | Main idea |
|---|---|---|
| 1 | [Start](01-start/README.md) | Define the shared `StockSnapshot` data shape. |
| 2 | [Fetching data](02-fetching-data/README.md) | Translate yfinance fields into that shape. |
| 3 | [First agent: Junior](03-first-agent-junior/README.md) | Turn one metric into a structured decision. |
| 4 | [Second agent: Senior](04-second-agent-senior/README.md) | Combine several metrics while keeping the same agent interface. |
| 5 | [Buffett-style agent](05-warren-buffett-agent/README.md) | Give one agent its own choice and weighting of metrics. |
| 6 | [Lynch-style agent](06-peter-lynch-agent/README.md) | Show how the same data can support a different perspective. |
| 7 | Evidence and confidence *(planned)* | Report how much of each agent's expected data was available, separately from its stock score. |
| 8 | Run the agents together *(planned)* | Have an orchestrator fetch once and collect independent decisions. |
| 9 | Combine opinions *(planned)* | Compare a plain average with a confidence-weighted final decision. |
| 10 | Readable output *(planned)* | Render the collected decisions and final result as a clear report. |
| 11 | First optional LLM call *(planned)* | Let one agent use a model to explain its heuristic decision. |
| 12 | Structured LLM output *(planned)* | Ask for a typed response that fits the agent's output shape. |
| 13 | Heuristic fallback *(planned)* | Keep the agent useful when an LLM is unavailable or fails. |
| 14 | Shared LLM interface *(planned)* | Move model-specific code behind a small reusable interface. |
| 15 | Second LLM-backed agent *(planned)* | Reuse the interface for the other investor perspective. |
| 16 | Runtime settings *(planned)* | Collect model and mode settings in one config object. |
| 17 | Configuration precedence *(planned)* | Add a TOML file and explain how defaults, environment, file, and CLI values combine. |
| 18 | Complete report *(planned)* | Bring both agents, the final decision, confidence, and LLM status into one run. |

In lesson 7, **confidence means evidence coverage**, not the probability that
a recommendation is correct. This keeps it distinct from a stock score and
gives lesson 9 a clear reason to weight opinions differently.

The LLM lessons start with one useful call before introducing structured
responses, fallback behavior, and a shared provider interface. Configuration
comes after the model path works, so each step has a concrete purpose.

## Run a built lesson

From the repository root:

```bash
uv sync
uv run python run.py --course 1 --ticker AAPL
uv run python run.py --course 2 --ticker AAPL
uv run python run.py --course 3 --ticker AAPL
uv run python run.py --course 4 --ticker AAPL
uv run python run.py --course 5 --ticker AAPL
uv run python run.py --course 6 --ticker AAPL
```

Lessons 2–6 fetch live stock data and need internet access.
