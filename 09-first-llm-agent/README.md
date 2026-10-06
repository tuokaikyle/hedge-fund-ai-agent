# Lesson 9: First LLM agent

## Goal

Let Buffett use a language model to make his assessment. The model returns a
typed score and explanation that the orchestrator combines with Lynch's
rule-based decision.

## What's here

```text
09-first-llm-agent/
├── README.md
├── lesson.py                      # changed: loads the root .env file
├── models.py                      # changed: adds BuffettModelDecision
├── orchestrator.py                # changed: creates the LLM client for Buffett
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── peter_lynch.py
│   └── warren_buffett.py          # changed: asks the model for a decision
├── llm/
│   ├── __init__.py                # new
│   └── client.py                  # new: wraps ChatOpenAI
└── utils/
    ├── __init__.py
    ├── confidence.py
    └── data_completeness.py
```

## New idea

Buffett still calculates a rule score and notes. He now sends them to the
model as a prompt and asks for a `BuffettModelDecision`: a score from 0 to 100
and a short explanation. The model uses the rule score as a starting point and
may adjust it when the notes justify a different view.

`LLMClient.invoke(system_prompt, user_prompt, response_model)` is the only
place that imports `ChatOpenAI` or reads the model environment variables.
`with_structured_output` makes the model answer in the shape of
`response_model`, which Pydantic validates. The orchestrator creates one client
and gives it to Buffett, so the agent never touches provider settings.

Buffett maps the model score to `buy`, `hold`, or `sell` with the same cutoffs
as before. Data completeness still measures available inputs, and confidence
comes from the returned score and completeness. Buffett and rule-based Lynch
still return the same `AnalystDecision` shape, so the rest of the orchestrator
is unchanged. The client calls the model with `temperature=0` and
`reasoning_effort="none"`; choose a model and endpoint that accept both.

## Run

From the repository root, create `.env` if needed and fill in `LLM_API_KEY`.
`.env.example` sets `LLM_MODEL` and `LLM_BASE_URL` for OpenAI; change all three
values to use another compatible provider.

```bash
cp -n .env.example .env
```

Then run:

```bash
uv run python run.py --ticker AAPL --lesson 9
```

This fetches live Yahoo data and makes one model API call, so it needs internet
access. Expected output is JSON with one `snapshot`, two `analyst_decisions`,
and a `final_recommendation`. Buffett's score and reasoning come from the
model; his signal follows that score. Lynch remains rule-based. Values depend
on the data and model response.

## What to watch

The model's response is not printed separately. It appears inside Buffett's
entry in `analyst_decisions`. The model produces only two fields, `score` and
`reasoning`. Code assembles the rest: the `signal` from the score, the
`data_completeness` from the available inputs, and the `confidence` from both.
The `snapshot` comes from Yahoo Finance, and the `final_recommendation`
combines the two agent scores; it is not another model response.

To see how Buffett changed, diff his file across the two lessons:

```bash
diff -u 08-combine-opinions/agents/warren_buffett.py 09-first-llm-agent/agents/warren_buffett.py
```
