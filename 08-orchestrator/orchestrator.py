"""Fetch one stock snapshot and collect the agents' independent decisions."""

from agents.peter_lynch import PeterLynchAgent
from agents.warren_buffett import WarrenBuffettAgent
from models import TickerAnalysis
from yfinance_service import YFinanceService


# introduced in lesson 08
class HedgeFundOrchestrator:
    # introduced in lesson 08
    def __init__(self) -> None:
        self.data_service = YFinanceService()
        self.agents = (WarrenBuffettAgent(), PeterLynchAgent())

    # introduced in lesson 08
    def run(self, ticker: str) -> TickerAnalysis:
        snapshot = self.data_service.get_snapshot(ticker)
        decisions = [agent.analyze(snapshot) for agent in self.agents]
        return TickerAnalysis(snapshot=snapshot, analyst_decisions=decisions)
