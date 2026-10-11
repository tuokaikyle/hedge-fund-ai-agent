"""Load model settings, run the agents, and show their decisions."""

from dotenv import load_dotenv

from orchestrator import HedgeFundOrchestrator


def run(ticker: str) -> None:
    load_dotenv(".env")
    analysis = HedgeFundOrchestrator().run(ticker)
    print(analysis.model_dump_json(indent=2, exclude_none=True))
