"""Compare the first investor persona with Junior."""

from agents.junior import JuniorAgent
from agents.warren_buffett import WarrenBuffettAgent
from yfinance_service import YFinanceService


def run(ticker: str) -> None:
    snapshot = YFinanceService().get_snapshot(ticker)
    for agent in (JuniorAgent(), WarrenBuffettAgent()):
        decision = agent.analyze(snapshot)
        print(f"{decision.analyst} on {snapshot.ticker}: {decision.signal.upper()} (score {decision.score}/100)")
        print(f"Reasoning: {decision.reasoning}")
        print()
