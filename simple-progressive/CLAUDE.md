# CLAUDE.md — simple-progressive

Rationale and methodology for this course. Read this before adding, editing,
or reordering lessons. The learner-facing overview lives in
[README.md](README.md); this file is about *how* the course is built, not
what it teaches.

## What this is

A progressive, lesson-by-lesson rebuild of
[`../simple-hedge-fund`](../simple-hedge-fund), reconstructing it from an
empty skeleton to the finished app. The target audience is someone who
wants to learn how a small multi-agent system is structured and how
LangChain fits into it — not to produce a trading tool.

The lesson count is not fixed and should not be treated as a target to hit.
Split a lesson when it's teaching more than one concept at once (see the
Junior/Senior split below — a single "first agent" lesson was cut in two
because it mixed "the agent shape" with "a realistic multi-metric
persona"). Merge lessons if two turn out to be trivial together. Resize the
plan whenever it stops matching how the material actually breaks down.

## Core methodology

1. **Each lesson is a standalone, independently runnable project.**
   Every `NN-lesson-name/` folder has its own `pyproject.toml`, its own
   `src/` tree, and its own `try_it.py` or CLI entrypoint. Nothing is
   imported across lesson folders. This was a deliberate choice over a
   single shared project so that:
   - a learner can `cd` into any lesson and run it in isolation
   - diffing lesson `N` against lesson `N+1` shows exactly what changed
   - later lessons can't accidentally depend on something a learner skipped

2. **Each lesson adds exactly one file or one concern.**
   Don't introduce a concept before its dependency exists, and don't bundle
   two new ideas into one lesson (e.g. the LLM protocol and the LangChain
   provider are two separate lessons — 09 and 10 — even though they're
   related). If a lesson's diff touches more than one clearly-scoped
   concern, it should probably be split.

3. **Mark new vs. carried-forward code explicitly.**
   Every file that has a prior-lesson version must mark what changed, using
   a section comment directly above the new or reused code:
   ```python
   # --- added in lesson 03 ---
   class WarrenBuffettAgent:
       ...
   ```
   ```python
   # --- carried forward from lesson 01, unchanged ---
   class StockSnapshot(BaseModel):
       ...
   ```
   When a lesson changes an existing function or class in place (rather
   than adding a new one beside it), mark it `modified` and say what
   changed in a few words, so the learner doesn't have to diff to find
   out:
   ```python
   # --- modified in lesson 08: takes a TickerAnalysis, adds the final recommendation ---
   def render_analysis(analysis: TickerAnalysis, *, show_explanation: bool) -> str:
       ...
   ```
   In the next lesson, if it's untouched again, it goes back to `carried
   forward from lesson 08, unchanged`.

   A file that is entirely new in a given lesson still gets the `added in
   lesson NN` marker on its main class/function — don't skip it just
   because the whole file is new. This is what lets a learner open any file
   in any lesson and immediately see what's new without having to diff
   against the previous folder.

   This also applies to each README's file-tree comment (the `# ...` notes
   in the `text` code block under "What's here"). Use `# unchanged from
   lesson NN` only when the *entire file* is byte-identical to that
   lesson's version. If a file keeps some prior content as-is but also adds
   something new (e.g. `models.py` keeping `StockSnapshot` untouched while
   adding a new `AnalystDecision` model), label the tree line `# modified:
   ...` and spell out what stayed and what's new — never `# unchanged, X
   added`, which contradicts itself.

4. **LLM/LangChain is introduced late, on purpose.**
   The app must be fully functional in heuristic-only mode for many lessons
   before any LLM is involved. This mirrors the real `simple-hedge-fund`
   project's own design (LLM is optional and degrades gracefully to
   heuristics) and lets the learner understand "agent system" as a concept
   independent of any specific LLM plumbing before LangChain enters the
   picture.

5. **Separate "the agent shape" from "a realistic persona."**
   Don't teach the mechanical shape of an agent
   (`analyze(snapshot) -> AnalystDecision`) in the same lesson as a named,
   multi-metric persona like Warren Buffett — that mixes two things a
   beginner has to learn at once. Use small, deliberately generic
   placeholder agents first (this course uses `JuniorAgent`, one metric,
   then `SeniorAgent`, several metrics combined) so the shape is already
   familiar by the time a real persona's domain-specific logic shows up.
   Placeholder agents still score on real `StockSnapshot` fields — never
   invent fake/arbitrary logic just to fill the lesson, since that breaks
   the connection to the data pipeline built in lessons 1-2.

6. **Trim dense code for early lessons; add robustness later.**
   The real project's `yfinance_service.py` and `warren_buffett.py` are
   dense (150-240 lines, many fallback branches and sub-scorers). Early
   lessons intentionally use a trimmed version — a handful of fields, one
   or a few sub-scorers, no fallback chains — so the lesson teaches
   structure, not copy-typing. Fuller robustness gets folded in near the
   end of the course, once the shape is already understood.

7. **`StockSnapshot` is defined at its full, final shape in lesson 1 and
   never widened again.** It carries every field the finished app ever
   uses (company info, valuation, profitability, leverage, growth,
   headlines) from lesson 1 onward. Later lessons' `models.py` for
   `StockSnapshot` is an unchanged carry-forward (mark it per point 3);
   each new agent just reads whichever subset of fields it needs — it
   never has to modify the shared contract to get access to more data.
   `data/yfinance_service.py` follows the same rule with one known
   exception: as of lesson 2 it populates every snapshot field *except*
   `recent_headlines`, which stays `[]` because yfinance's news payload
   needs fiddly shape-handling that would swamp an early lesson. The
   target project's Lynch agent does score headlines, so the robustness
   lesson near the end of the course is expected to fill this in — that
   revisit is planned, not an accident. Apart from that, the service isn't
   revisited just to add fields. New models that aren't part of the snapshot (`AnalystDecision`,
   `FinalRecommendation`, etc.) still get added incrementally, in the
   lesson that introduces their first consumer.

8. **Don't import the target project's finance machinery just because it's
   there.** This course teaches how an agent system is wired together, not
   how to value a company. The target's `AnalystDecision` carries a
   `confidence` field and its orchestrator weights each analyst by it —
   that is an *investing* refinement, and reproducing it costs every agent
   an extra output and an extra method before anything consumes them. This
   course deliberately omits it: `AnalystDecision` stays
   `analyst/signal/score/reasoning/key_points`, and lesson 8's orchestrator
   should combine signals with the simplest rule that demonstrates
   aggregation (majority, or mean score). Apply the same test to anything
   else carried over from the target — if a beginner needs domain knowledge
   to see why it exists, and no agent-architecture concept depends on it,
   leave it out. `used_llm` is a genuine exception: it's added in lesson 9,
   where the LLM seam makes it meaningful.

## Lesson plan

The lesson table lives in one place only: [README.md](README.md#lessons).
Don't copy it here — a second table drifts out of date. Lesson numbers
mentioned elsewhere in this file refer to that table. If a future lesson
turns out to need splitting or merging, renumber the table rather than
leaving gaps or inserting letter suffixes, and update any lesson numbers
cited in this file to match.

## When adding a new lesson

1. Copy forward the previous lesson's folder as a starting point.
2. Make the one change the lesson is about.
3. Mark new/changed code per point 3 above.
4. Write the lesson's `README.md`: goal, what's new, why it's built that
   way, how to run it, link to the next lesson.
5. Actually run it (`uv sync && uv run ...`) before considering it done —
   don't hand back unverified code.
6. Update the `README.md` table entry from "*(coming)*" to a real link.
