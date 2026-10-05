"""Fetch one stock snapshot and collect the agents' independent decisions."""

from junior import JuniorAgent
from models import TickerAnalysis
from peter_lynch import PeterLynchAgent
from senior import SeniorAgent
from warren_buffett import WarrenBuffettAgent
from yfinance_service import YFinanceService


class HedgeFundOrchestrator:
    def __init__(self) -> None:
        self.data_service = YFinanceService()
        self.agents = (JuniorAgent(), SeniorAgent(), WarrenBuffettAgent(), PeterLynchAgent())

    def run(self, ticker: str) -> TickerAnalysis:
        snapshot = self.data_service.get_snapshot(ticker)
        decisions = [agent.analyze(snapshot) for agent in self.agents]
        return TickerAnalysis(snapshot=snapshot, analyst_decisions=decisions)
