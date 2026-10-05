"""Fetch one stock snapshot and combine the agents' decisions."""

from agents.peter_lynch import PeterLynchAgent
from agents.warren_buffett import WarrenBuffettAgent
from models import AnalystDecision, FinalRecommendation, Signal, TickerAnalysis
from yfinance_service import YFinanceService


# introduced in lesson 08
# modified in lesson 09
class HedgeFundOrchestrator:
    # introduced in lesson 08
    def __init__(self) -> None:
        self.data_service = YFinanceService()
        self.agents = (WarrenBuffettAgent(), PeterLynchAgent())

    # introduced in lesson 08
    # modified in lesson 09
    def run(self, ticker: str) -> TickerAnalysis:
        snapshot = self.data_service.get_snapshot(ticker)
        decisions = [agent.analyze(snapshot) for agent in self.agents]
        final = self._combine_decisions(decisions)
        return TickerAnalysis(
            snapshot=snapshot,
            analyst_decisions=decisions,
            final_recommendation=final,
        )

    # introduced in lesson 09
    def _combine_decisions(self, decisions: list[AnalystDecision]) -> FinalRecommendation:
        """Compare equal and confidence-weighted averages of the two scores."""
        plain_score = round(sum(decision.score for decision in decisions) / len(decisions))

        total_confidence = sum(decision.confidence for decision in decisions)
        weighted_score = round(
            sum(decision.score * decision.confidence for decision in decisions)
            / total_confidence
        )

        return FinalRecommendation(
            plain_score=plain_score,
            plain_signal=self._signal_from_score(plain_score),
            weighted_score=weighted_score,
            signal=self._signal_from_score(weighted_score),
        )

    # introduced in lesson 09
    def _signal_from_score(self, score: int) -> Signal:
        if score >= 70:
            return "buy"
        if score >= 45:
            return "hold"
        return "sell"
