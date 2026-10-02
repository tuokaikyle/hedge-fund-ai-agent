"""Coordinate the whole run: fetch data, ask every agent, combine their answers.

This is the "multi" in multi-agent system. Each agent only ever sees one
snapshot and returns one opinion; the orchestrator is the only place that
knows there are several agents and decides how to turn their opinions into
one final call.
"""

from __future__ import annotations

from simple_hedge_fund.agents.peter_lynch import PeterLynchAgent
from simple_hedge_fund.agents.warren_buffett import WarrenBuffettAgent
from simple_hedge_fund.data.yfinance_service import YFinanceService
from simple_hedge_fund.models import AnalystDecision, FinalRecommendation, Signal, TickerAnalysis


# --- added in lesson 08 ---
class SimpleHedgeFundOrchestrator:
    """Own the end-to-end analysis flow for a list of tickers."""

    def __init__(self):
        self._data_service = YFinanceService()
        self._agents = [WarrenBuffettAgent(), PeterLynchAgent()]

    def run(self, tickers: list[str]) -> list[TickerAnalysis]:
        """Analyze each ticker with every agent, then combine their decisions."""
        analyses: list[TickerAnalysis] = []
        for ticker in tickers:
            snapshot = self._data_service.get_snapshot(ticker)
            decisions = [agent.analyze(snapshot) for agent in self._agents]
            analyses.append(
                TickerAnalysis(
                    snapshot=snapshot,
                    analyst_decisions=decisions,
                    final_recommendation=self._combine_decisions(decisions),
                )
            )
        return analyses

    def _combine_decisions(self, decisions: list[AnalystDecision]) -> FinalRecommendation:
        """Average the analysts' scores and turn that average into one signal."""
        average_score = round(sum(decision.score for decision in decisions) / len(decisions))
        signal = self._score_to_signal(average_score)

        analyst_labels = ", ".join(f"{decision.analyst}: {decision.signal}" for decision in decisions)
        summary = f"Analysts said {analyst_labels}. Their average score is {average_score}/100, which maps to {signal}."

        return FinalRecommendation(signal=signal, score=average_score, summary=summary)

    def _score_to_signal(self, score: int) -> Signal:
        """Map the average score to buy/hold/sell, using the same cut-offs as the agents."""
        if score >= 70:
            return "buy"
        if score >= 45:
            return "hold"
        return "sell"
