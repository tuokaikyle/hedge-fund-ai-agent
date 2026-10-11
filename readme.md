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

- **`v0.3`** starts with 9 foundation lessons and continues through lesson 17,
  adding model judgments, tools, collaboration, and feedback.
- **`v0.2`** has 15 lessons, with a more gradual learning curve than `v0.3`
  and slightly more content.

## Course plan

**This plan is subject to change.** 

| #   | Lesson                                                      | Main idea                                                                                   |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 1   | [Start](01-start/README.md)                                 | Define the shared `StockSnapshot` data shape.                                               |
| 2   | [Fetching data](02-fetching-data/README.md)                 | Translate yfinance fields into that shape.                                                  |
| 3   | [Junior agent](03-junior-agent/README.md)                   | Turn one metric into a structured decision.                                                 |
| 4   | [Buffett-style agent](04-warren-buffett-agent/README.md)    | Give one agent its own choice and weighting of metrics.                                     |
| 5   | [Lynch-style agent](05-peter-lynch-agent/README.md)         | Show how the same data can support a different perspective.                                 |
| 6   | [Orchestrator](06-orchestrator/README.md)                   | Fetch once and collect Buffett's and Lynch's decisions.                                     |
| 7   | [Combine opinions](07-combine-opinions/README.md)           | Average the two agents' scores to produce one final signal.                                 |
| 8   | [First LLM agent](08-first-llm-agent/README.md)             | Let an LLM explain Buffett's rule-based score through an `LLMClient`.                       |
| 9   | [Second LLM agent](09-second-llm-agent/README.md)           | Reuse the same client and response shape for Lynch's explanation.                           |
| 10  | [LLM judgment](10-llm-judgment/README.md)                   | Let Buffett make a model-based assessment instead of explaining a rule score.               |
| 11  | [Second LLM judgment](11-second-llm-judgment/README.md)     | Give Lynch the same model-based assessment path as Buffett.                                 |
| 12  | [First tool](12-first-tool/README.md)                       | Give the analysts an additional source of evidence through an ordinary Python function.     |
| 13  | [Model calls a tool](13-model-calls-tool/README.md)         | Let Buffett request a tool and use the returned evidence in his assessment.                 |
| 14  | [Agent loop](14-agent-loop/README.md)                       | Let each analyst choose whether another tool would help after seeing the first result.      |
| 15  | [Manager agent](15-manager-agent/README.md)                 | Use an agent to combine the analysts’ assessments into a reasoned recommendation.           |
| 16  | [Reviewer agent](16-reviewer-agent/README.md)               | Have a separate agent check whether the manager’s recommendation follows from the evidence. |
| 17  | [Revise after feedback](17-revise-after-feedback/README.md) | Let the manager respond to review while preserving the result before feedback.              |

Lessons 1–9 introduce the shared data shape, rule-based analysts, and model-written
explanations. Lessons 10–17 progressively give models assessments to make,
tools to request, and other agents' outputs and feedback to act on. The analysts
keep `analyze(snapshot) -> AnalystDecision` throughout.

## Code added and learning difficulty

Line counts compare each lesson with the previous one and include added Python
code lines, excluding blank lines, comments, docstrings, and unchanged copied
code. Replacement lines count as additions; the shared `run.py` is excluded.

Difficulty estimates assume basic Python knowledge: **1 = easy; 5 = demanding**.

| #   | Lesson                | Lines added | Difficulty | Main learning challenge                                                     |
| --- | --------------------- | ----------: | ---------- | --------------------------------------------------------------------------- |
| 1   | Start                 |          29 | 2/5        | Pydantic models, type hints, and optional fields                            |
| 2   | Fetching data         |          31 | 2/5        | Mapping API fields into a consistent data shape                             |
| 3   | Junior agent          |          39 | 2/5        | Turning a metric into a score and structured decision                       |
| 4   | Buffett-style agent   |          62 | 3/5        | Combining several scoring functions and weights                             |
| 5   | Lynch-style agent     |          48 | 2/5        | Reusing the agent pattern; understanding the PEG calculation                |
| 6   | Orchestrator          |          18 | 2/5        | Moving fetching and the agent loop into one coordinating class              |
| 7   | Combine opinions      |          20 | 2/5        | Averaging scores and producing a final recommendation                       |
| 8   | First LLM agent       |          63 | 4/5        | Client setup, prompts, structured output, and passing dependencies          |
| 9   | Second LLM agent      |          29 | 2/5        | Applying the established LLM pattern to another agent                       |
| 10  | LLM judgment          |          20 | 2/5        | Moving assessment from rules into a structured model response               |
| 11  | Second LLM judgment   |          18 | 2/5        | Applying the established assessment pattern to a second perspective         |
| 12  | First tool            |           7 | 2/5        | Separating a data capability from the agent that consumes it                |
| 13  | Model calls a tool    |          80 | 4/5        | Following tool schemas, model requests, execution, and tool-result messages |
| 14  | Agent loop            |          51 | 4/5        | Preserving evidence across tool calls and choosing when to stop             |
| 15  | Manager agent         |          54 | 2/5        | Passing independent agents’ outputs and evidence to a coordinating agent    |
| 16  | Reviewer agent        |          27 | 2/5        | Giving another agent an explicit review task and structured feedback        |
| 17  | Revise after feedback |          19 | 2/5        | Using feedback to revise a result and keeping before-and-after outputs      |

Lesson 6 also removes 38 code lines, so its net change is −20, mainly from
removing Junior and replacing the previous lesson's loop.

## Run a built lesson

From the repository root with a ticker and lesson number, for example:

```bash
uv sync
uv run python run.py --ticker AAPL --lesson 1
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
  supplies model calls, tool schemas, and tool-call messages; the agent loop
  remains plain Python.
- **A formatted report.** The final output is the analysis as JSON. There is no
  report renderer.
- **News analysis.** The business summary is introduced in lesson 12, but no
  lesson fetches or analyzes news headlines.
- **Confidence measures and weighted aggregation.** Lessons 7–14 average the
  two analyst scores; lesson 15 introduces a manager assessment. These scores
  are judgments, not confidence estimates. The course does not calculate
  confidence or assign numeric weights to the agents.
- **Rich data and real analysis.** Data comes from Yahoo: a stock snapshot, a
  business description from lesson 12, and annual revenue from lesson 14. There
  is no price history or insider trading data. The initial scoring rules are
  teaching rules, and later model scores are qualitative assessments. The
  course does not establish a moat or calculate intrinsic value and margin
  of safety.
- **Framework orchestration and persistent memory.** Tool use is a small Python
  loop. There are no graphs, parallel agent runs, saved conversation memory,
  or retry/fallback layers added by the course. Review offers one revision.
- **The original's wider scope.** There is no portfolio or risk management,
  trading, backtesting, or web interface. Buffett and Lynch analyze
  one ticker at a time; a manager and reviewer coordinate their results.
- **Production concerns.** There is no caching, rate limiting, logging, or
  automated tests, and little error handling. Early rule-based analysts assign
  partial points to missing metrics; later model prompts treat missing facts
  as unknown. Tool traces are printed with the analysis.
