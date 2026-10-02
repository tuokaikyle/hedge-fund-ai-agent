"""A slightly more capable agent: still generic, but combines several
metrics instead of one. The natural next step between Junior (lesson 3)
and the real investor personas (lessons 5-6).
"""

from __future__ import annotations

from simple_hedge_fund.models import AnalystDecision, Signal, StockSnapshot


# --- carried forward from lesson 04, unchanged ---
class SeniorAgent:
    """Scores a stock using three metrics: ROE, debt-to-equity, and profit margin.

    Same analyze(snapshot) -> AnalystDecision shape as JuniorAgent. The only
    difference is that this agent scores multiple sub-factors and combines
    them, which is the same pattern the real Warren Buffett and Peter Lynch
    agents use — just with more metrics and more persona-specific framing.
    """
    name = "Senior"

    def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
        """Score three sub-factors, combine them, and turn the total into a decision."""
        roe_score, roe_note = self._score_roe(snapshot.return_on_equity)
        debt_score, debt_note = self._score_debt(snapshot.debt_to_equity)
        margin_score, margin_note = self._score_margin(snapshot.profit_margin)

        total_score = min(100, roe_score + debt_score + margin_score)
        signal = self._score_to_signal(total_score)
        notes = [roe_note, debt_note, margin_note]

        return AnalystDecision(
            analyst=self.name,
            signal=signal,
            score=total_score,
            reasoning=f"Senior's view on {snapshot.ticker}: {' '.join(notes)}",
            key_points=notes,
        )

    def _score_roe(self, value: float | None) -> tuple[int, str]:
        """Score capital efficiency, out of 40."""
        if value is None:
            return 15, "ROE is unavailable."
        if value >= 0.18:
            return 40, f"ROE is strong at {value:.1%}."
        if value >= 0.12:
            return 28, f"ROE is respectable at {value:.1%}."
        return 10, f"ROE is weak at {value:.1%}."

    def _score_debt(self, value: float | None) -> tuple[int, str]:
        """Score leverage (lower debt-to-equity is better), out of 30."""
        if value is None:
            return 15, "Debt-to-equity is unavailable."
        if value <= 0.5:
            return 30, f"Debt-to-equity is conservative at {value:.2f}."
        if value <= 1.0:
            return 20, f"Debt-to-equity is manageable at {value:.2f}."
        return 8, f"Debt-to-equity is elevated at {value:.2f}."

    def _score_margin(self, value: float | None) -> tuple[int, str]:
        """Score profitability, out of 30."""
        if value is None:
            return 15, "Profit margin is unavailable."
        if value >= 0.15:
            return 30, f"Profit margin is healthy at {value:.1%}."
        return 10, f"Profit margin is thin at {value:.1%}."

    def _score_to_signal(self, score: int) -> Signal:
        """Map the combined score to a coarse buy/hold/sell recommendation."""
        if score >= 70:
            return "buy"
        if score >= 45:
            return "hold"
        return "sell"
