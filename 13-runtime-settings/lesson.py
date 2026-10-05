"""Load model settings, run the agents, and show their decisions."""

from dotenv import load_dotenv

from config import load_config
from orchestrator import HedgeFundOrchestrator


# modified in lesson 13
def run(ticker: str) -> None:
    load_dotenv(".env")
    config = load_config()
    analysis = HedgeFundOrchestrator(config).run(ticker)
    print(analysis.model_dump_json(indent=2, exclude_none=True))
