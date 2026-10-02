"""Buffett-style analyst: quality, balance-sheet discipline, and valuation.

Same analyze(snapshot) -> AnalystDecision shape as JuniorAgent and
SeniorAgent (lessons 3-4). What's new here isn't the mechanics — it's
persona-specific domain logic: which metrics a "Buffett style" investor
cares about, how they're weighted, and how the reasoning is framed.

Still no LLM. Lesson 9 introduces an LLM seam; this agent will optionally
use it starting there.
"""

from __future__ import annotations

from simple_hedge_fund.models import AnalystDecision, Signal, StockSnapshot


# --- added in lesson 05 ---
class WarrenBuffettAgent:
    """Score a stock the way a Buffett-style investor might: efficient use of
    capital, conservative leverage, durable profitability, and a fair price.
    """
    name = "Warren Buffett"

    def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
        """Score four Buffett-flavored sub-factors and turn the total into a decision."""
        roe_score, roe_note = self._score_roe(snapshot.return_on_equity)
        debt_score, debt_note = self._score_debt(snapshot.debt_to_equity)
        margin_score, margin_note = self._score_margins(snapshot.profit_margin, snapshot.operating_margin)
        valuation_score, valuation_note = self._score_valuation(snapshot.trailing_pe)

        total_score = min(100, roe_score + debt_score + margin_score + valuation_score)
        signal = self._score_to_signal(total_score)
        notes = [roe_note, debt_note, margin_note, valuation_note]

        return AnalystDecision(
            analyst=self.name,
            signal=signal,
            score=total_score,
            reasoning=(
                f"Buffett-style view on {snapshot.ticker}: {' '.join(notes)} "
                f"Overall this looks like a {signal} based on quality, leverage, and valuation."
            ),
            key_points=notes,
        )

    # Factor: return on equity (capital efficiency).
    def _score_roe(self, value: float | None) -> tuple[int, str]:
        """Score capital efficiency, out of 30. Central to the Buffett profile."""
        if value is None:
            return 12, "ROE is unavailable, so business quality is harder to judge."
        if value >= 0.18:
            return 30, f"ROE is strong at {value:.1%}, suggesting efficient use of shareholder capital."
        if value >= 0.12:
            return 20, f"ROE is respectable at {value:.1%}, though not exceptional."
        return 8, f"ROE is weak at {value:.1%}, which is not ideal for a Buffett-style profile."

    # Factor: debt-to-equity (leverage).
    def _score_debt(self, value: float | None) -> tuple[int, str]:
        """Score leverage, out of 25. Buffett favors conservative balance sheets."""
        if value is None:
            return 12, "Debt-to-equity is unavailable, so leverage risk is less clear."
        if value <= 0.5:
            return 25, f"Debt-to-equity is conservative at {value:.2f}."
        if value <= 1.0:
            return 17, f"Debt-to-equity is manageable at {value:.2f}."
        return 6, f"Debt-to-equity is elevated at {value:.2f}, which weakens the balance-sheet story."

    # Factors: profit margin and operating margin (profitability).
    def _score_margins(self, profit_margin: float | None, operating_margin: float | None) -> tuple[int, str]:
        """Score profitability from both bottom-line and operating angles, out of 25."""
        if profit_margin is None or operating_margin is None:
            return 10, "Margin data is unavailable."
        if profit_margin >= 0.15 and operating_margin >= 0.15:
            return 25, f"Profit margin ({profit_margin:.1%}) and operating margin ({operating_margin:.1%}) are both healthy."
        if profit_margin >= 0.08 or operating_margin >= 0.1:
            return 16, f"Margins are acceptable: profit {profit_margin:.1%}, operating {operating_margin:.1%}."
        return 6, f"Margins are thin: profit {profit_margin:.1%}, operating {operating_margin:.1%}."

    # Factor: trailing PE (valuation).
    def _score_valuation(self, trailing_pe: float | None) -> tuple[int, str]:
        """Score a simple valuation anchor, out of 20. Buffett wants a fair price, not just a good business."""
        if trailing_pe is None or trailing_pe <= 0:
            return 8, "Trailing PE is unavailable, so valuation is harder to compare."
        if trailing_pe <= 20:
            return 20, f"Trailing PE of {trailing_pe:.1f} looks reasonable for a quality business."
        if trailing_pe <= 28:
            return 13, f"Trailing PE of {trailing_pe:.1f} is fair but not especially cheap."
        return 5, f"Trailing PE of {trailing_pe:.1f} looks expensive for a Buffett-style entry point."

    def _score_to_signal(self, score: int) -> Signal:
        """Map the combined score to a coarse buy/hold/sell recommendation."""
        if score >= 70:
            return "buy"
        if score >= 45:
            return "hold"
        return "sell"
