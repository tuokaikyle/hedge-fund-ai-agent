"""A second analyst that combines three business metrics."""

from utils.confidence import decision_confidence
from utils.data_completeness import data_completeness
from models import AnalystDecision, Signal, StockSnapshot


class SeniorAgent:
    def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
        roe_score, roe_note = self._score_roe(snapshot.return_on_equity)
        debt_score, debt_note = self._score_debt(snapshot.debt_to_equity)
        margin_score, margin_note = self._score_margin(snapshot.profit_margin)

        score = roe_score + debt_score + margin_score
        if score >= 70:
            signal: Signal = "buy"
        elif score >= 45:
            signal = "hold"
        else:
            signal = "sell"

        completeness = data_completeness(
            snapshot.return_on_equity, snapshot.debt_to_equity, snapshot.profit_margin
        )
        return AnalystDecision(
            analyst="Senior",
            signal=signal,
            score=score,
            data_completeness=completeness,
            confidence=decision_confidence(score, completeness),
            reasoning=" ".join((roe_note, debt_note, margin_note)),
        )

    def _score_roe(self, value: float | None) -> tuple[int, str]:
        if value is None:
            return 15, "ROE is unavailable."
        if value >= 0.18:
            return 40, f"ROE is strong at {value:.1%}."
        if value >= 0.12:
            return 28, f"ROE is moderate at {value:.1%}."
        return 10, f"ROE is low at {value:.1%}."

    def _score_debt(self, value: float | None) -> tuple[int, str]:
        if value is None:
            return 15, "Debt-to-equity is unavailable."
        if value <= 0.5:
            return 30, f"Debt-to-equity is low at {value:.2f}."
        if value <= 1.0:
            return 20, f"Debt-to-equity is moderate at {value:.2f}."
        return 8, f"Debt-to-equity is high at {value:.2f}."

    def _score_margin(self, value: float | None) -> tuple[int, str]:
        if value is None:
            return 15, "Profit margin is unavailable."
        if value >= 0.15:
            return 30, f"Profit margin is healthy at {value:.1%}."
        return 10, f"Profit margin is low at {value:.1%}."
