# Lesson 10: First LLM decision

## Goal

Make the first model call and ask Buffett for a typed score and explanation
that the orchestrator can combine with Lynch's rule-based decision.

## What's here

```text
10-first-llm-call/
├── README.md
├── lesson.py                      # changed: loads the root .env file
├── models.py                      # changed: adds BuffettModelDecision
├── orchestrator.py                # unchanged from lesson 9
├── yfinance_service.py            # unchanged from lesson 9
├── agents/
│   ├── __init__.py                # unchanged from lesson 9
│   ├── peter_lynch.py             # unchanged from lesson 9
│   └── warren_buffett.py          # changed: requests a typed model decision
└── utils/
    ├── __init__.py                # unchanged from lesson 9
    ├── confidence.py              # unchanged from lesson 9
    └── data_completeness.py       # unchanged from lesson 9
```

## New idea

Buffett calculates a rule score and notes, then sends them to `ChatOpenAI`.
`with_structured_output(BuffettModelDecision)` asks the model for a validated
score from 0 to 100 and a short explanation. The model uses the rule score as
a starting point and may adjust it when the notes justify a different view.

Buffett maps the model score to `buy`, `hold`, or `sell` with the same cutoffs
as before. Data completeness still measures available inputs, and confidence
comes from the returned score and completeness. Buffett and rule-based Lynch
still return the same `AnalystDecision` shape, so the orchestrator is unchanged.
The call uses `reasoning_effort="none"` and `temperature=0`; choose a model
and provider endpoint that accept both settings.

## Run

From the repository root, create `.env` if needed and fill in `LLM_API_KEY`.
The example sets `LLM_MODEL` to `gpt-6-luna` and `LLM_BASE_URL` to OpenAI's
endpoint. You can change all three values for another compatible provider.

```bash
cp -n .env.example .env
```

Then run:

```bash
uv run python run.py --ticker AAPL --lesson 10
```

This fetches live Yahoo data and makes one model API call, so it needs internet
access. Expected output is JSON with one `snapshot`, two `analyst_decisions`,
and a `final_recommendation`. Buffett's score and reasoning come from the
model; his signal follows that score. Lynch remains rule-based. Values depend
on the data and model response.

## What to watch

The model's response is not printed separately. It appears inside Buffett's
entry in `analyst_decisions`. The model returns only two fields through
`BuffettModelDecision`: `score` and `reasoning`. In one AAPL run, it returned a
score of 77 and an explanation saying the expensive P/E did not justify
changing the rule score.

The rest of Buffett's entry is assembled by code: 77 maps to `buy`, the five
available inputs give `data_completeness` of 100, and the distance from the
buy cutoff gives `confidence` of 57. Lynch's score and explanation still come
entirely from rules. The `snapshot` comes from Yahoo Finance, and the
`final_recommendation` combines the two agent scores; it is not another model
response. Your numbers and model wording may differ from this example.
