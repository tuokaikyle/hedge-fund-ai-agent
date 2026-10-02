# Simple Hedge Fund: A Progressive Mini Course

This is a from-scratch, lesson-by-lesson rebuild of
[`simple-hedge-fund`](../simple-hedge-fund), a minimal AI agent system that
scores stocks using two investor personas (Warren Buffett and Peter Lynch)
and optionally refines their calls with an LLM via LangChain.

The goal isn't to trade — it's to learn how a small multi-agent system is
structured, and how LangChain fits into one narrow seam of it, by building
it up one concern at a time instead of reading the finished result
top-down.

## How this course works

- Each lesson lives in its own numbered folder (`01-...`, `02-...`, etc.)
  and is a **complete, independently runnable project** — its own
  `pyproject.toml`, its own `src/`, its own `try_it.py` or CLI you can
  actually execute.
- Every lesson builds on the previous one: later folders copy forward what
  already worked and add exactly one new file or concern. Diffing lesson
  `N` against lesson `N+1` shows you exactly what changed and why.
- Each lesson's `README.md` explains the goal, what's new, why it's built
  that way, how to run it, and links to the next lesson.
- LLM/LangChain integration is deliberately introduced late. The app is
  fully working in heuristic-only mode for many lessons before that, so
  "agent system" is learned as a concept independent of any specific LLM
  plumbing — matching the real project's own design, where the LLM is
  optional and gracefully degrades.
- The lesson count isn't fixed. This table grows or shrinks as the course
  is built — a step gets split when it's doing too much at once (see
  lessons 3-4 below), or merged if two steps turn out to be trivial
  together. Treat the table as the current plan, not a locked spec.

## Lessons

| # | Folder | Focus | New concept |
|---|--------|-------|-------------|
| 1 | [01-project-skeleton](01-project-skeleton) | Project setup + the data contract | Defining a Pydantic model (`StockSnapshot`) before writing any logic |
| 2 | [02-fetching-data](02-fetching-data) | Fetching real data | Wrapping a messy third-party API (yfinance) behind a clean interface |
| 3 | [03-first-agent-junior](03-first-agent-junior) | First agent (Junior), one metric | An agent as a deterministic function — no LLM, no persona yet |
| 4 | [04-second-agent-senior](04-second-agent-senior) | Second agent (Senior), combined metrics | Same agent shape, but scoring and summing several metrics |
| 5 | [05-warren-buffett-agent](05-warren-buffett-agent) | First real persona | Persona-specific investing logic layered on the shape you already know |
| 6 | [06-peter-lynch-agent](06-peter-lynch-agent) | Second real persona | Reinforcing the shape with an independent, differently-weighted persona |
| 7 | [07-cli-and-output](07-cli-and-output) | A real CLI | Turning a script into a usable command-line tool |
| 8 | [08-orchestrator](08-orchestrator) | Combining opinions | Multi-agent aggregation into one final decision |
| 9 | 09-llm-seam *(coming)* | Defining the LLM interface | Programming to a protocol, independent of any provider SDK |
| 10 | 10-langchain-provider *(coming)* | Wiring in LangChain | `ChatPromptTemplate` + structured output, with heuristic fallback |
| 11 | 11-config-layering *(coming)* | Config resolution | Env vars, TOML, and CLI flags merged with clear precedence |
| 12 | 12-full-report *(coming)* | Pulling it together | Both agents LLM-backed, full report output, final shape of the app |

## Running any lesson

```bash
cd simple-progressive/0N-lesson-name
uv sync
uv run python try_it.py        # or the lesson's CLI, once introduced
```

## Relationship to the other projects in this workspace

- [`../simple-hedge-fund`](../simple-hedge-fund) is the finished target this
  course reconstructs.
- [`../ai-hedge-fund-cl`](../ai-hedge-fund-cl) is a good "level 2" once this
  course is done — the same two personas, but orchestrated as a LangGraph
  state graph, and with dedicated portfolio-manager and risk-manager
  agents on top.
- [`../ai-hedge-fund-main`](../ai-hedge-fund-main) is the original full-stack
  project (FastAPI + React + DB) that both simplified versions descend from.
