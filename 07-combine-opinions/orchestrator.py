"""Fetch one stock snapshot and combine the agents' decisions."""

from agents.peter_lynch import PeterLynchAgent
from agents.warren_buffett import WarrenBuffettAgent
from models import AnalystDecision, FinalRecommendation, Signal, TickerAnalysis
from yfinance_service import YFinanceService


class HedgeFundOrchestrator:
    def __init__(self) -> None:
        self.data_service = YFinanceService()
        self.agents = (WarrenBuffettAgent(), PeterLynchAgent())

    # changed in lesson 6, 7
    def run(self, ticker: str) -> TickerAnalysis:
        snapshot = self.data_service.get_snapshot(ticker)
        decisions = [agent.analyze(snapshot) for agent in self.agents]
        final = self._combine_decisions(decisions)
        return TickerAnalysis(
            snapshot=snapshot,
            analyst_decisions=decisions,
            final_recommendation=final,
        )

    # changed in lesson 7
    def _combine_decisions(self, decisions: list[AnalystDecision]) -> FinalRecommendation:
        """Average the analysts' scores and derive one final signal."""
        score = round(sum(decision.score for decision in decisions) / len(decisions))
        return FinalRecommendation(score=score, signal=self._signal_from_score(score))

    # changed in lesson 7
    def _signal_from_score(self, score: int) -> Signal:
        if score >= 70:
            return "buy"
        if score >= 45:
            return "hold"
        return "sell"
