"""Fetch data, run the analysts, and ask the manager for a recommendation."""

from agents.manager import ManagerAgent
from agents.reviewer import ReviewerAgent
from agents.peter_lynch import PeterLynchAgent
from agents.warren_buffett import WarrenBuffettAgent
from llm.client import LLMClient
from models import TickerAnalysis
from yfinance_service import YFinanceService


class HedgeFundOrchestrator:
    # changed in lesson 6, 8, 9, 15, 16
    def __init__(self) -> None:
        self.data_service = YFinanceService()
        llm = LLMClient()
        self.agents = (WarrenBuffettAgent(llm), PeterLynchAgent(llm))
        self.manager = ManagerAgent(llm)
        self.reviewer = ReviewerAgent(llm)

    # changed in lesson 6, 7, 12, 13, 14, 15, 16
    def run(self, ticker: str) -> TickerAnalysis:
        snapshot = self.data_service.get_snapshot(ticker)
        decisions = [agent.analyze(snapshot) for agent in self.agents]
        tool_calls = [call for agent in self.agents for call in agent.tool_calls]
        final = self.manager.combine(snapshot, decisions, tool_calls)
        analysis = TickerAnalysis(
            snapshot=snapshot,
            analyst_decisions=decisions,
            final_recommendation=final,
            tool_calls=tool_calls,
        )
        analysis.review = self.reviewer.review(analysis)
        return analysis
