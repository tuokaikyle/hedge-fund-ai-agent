# Repository Guidelines

This project is a mini course. Give learners a gentle path to understanding how
a small agent system is built.

Focus on the core logic. Keep it simple. It does not need to be production-ready
or handle every error scenario. Keep test-like demonstrations out of lesson code.
Run each lesson's documented command once, but do not test every edge case.

Keep lesson code focused on the main path. Do not write code for hypothetical
edge cases. Handle a case when it is likely to occur during the documented run
or is essential to the lesson's core logic.

This project is inspired by ai-hedge-fund-main. refer to it if you need to make big decisions or plans. 
simple-progressive is an unfinished project also in the format of educational course. 

Each lesson should contain the code it needs and run through the root `run.py`
with the shared environment. Build on the previous lesson and copy forward
working code. Keep unchanged files unchanged so adjacent lessons are easy to
compare.

Keep each lesson README concise: state the goal, show a "What's here" file tree,
explain the new idea, and give the run command and expected output. In the
tree, mark code files as new, changed, or unchanged from the previous lesson.
In code, label a new or modified function or class only when that helps the
learner spot the change; leave unchanged code unmarked.

When several agents are introduced, keep a consistent input and output shape
so their logic is easy to compare.

If uv's cache is unwritable in a sandbox, set `UV_CACHE_DIR=/tmp/hedge-fund-mini-uv-cache`
and use `uv run --no-sync` with the existing `.venv`. This does not fix Yahoo DNS
errors; those runs need network access.
