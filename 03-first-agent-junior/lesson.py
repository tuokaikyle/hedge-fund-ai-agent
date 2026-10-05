"""Fetch a stock snapshot and ask the first agent to analyze it."""

from agents.junior import JuniorAgent
from yfinance_service import YFinanceService


def run(ticker: str) -> None:
    snapshot = YFinanceService().get_snapshot(ticker)
    decision = JuniorAgent().analyze(snapshot)
    print(f"{decision.analyst} on {snapshot.ticker}: {decision.signal.upper()} (score {decision.score}/100)")
    print(f"Reasoning: {decision.reasoning}")
