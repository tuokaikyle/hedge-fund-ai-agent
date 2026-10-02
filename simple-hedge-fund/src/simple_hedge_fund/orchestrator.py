"""Coordinate data fetching, analyst runs, and final recommendation assembly."""

from __future__ import annotations

from simple_hedge_fund.agents.peter_lynch import PeterLynchAgent
from simple_hedge_fund.agents.warren_buffett import WarrenBuffettAgent
from simple_hedge_fund.data.yfinance_service import YFinanceService
from simple_hedge_fund.llm.factory import build_llm
from simple_hedge_fund.models import AppConfig, FinalRecommendation, RunResult, Signal, TickerAnalysis


class SimpleHedgeFundOrchestrator:
    """Own the end-to-end analysis flow for a list of tickers."""
    def __init__(self, config: AppConfig):
        self._config = config
        self._data_service = YFinanceService()
        self._llm, self._llm_status = build_llm(config)
        self._buffett = WarrenBuffettAgent()
        self._lynch = PeterLynchAgent()

    def run(self, tickers: list[str]) -> RunResult:
        """Analyze each ticker and collect both analyst views plus a combined result."""
        analyses: list[TickerAnalysis] = []
        for ticker in tickers:
            snapshot = self._data_service.get_snapshot(ticker)
            buffett_decision = self._buffett.analyze(snapshot, self._llm)
            lynch_decision = self._lynch.analyze(snapshot, self._llm)
            final_recommendation = self._combine_decisions([buffett_decision, lynch_decision])
            analyses.append(
                TickerAnalysis(
                    snapshot=snapshot,
                    analyst_decisions=[buffett_decision, lynch_decision],
                    final_recommendation=final_recommendation,
                )
            )

        return RunResult(
            provider=self._config.provider,
            model=self._config.model,
            llm_enabled=self._llm is not None,
            llm_status=self._llm_status,
            analyses=analyses,
        )

    def _combine_decisions(self, decisions) -> FinalRecommendation:
        """Collapse the two analyst decisions into one weighted recommendation."""
        signal_weights = {"buy": 1.0, "hold": 0.0, "sell": -1.0}
        weighted_total = sum(signal_weights[decision.signal] * (decision.confidence / 100) for decision in decisions)
        average_score = sum(decision.score for decision in decisions) / len(decisions)

        if weighted_total >= 0.35:
            signal: Signal = "buy"
        elif weighted_total <= -0.35:
            signal = "sell"
        else:
            signal = "hold"

        confidence = min(95, max(50, int((abs(weighted_total) * 35) + (average_score * 0.45))))
        analyst_labels = ", ".join(f"{decision.analyst}: {decision.signal}" for decision in decisions)
        summary = (
            f"Final view: {signal}. Combined analyst signals were {analyst_labels}. "
            f"The average heuristic score was {average_score:.0f}/100."
        )

        return FinalRecommendation(
            signal=signal,
            confidence=confidence,
            summary=summary,
        )
