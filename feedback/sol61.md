# Course feedback: Teaching how AI agents work

Your course gives learners a strong foundation in building a small LLM workflow. **To fully meet your goal of teaching how AI agents work, it needs a lesson where the model chooses an action, receives the result, and decides what to do next.**

I reviewed the 15 lessons and the reference projects, compared adjacent lesson folders, and ran every lesson successfully with AAPL using the shared environment and network access. No lesson code was changed during the review.

## What works well

The progressive structure works well. Each lesson introduces a manageable change, the agents share `analyze(snapshot) → AnalystDecision`, and the orchestrator makes the data flow easy to follow. Files marked “unchanged” really are identical across adjacent lessons. These are valuable teaching choices worth preserving.

The current progression teaches:

| Lessons | What learners understand |
|---|---|
| 1–4 | Structured data, fetching data, and deterministic decisions |
| 5–6 | Different analyst perspectives using the same interface |
| 7–9 | Input completeness, decision strength, and combining outputs |
| 10–12 | Prompts, structured model responses, and a shared LLM interface |
| 13–15 | Configuration and presenting results |

A learner completing this course should understand how to assemble an application containing several focused LLM calls.

## The main conceptual gap

The main conceptual gap is who controls the next step. In the [completed orchestrator](../15-complete-report/orchestrator.py), Python always fetches a snapshot, runs Buffett and Lynch sequentially, and averages their scores. Each analyst makes one model call. The model cannot request more information, select a tool, or revisit its assessment after receiving new evidence.

Terminology varies, but this is a useful distinction to teach explicitly: predefined workflows versus systems where the model directs subsequent actions and tool use. [Anthropic’s agent architecture guide](https://www.anthropic.com/engineering/building-effective-agents) makes that distinction.

The reference projects explain how this emphasis arose: `simple-hedge-fund` follows a similar fixed pipeline, and the original project adds a predefined graph. Adopting a graph framework alone would leave this learning gap unresolved.

## Recommended priorities

### 1. Explain the three stages explicitly

Introduce “rule-based analyst,” “LLM-backed analyst,” and “agent with tools and a loop.” Junior and Senior are useful scaffolding. Explain that their classes establish the input/output contract learners will later reuse for model-driven behavior. This prevents learners from concluding that any class with an `analyze()` method demonstrates AI agency.

### 2. Make the model’s contribution visible

The [Buffett prompt](../15-complete-report/agents/warren_buffett.py) supplies a rule score and already interpreted notes, then asks the model to stay close to that baseline. In my runs, Buffett stayed at 77 and Lynch at 74 throughout the rule-based and LLM-backed lessons.

That behavior fits the prompt, but learners may wonder why an LLM is needed. Show the supplied prompt, baseline score, returned score, and explanation in a concise walkthrough. Explain why judgment might help—and when rules already accomplish the task. Also clarify that `reasoning` is a generated explanation, not a trace of the model’s internal computation.

### 3. Add a small tool-use progression

The highest-value continuation would be:

| New lesson | Main idea |
|---|---|
| Model requests a tool | Define `get_stock_snapshot(ticker)` and inspect the model’s requested arguments |
| Python executes the tool | Dispatch the request and return its result to the model |
| Agent continues or finishes | Preserve messages, repeat the interaction, and stop on a final response or a small step limit |

One tool is enough to demonstrate the mechanism. Learners should see that **the model requests an action; Python executes it; the result becomes context for the next decision.** Keep the implementation small and visible.

### 4. Give agent behavior more curriculum space

Nine lessons precede the first LLM call. Lessons 4–6 reinforce the interface, but much of their new code concerns financial scoring. If you revise the sequence, bring the first model call forward after a shorter rule-based foundation. Configuration precedence can become an optional extension once learners have experienced the agent loop.

### 5. Add brief learner activities to the READMEs

Keep demonstrations out of lesson code, as your guidelines require. Add one short activity per lesson: predict the output, change a prompt, explain a disagreement, or trace which fields come from Yahoo, Python, and the model. These activities reveal understanding beyond successfully running the command.

## Smaller teaching corrections

- [“Confidence”](../15-complete-report/utils/confidence.py) is a heuristic based on distance from a decision threshold, capped by completeness. After LLM integration, it uses the model’s score. `decision_strength` would communicate its meaning more clearly.
- [Lesson 11](../11-shared-llm-interface/README.md) should clarify that `Protocol` compatibility is checked by static typing tools. Its output comparison should also acknowledge that a changed model score changes derived confidence and combined results.
- The weighted average divides by total confidence. Since earlier lessons intentionally support missing inputs, explain what happens when both weights are zero.

## Recommended direction

Preserve the existing lessons as a first chapter on building an LLM analyst workflow, then add the small tool-and-loop chapter. That would connect the course’s careful software foundations to the agent behavior you want learners to understand.
