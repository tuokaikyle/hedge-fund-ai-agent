# Lesson 11: Shared LLM interface

## Goal

Give agents one small way to request a typed model response, without making
each agent set up `ChatOpenAI` itself.

## What's here

```text
11-shared-llm-interface/
├── README.md
├── lesson.py                      # unchanged from lesson 10
├── models.py                      # unchanged from lesson 10
├── orchestrator.py                # changed: creates and passes the LLM client
├── yfinance_service.py            # unchanged from lesson 10
├── agents/
│   ├── __init__.py                # unchanged from lesson 10
│   ├── peter_lynch.py             # unchanged from lesson 10
│   └── warren_buffett.py          # changed: uses the shared interface
├── llm/
│   ├── __init__.py                # new
│   ├── interface.py               # new: defines StructuredLLM
│   └── openai_client.py           # new: wraps ChatOpenAI
└── utils/
    ├── __init__.py                # unchanged from lesson 10
    ├── confidence.py              # unchanged from lesson 10
    └── data_completeness.py       # unchanged from lesson 10
```

## New idea

`StructuredLLM.invoke` takes a system prompt, a user prompt, and a Pydantic
response model. `OpenAIStructuredLLM` implements that shape using the same
model settings and `ChatOpenAI` call as lesson 10. `StructuredLLM` is a
`Protocol`, so `OpenAIStructuredLLM` satisfies it structurally without
inheriting from it; the check happens where `WarrenBuffettAgent(llm:
StructuredLLM)` receives the client. The orchestrator creates one client and
gives it to Buffett. Buffett still supplies `BuffettModelDecision`, so the
model returns a score and explanation, and the rest of the decision is
assembled as before.

The call also changed from a list of `("system", ...)` / `("human", ...)`
tuples to named `system_prompt`, `user_prompt`, and `response_model`
arguments. That is deliberate: the same information is now readable at the
call site instead of being positional and easy to misread.

Only the client file imports `ChatOpenAI` or reads the model environment
variables. Lynch remains rule-based in this lesson; the same client can also
serve Lynch with a different response model and prompt.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env` file,
run from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 11
```

This fetches live Yahoo data and makes one model API call. Expected output
has the same JSON shape as lesson 10: a `snapshot`, Buffett's model-backed
decision, Lynch's rule-based decision, and a `final_recommendation`. Values
and model wording may differ between runs.

## What to watch

The JSON should be byte-for-byte comparable to lesson 10 for the same ticker
and the same data: same fields, same shapes, and the same code-assembled
values. Only the model's `score` and `reasoning` can change between runs,
because those two fields are the only ones the model produces. This lesson
reorganizes code; it does not change the decision path.

To see that the change is only in Buffett's setup, diff his file across the
two lessons from the repository root:

```bash
diff -u 10-first-llm-call/agents/warren_buffett.py 11-shared-llm-interface/agents/warren_buffett.py
```

The diff should be small: the constructor no longer imports `os` or
`ChatOpenAI`, no longer reads the model environment variables, and
`_decide_with_llm` now passes named arguments to `self.llm.invoke`.
