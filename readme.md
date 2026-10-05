# Hedge Fund Mini

A small course on building an agent system one step at a time. The agents use
simple stock rules so the focus stays on data flow, agent interfaces, and
coordination. This is a learning project, not investment advice.

Each lesson is a runnable folder. It carries forward the previous lesson's
working code, and the root `run.py` runs every lesson with the same Python
environment. Comparing adjacent folders shows what changed.
The `agents/`, `utils/`, and `llm/` folders appear when lessons first need them.

## Course plan

**This plan is subject to change.** Lessons 1–15 are built. We can split,
merge, or add lessons as we learn what makes each idea easiest to understand.
Each lesson adds one main idea and runs through `run.py`.

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
| 10  | [First LLM decision](10-first-llm-call/README.md)                                 | Let Buffett return a typed model score and explanation for the orchestrator to combine.   |
| 11  | [Shared LLM interface](11-shared-llm-interface/README.md)                         | Move model-specific code behind a small reusable interface.                              |
| 12  | [Second LLM-backed agent](12-second-llm-backed-agent/README.md)                   | Reuse the interface for the other investor perspective.                                  |
| 13  | [Runtime settings](13-runtime-settings/README.md)                                                      | Collect model settings in one config object.                                             |
| 14  | [Configuration precedence](14-configuration-precedence/README.md)                                              | Add a TOML file and explain how defaults, environment, file, and CLI values combine.     |
| 15  | [Complete report](15-complete-report/README.md)                                                       | Render agent decisions, the final result, completeness, confidence, and model reasoning. |

Junior and Senior teach the agent interface and scoring steps. They do not
participate in decision making from lesson 8 onward; Buffett and Lynch are the
agents carried forward.

Through lesson 10, all agents use the same score cutoffs for buy, hold, and
sell. Buffett and Lynch score different metrics, but no separate rule overrides
their final signal. This keeps confidence and opinion combining easy to trace.

In lesson 7, **data completeness** measures input coverage, while
**confidence** estimates how strongly the simple rules support the final
signal. Neither is a measured probability of being correct.

Lessons 1–9 do not need an API key. The root `.env.example` can be copied to
`.env` and filled in with `LLM_API_KEY` when starting lesson 10. Lesson 10 and
later require that key. Lesson 10 makes one structured model call for Buffett's
score and explanation. Lesson 11 moves that call behind a shared interface.
Lesson 12 gives Lynch his own model-backed score and explanation through the
same interface. Lesson 13 collects model settings in a runtime config object and passes it
to the shared client. Lesson 14 layers defaults, environment settings, TOML,
and CLI overrides in that order; the API key stays in the environment.
Lesson 15 renders the completed analysis as a readable terminal report.
Configuration comes after the model path works, so each
step has a concrete purpose.

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
