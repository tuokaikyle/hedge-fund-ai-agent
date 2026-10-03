"""Compare the first investor persona with Junior and Senior."""

from junior import JuniorAgent
from senior import SeniorAgent
from warren_buffett import WarrenBuffettAgent
from yfinance_service import YFinanceService


def run(ticker: str) -> None:
    snapshot = YFinanceService().get_snapshot(ticker)
    for agent in (JuniorAgent(), SeniorAgent(), WarrenBuffettAgent()):
        decision = agent.analyze(snapshot)
        print(f"{decision.analyst} on {snapshot.ticker}: {decision.signal.upper()} (score {decision.score}/100)")
        print(f"Reasoning: {decision.reasoning}")
        print()
