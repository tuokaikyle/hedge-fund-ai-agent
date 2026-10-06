Mostly yes. The first 9 lessons meet your standards well. Lessons 10–15 are weaker, and two things break them outright. I read the code and READMEs for all 15 lessons and diffed adjacent lessons. I didn't run any of them: the environment is missing `dotenv`, and there is no `.env`, API key or confirmed network access.

## Breaks the documented run
- **Lessons 14 and 15 will crash on a fresh clone.** Both READMEs list `config.toml`, and [config.py](14-configuration-precedence/config.py) opens it unconditionally. The file isn't on disk, and the root `.gitignore` has a `config.toml` rule that blocks it from being committed. Both lessons need the file committed. The simplest fix is to rename it to `config.example.toml`, or add a `!` exception in `.gitignore`.

## Where it meets your goals
- **Consistent agent shape.** Every agent has `analyze(snapshot) → AnalystDecision`. That matches your "same input and output shape" rule and makes the agents easy to compare.
- **Lessons 1–9 build in small steps.** The tree markers (new, changed, unchanged) match the actual diffs in every lesson. The only exceptions are the two missing `config.toml` entries.
- **Code is simple.** The code is easy to read and has no edge-case handling beyond what the main path needs.
- **The LLM boundary is clear.** The model produces only `score` and `reasoning`. Code assembles everything else, and lesson 10's README says so explicitly.

## Where it falls short

1. **LLM setup is rewritten four times.** The model settings code changes in lessons 10, 11, 13 and 14.
   - In lesson 10 the agent reads env vars and builds `ChatOpenAI` itself.
   - Lesson 11 moves that into `llm/openai_client.py`.
   - Lesson 13 replaces the env reading with `RuntimeConfig`.
   - Lesson 14 rewrites `load_config` entirely.

   This is the "repeatedly refactored" frustration your goals say to avoid. The cleanest fix is to introduce the client once, with config, in lesson 11. Lesson 10 would then be a bare call with no abstraction around it.

2. **Lessons 13–15 are mostly not about agents.** Lesson 13 is a config dataclass, lesson 14 is TOML plus CLI precedence, and lesson 15 is report formatting. This conflicts with "prevents distraction from content unrelated to the AI agent". I'd fold 13 into the LLM client, and either make 14 clearly optional or cut it. Lesson 15 is fine as a capstone if you keep it short.

3. **Comment labels pile up and break your own rule.** AGENTS.md says to label a function or class only when it helps, and to leave unchanged code unmarked. Instead, comments accumulate a history. The `__init__` in [13-runtime-settings/orchestrator.py](13-runtime-settings/orchestrator.py) carries four stacked "modified in lesson N" comments. [15-complete-report/lesson.py](15-complete-report/lesson.py) still says "introduced in lesson 14" on unchanged code. Lesson 8's `models.py` changed only because history comments were added retroactively to lessons 1, 3 and 7. Labels should appear only in the lesson that makes the change. When copied forward, drop them.

4. **The agent part arrives late.** The first LLM call is lesson 10 of 15. Lessons 3–6 are four variations of the same rule-scoring pattern (Junior, Senior, Buffett, Lynch), and lessons 5 and 6 add little structure. Junior and Senior then vanish in lesson 8. Merging 3–4 and 5–6 would bring the LLM in sooner.

5. **Lesson 10 introduces too much at once.** It adds LangChain, structured output, a system prompt, `.env` loading and a rule-score-to-LLM handoff. Its diff is 54 lines in one file.

6. **Duplicated logic.**
   - The score-to-signal mapping (70 → buy, 45 → hold) is copied into every agent and the orchestrator. That's fine while the agents are being compared, but it will bother a reader by lesson 12.
   - Lessons 10–11 hard-code a sample AAPL result in their READMEs, which will date quickly.
   - The two LLM agents (lessons 10–12) repeat the same system prompt text.

## Priorities
1. Fix `config.toml`.
2. Move the LLM client and config to one stable design, with no rewrites after lesson 11.
3. Clean up the comment labels.
4. Decide what to do with 13–14.

I can start on the `config.toml` fix and the comment cleanup if you'd like.

Here is how I'd reorganise it. The aim is to bring the agent and LLM material forward and settle the LLM and config design once. I'd also drop anything that isn't about agents.

## Proposed plan: 11 core lessons plus 1 optional

| # | Lesson | Main idea | vs. today |
|---|---|---|---|
| 1 | Start | `StockSnapshot` | same |
| 2 | Fetching data | yfinance → snapshot | same |
| 3 | First agent: Junior | One metric → `AnalystDecision` | same |
| 4 | Buffett-style agent | Several metrics with their own weights, same interface | merges today's 4 and 5; Senior is dropped |
| 5 | Lynch-style agent | Same data, a different perspective | today's 6 |
| 6 | Completeness and confidence | Input coverage vs. signal strength | today's 7 |
| 7 | Orchestrator | Fetch once, collect decisions | today's 8 |
| 8 | Combine opinions | Equal vs. confidence-weighted average | today's 9 |
| 9 | First LLM-backed agent | `LLMClient` (final shape) and a Buffett decision with a typed score and reasoning | replaces today's 10, 11 and 13 |
| 10 | Second LLM-backed agent | Reuse the same client for Lynch | today's 12 |
| 11 | Complete report | Readable output | today's 15 |
| Optional | Configuration | `.toml` and CLI overrides | today's 14, moved out of the main path |

## Why these changes

- **Merge Senior into Buffett (4 and 5).** Senior's "combine several metrics" idea is exactly what Buffett does. Dropping Senior removes an agent that disappears in lesson 8 anyway, and the LLM arrives at lesson 9 instead of 10.
- **Build the LLM client once, in lesson 9.** Today the model setup is rewritten in lessons 10, 11, 13 and 14. In the new plan, lesson 9 introduces `llm/client.py` in its final shape. It's a concrete class with `invoke(system_prompt, user_prompt, response_model)` and settings read from env vars in one place. Lesson 10 then reuses it unchanged, so `llm/` stays unchanged in the later lessons.
- **Drop the `Protocol`.** With only one implementation, it's abstraction without a reason. If you want to keep it, introduce it only when a second provider appears.
- **Handle lesson 9's density.** It still carries LangChain, structured output and a prompt. I'd keep the config to a few env vars and put the model and base URL in `.env.example`. The client file stays about 20 lines.
- **Move config precedence to the end, optional.** Lesson 14 is the one lesson here that isn't about agents. It needs `config.toml` committed, so the existing bug gets fixed whichever way you go.
- **Lesson 11 can stay short.** It's pure presentation, so one `output.py` is enough.

## Optional idea to consider

`StockSnapshot` already has `recent_headlines` and `business_summary`, but `yfinance_service.py` never fills them. A lesson between 10 and 11 could populate headlines and let the LLM agents read them. That shows what an LLM can use that rules can't, which is the real reason to use an LLM here. It would replace config as the closing "agent-ish" lesson.

## Cost

- Lessons are copies, so renumbering is mostly directory moves plus edits to READMEs, tree markers, "diff" commands and `run.py` examples.
- The comment labels ("introduced in lesson N") all need regenerating or removing, which I'd do anyway.
- The root readme's table and run list need updating.

Do you want me to do the restructure? Or would you rather settle two open choices first: whether to keep Senior, and whether to add the headlines lesson?