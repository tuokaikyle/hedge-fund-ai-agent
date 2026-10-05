# Feedback: does this course teach how AI agents work?

Scope: full review of lessons 1–15, the shared `run.py`, and the final code in
`15-complete-report/`. Judged against the stated intention: learners should
learn how AI agents work.

## What the project is

A 15-lesson progressive course. Each lesson is a self-contained folder that
copies forward the previous lesson's working code, and a shared root `run.py`
runs any lesson in one environment:

```
run.py --lesson N --ticker AAPL  ->  runpy loads NN-*/lesson.py, injects sys.path
```

The "agent" abstraction is consistent throughout: a class with
`analyze(snapshot) -> AnalystDecision`, plus an orchestrator that fetches once
and combines results.

## The pedagogical arc

| Lessons | Concept introduced | Agent concept it teaches |
| --- | --- | --- |
| 1–2 | `StockSnapshot`, yfinance -> shape | Typed data contracts between components |
| 3–4 | Junior (1 metric), Senior (3 metrics) | One agent = deterministic rule -> structured decision |
| 5–6 | Buffett (quality/value), Lynch (growth) | Same interface, different persona/metrics/weights |
| 7 | `data_completeness`, `decision_confidence` | Separating input coverage from signal strength |
| 8–9 | Orchestrator, equal vs confidence-weighted averaging | Multi-agent coordination and opinion aggregation |
| 10 | First `ChatOpenAI` call with `with_structured_output` | LLM as a reasoning step (typed output) |
| 11 | `StructuredLLM` Protocol | Reusable interface / swapping implementations |
| 12 | Lynch also uses the LLM | Same interface, second agent |
| 13–15 | `RuntimeConfig`, TOML precedence, report | Config, precedence, presentation |

The design is disciplined: one idea per lesson, unchanged files stay
byte-identical for adjacent diffs, and READMEs mark files as new/changed/
unchanged. That is genuinely good course engineering.

## Strengths for the goal

- **Immediate, readable agent shape.** Lessons 3–6 make "an agent" concrete and
  testable before any LLM appears. Learners see that an agent is a transform
  over structured data, not magic.
- **The LLM is introduced honestly.** Lesson 10 is the strongest "how agents
  work" moment: the model receives *rule-based notes*, returns a *validated
  Pydantic object* (score + reasoning), and **code, not the model, maps
  score -> signal**. This correctly frames the LLM as one component in a
  controlled pipeline, not an oracle.
- **Interfaces before implementations.** The `StructuredLLM` Protocol
  (lesson 11) teaches a real agent-design skill: agents depend on a capability,
  not a vendor. Lesson 12 reuses the client for a second agent, which drives
  the point home.
- **Consistent I/O across agents** makes comparison and aggregation easy to
  follow.

## Where it under-delivers on "how AI agents work"

This is the crux. What is taught is mostly the **scaffolding around** an LLM,
while several defining features of modern agents are absent:

1. **No autonomy / no loop.** There is no observe -> decide -> act cycle and no
   iterative refinement. `orchestrator.run()` is a fixed pipeline. Learners
   never see an agent "decide what to do next."
2. **No tools / function calling / retrieval.** The LLM never chooses to fetch
   data or call a function. Data fetching is hard-wired before the model runs.
   Tool use is arguably *the* core of agentic behavior, and it is not shown.
3. **The LLM is minimal.** It refines a pre-computed rule score with a 1-shot
   prompt. There is no planning, memory/state across steps, self-critique, or
   multi-turn interaction. A learner leaves knowing "LLM as a structured
   scoring step," not "agent."
4. **The LLM arrives very late (~70% into the course).** Nine lessons build
   rules and plumbing first. That is deliberate and defensible for data-flow
   pedagogy, but a learner drawn by "AI agents" waits a long time for the AI.
5. **No failure-mode teaching.** Nothing on hallucination, prompt sensitivity,
   why structured output guards matter, or what happens when the model returns
   something unreasonable. These are exactly the "how agents actually behave"
   lessons.

## Drift from the stated intention

Lessons 13–15 (config dataclass, TOML/env/CLI precedence, terminal report) are
solid software-engineering lessons but are **application production concerns,
not agent concepts**. For a course whose goal is "how AI agents work," these
are roughly 20% of the curriculum spent on configuration and formatting. They
would fit better as an appendix or a separate "shipping an agent" track.

## Recommendation

The course is a strong "how to structure a small LLM-backed decision system."
To fully match "how AI agents work," consider:

- **Add a planning/loop lesson** after 12: let an agent decide among 2–3
  actions (fetch more data, ask the LLM, finalize), demonstrating a real agent
  loop.
- **Add a tool-calling lesson**: give the LLM a function to fetch a metric, so
  it *chooses* to gather data. This is the highest-value gap.
- **Add a failure/guardrails lesson**: same agent, adversarial or missing data,
  showing why the typed output and code-owned signal mapping matter.
- **Reframe or relocate 13–15** so agent concepts dominate the arc.
- **Renumber the concept boundary** in the README table into two clear phases:
  "Agents without an LLM" (1–9) and "Agents with an LLM" (10+), so learners see
  the intent.

Net: excellent pedagogy and code discipline, and the interface/orchestration
foundation is exactly right — but the course currently teaches agent *plumbing*
more than agent *behavior*. The three additions above (loop, tools, failure
modes) would close that gap.
