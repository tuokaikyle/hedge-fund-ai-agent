# Lesson 8: First LLM agent

## Goal

Let a language model explain Buffett's rule-based assessment. The rules still
calculate his score and signal; the model supplies the explanation.

## What's here

```text
08-first-llm-agent/
├── README.md
├── lesson.py                      # changed: loads the root .env file
├── models.py                      # changed: adds ModelDecision
├── orchestrator.py                # changed: creates the LLM client for Buffett
├── yfinance_service.py
├── agents/
│   ├── __init__.py
│   ├── peter_lynch.py
│   └── warren_buffett.py          # changed: asks the model for an explanation
└── llm/
    ├── __init__.py                # new
    └── client.py                  # new: wraps ChatOpenAI
```

## New idea

Buffett still calculates a rule score and notes. He now sends them to the
model as a prompt and asks for a `ModelDecision` with one field,
`model_reasoning`: a short explanation of the metrics and tradeoffs. The prompt
asks the model to preserve the rule-based assessment and treat missing data as
unknown.

`LLMClient.invoke(system_prompt, user_prompt, response_model)` is the only
place that imports `ChatOpenAI` or reads the model environment variables.
`with_structured_output` makes the model answer in the shape of
`response_model`, which Pydantic validates. The orchestrator creates one client
and gives it to Buffett, so the agent never touches provider settings.

Buffett maps the rule score to `buy`, `hold`, or `sell` with the same cutoffs
as before. The model's `model_reasoning` becomes the decision's `reasoning`.
Both agents still return the same `AnalystDecision` shape, so the orchestrator
combines their rule-based scores
as before. The client calls the model with `temperature=0` and
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
uv run python run.py --ticker AAPL --lesson 8
```

This fetches live Yahoo data and makes one model API call, so it needs internet
access. Expected output is JSON with one `snapshot`, two `analyst_decisions`,
and a `final_recommendation`. Buffett's reasoning comes from the model; both
agents' scores and signals remain rule-based. Lynch's explanation still comes
from his rule notes. Scores depend on the live data, and Buffett's explanation
can vary with the model response.

## What to watch

The model produces only `model_reasoning`, which appears as `reasoning` in
Buffett's entry in `analyst_decisions`. Code calculates the score from the
metrics and the signal from that score. The `snapshot` comes from Yahoo
Finance, and the orchestrator calculates `final_recommendation` by averaging
the two rule-based scores.

To see how Buffett changed, diff his file across the two lessons:

```bash
diff -u 07-combine-opinions/agents/warren_buffett.py 08-first-llm-agent/agents/warren_buffett.py
```
