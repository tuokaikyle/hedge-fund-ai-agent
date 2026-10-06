# Lesson 7: Combine opinions

## Goal

Average Buffett's and Lynch's independent scores to produce one final signal.

## What's here

```text
07-combine-opinions/
├── README.md
├── lesson.py
├── models.py                      # changed: adds FinalRecommendation
├── orchestrator.py                # changed: combines the two decisions
├── yfinance_service.py
└── agents/
    ├── __init__.py
    ├── peter_lynch.py
    └── warren_buffett.py
```

## New idea

The orchestrator adds the two scores, divides by the number of agents, and
rounds to a whole number. For example, scores of 80 and 60 give a final score
of 70. Both agents have equal influence.

The average uses the familiar cutoffs: 70 or more is `buy`, 45–69 is `hold`,
and below 45 is `sell`. `FinalRecommendation` contains the average `score` and
its `signal`. The agents keep their individual scores and explanations, so
their different perspectives remain visible alongside the combined result.

## Run

From the repository root:

```bash
uv run python run.py --ticker AAPL --lesson 7
```

This fetches live data and needs internet access. Expected output: JSON with
one `snapshot`, two `analyst_decisions`, and a `final_recommendation` containing
`score` and `signal`. Values depend on the data Yahoo returns.
