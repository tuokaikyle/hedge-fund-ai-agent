"""Compare each agent's decision, data completeness, and confidence."""

from junior import JuniorAgent
from peter_lynch import PeterLynchAgent
from senior import SeniorAgent
from warren_buffett import WarrenBuffettAgent
from yfinance_service import YFinanceService


def run(ticker: str) -> None:
    snapshot = YFinanceService().get_snapshot(ticker)
    for agent in (JuniorAgent(), SeniorAgent(), WarrenBuffettAgent(), PeterLynchAgent()):
        decision = agent.analyze(snapshot)
        print(
            f"{decision.analyst} on {snapshot.ticker}: {decision.signal.upper()} "
            f"(score {decision.score}/100, data completeness {decision.data_completeness}%, "
            f"confidence {decision.confidence}%)"
        )
        print(f"Reasoning: {decision.reasoning}")
        print()
