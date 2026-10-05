# Lesson 14: Configuration precedence

## Goal

Combine defaults, environment settings, a TOML file, and CLI overrides into
one runtime config.

## What's here

```text
14-configuration-precedence/
├── README.md
├── config.toml                    # new: public model settings
├── config.py                      # changed: merges settings in order
├── lesson.py                      # changed: defines and passes CLI overrides
├── models.py                      # unchanged from lesson 13
├── orchestrator.py                # unchanged from lesson 13
├── yfinance_service.py            # unchanged from lesson 13
├── agents/
│   ├── __init__.py                # unchanged from lesson 13
│   ├── peter_lynch.py             # unchanged from lesson 13
│   └── warren_buffett.py          # unchanged from lesson 13
├── llm/
│   ├── __init__.py                # unchanged from lesson 13
│   ├── interface.py               # unchanged from lesson 13
│   └── openai_client.py           # unchanged from lesson 13
└── utils/
    ├── __init__.py                # unchanged from lesson 13
    ├── confidence.py              # unchanged from lesson 13
    └── data_completeness.py       # unchanged from lesson 13
```

The shared root `run.py` also changes: it reads the lesson number, lets the
selected lesson add CLI arguments, then parses and passes those arguments.
Earlier lessons still accept their original `--lesson` and `--ticker` options.

## New idea

`load_config()` merges public settings from lowest to highest priority:

| Priority | Source | Example |
| --- | --- | --- |
| 1 | Defaults in code | `temperature = 0.0` |
| 2 | Environment, including the root `.env` | `LLM_TEMPERATURE=0.2` |
| 3 | TOML file | `temperature = 0.1` |
| 4 | CLI | `--temperature 0` |

In that example, the final temperature is `0`. An omitted CLI option is `None`
and is left out of the overrides; an explicit zero still overrides the file.
`load_dotenv()` preserves values already set in the shell.

The four public settings are `model`, `base_url`, `temperature`, and
`reasoning_effort`. Their environment names use the `LLM_` prefix and uppercase,
and their CLI names use hyphens, such as `--base-url` and `--reasoning-effort`.
The API key comes only from `LLM_API_KEY` in the environment and is not printed.

By default, the loader reads this lesson's `config.toml`. It sets temperature
and reasoning effort; model and endpoint come from the environment or defaults.
Uncomment those fields to override the environment too. `--config path/to/file.toml`
selects another file, with a relative path resolved from the working directory.
The selected file must exist. Python's built-in `tomllib` reads it, so no new
dependency is needed.

The result is the same `RuntimeConfig` from lesson 13. The orchestrator, client,
and agents need no changes because they already receive resolved settings.

## Run

With `LLM_API_KEY` set in the root `.env` (and the model and endpoint set for
your provider), run from the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 14 --temperature 0
```

Expected output is JSON with one `snapshot`, two model-backed
`analyst_decisions`, and a `final_recommendation`. The CLI temperature wins
over both the environment and TOML. This run fetches live Yahoo data and makes
two model calls, so scores and explanations can vary.
