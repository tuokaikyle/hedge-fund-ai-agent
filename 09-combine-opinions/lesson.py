"""Run the agents together and show their collected decisions."""

from orchestrator import HedgeFundOrchestrator


def run(ticker: str) -> None:
    analysis = HedgeFundOrchestrator().run(ticker)
    print(analysis.model_dump_json(indent=2, exclude_none=True))
