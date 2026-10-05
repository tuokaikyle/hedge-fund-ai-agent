# Lesson 13: Runtime settings

## Goal

Collect model settings in one object and pass it to the code that needs them.

## What's here

```text
13-runtime-settings/
├── README.md
├── config.py                      # new: RuntimeConfig and environment loader
├── lesson.py                      # changed: loads and passes the config
├── models.py                      # unchanged from lesson 12
├── orchestrator.py                # changed: passes config to the shared client
├── yfinance_service.py            # unchanged from lesson 12
├── agents/
│   ├── __init__.py                # unchanged from lesson 12
│   ├── peter_lynch.py             # unchanged from lesson 12
│   └── warren_buffett.py          # unchanged from lesson 12
├── llm/
│   ├── __init__.py                # unchanged from lesson 12
│   ├── interface.py               # unchanged from lesson 12
│   └── openai_client.py           # changed: reads settings from config
└── utils/
    ├── __init__.py                # unchanged from lesson 12
    ├── confidence.py              # unchanged from lesson 12
    └── data_completeness.py       # unchanged from lesson 12
```

## New idea

Previously the LLM client read environment variables itself. Now `lesson.py`
loads the root `.env`, then `load_config()` collects `LLM_MODEL`, `LLM_BASE_URL`,
and `LLM_API_KEY` into a `RuntimeConfig` dataclass. Its defaults keep
`temperature=0` and `reasoning_effort="none"`, preserving lesson 12's behavior.

The settings follow a visible path:
`lesson.py → HedgeFundOrchestrator(config) → OpenAIStructuredLLM(config)`.
The client only builds the model; it no longer decides where settings come
from. Both agents still receive the same client and use the same interface.
The config stays separate from the analysis JSON, so the API key is not printed.
Lesson 14 will add TOML and configuration precedence.

## Run

With `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` set in the root `.env`, run
from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 13
```

Expected output is JSON with one `snapshot`, two model-backed
`analyst_decisions`, and a `final_recommendation`, just like lesson 12.
This run fetches live Yahoo data and makes two model calls, so scores and
explanations can vary.
