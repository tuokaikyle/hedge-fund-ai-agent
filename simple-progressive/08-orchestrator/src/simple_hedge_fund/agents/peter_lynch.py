"""Lynch-style analyst: growth at a reasonable price (GARP).

Same analyze(snapshot) -> AnalystDecision shape as every other agent in
this course. What's new is a different investing philosophy from Warren
Buffett's: Lynch chases growth, and is willing to pay a higher price for a
company that's growing fast enough to justify it. His signature metric,
the PEG ratio (PE divided by growth rate), captures exactly that trade-off.

Still no LLM. Lesson 9 introduces an LLM seam; this agent will optionally
use it starting there.
"""

from __future__ import annotations

from simple_hedge_fund.models import AnalystDecision, Signal, StockSnapshot


# --- carried forward from lesson 06, unchanged ---
class PeterLynchAgent:
    """Score a stock the way a Lynch-style investor might: strong growth,
    a reasonable price relative to that growth (PEG), and steady earnings growth.
    """
    name = "Peter Lynch"

    def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
        """Score three Lynch-flavored sub-factors and turn the total into a decision."""
        growth_score, growth_note = self._score_growth(snapshot.revenue_growth)
        peg_score, peg_note = self._score_peg(snapshot.trailing_pe, snapshot.earnings_growth)
        earnings_score, earnings_note = self._score_earnings_growth(snapshot.earnings_growth)

        total_score = min(100, growth_score + peg_score + earnings_score)
        signal = self._score_to_signal(total_score)
        notes = [growth_note, peg_note, earnings_note]

        return AnalystDecision(
            analyst=self.name,
            signal=signal,
            score=total_score,
            reasoning=(
                f"Lynch-style view on {snapshot.ticker}: {' '.join(notes)} "
                f"Overall this looks like a {signal} based on growth and price relative to that growth."
            ),
            key_points=notes,
        )

    # Factor: revenue growth (top-line growth).
    def _score_growth(self, value: float | None) -> tuple[int, str]:
        """Score top-line growth, out of 35. Lynch wants a business that's actually expanding."""
        if value is None:
            return 14, "Revenue growth is unavailable."
        if value >= 0.20:
            return 35, f"Revenue growth is excellent at {value:.1%}."
        if value >= 0.08:
            return 24, f"Revenue growth is solid at {value:.1%}."
        return 10, f"Revenue growth is sluggish at {value:.1%}, which is unappealing for a growth investor."

    # Factors: trailing PE and earnings growth, combined into the PEG ratio (PE / growth).
    def _score_peg(self, trailing_pe: float | None, earnings_growth: float | None) -> tuple[int, str]:
        """Score the PEG ratio (PE / growth rate), out of 40. Lynch's signature metric:
        a higher PE is fine as long as growth justifies it."""
        if trailing_pe is None or trailing_pe <= 0 or earnings_growth is None or earnings_growth <= 0:
            return 16, "PEG ratio is unavailable, so price-to-growth is harder to judge."

        # PEG divides PE by growth in whole percentage points (a PE of 30 at 30%
        # growth is a PEG of 1.0), so the fraction-style 0.30 is scaled up to 30.
        peg = trailing_pe / (earnings_growth * 100)
        if peg <= 1.0:
            return 40, f"PEG ratio is attractive at {peg:.2f}, suggesting the price is justified by growth."
        if peg <= 2.0:
            return 25, f"PEG ratio is fair at {peg:.2f}."
        return 8, f"PEG ratio is expensive at {peg:.2f}, meaning the price is outrunning growth."

    # Factor: earnings growth (profit growth).
    def _score_earnings_growth(self, value: float | None) -> tuple[int, str]:
        """Score earnings growth, out of 25. A company should be turning growth into profit."""
        if value is None:
            return 10, "Earnings growth is unavailable."
        if value >= 0.15:
            return 25, f"Earnings growth is strong at {value:.1%}."
        if value >= 0.05:
            return 16, f"Earnings growth is moderate at {value:.1%}."
        return 6, f"Earnings growth is weak at {value:.1%}."

    def _score_to_signal(self, score: int) -> Signal:
        """Map the combined score to a coarse buy/hold/sell recommendation."""
        if score >= 70:
            return "buy"
        if score >= 45:
            return "hold"
        return "sell"
