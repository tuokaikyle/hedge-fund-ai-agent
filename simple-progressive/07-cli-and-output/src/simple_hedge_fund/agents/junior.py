"""A deliberately simple agent, used to learn the agent shape before meeting
real investor personas in later lessons.

No LLM here yet — this lesson is about an agent as a plain, deterministic
function: read a StockSnapshot in, produce an AnalystDecision out. Lesson 9
introduces an LLM seam; agents will optionally use it starting there.
"""

from __future__ import annotations

from simple_hedge_fund.models import AnalystDecision, Signal, StockSnapshot


# --- carried forward from lesson 03, unchanged ---
class JuniorAgent:
    """Scores a stock using a single metric: return on equity (ROE).

    This is intentionally the smallest useful agent: one input, one score,
    one signal. Lesson 4's SeniorAgent builds on this same shape but
    combines several metrics instead of one.
    """
    name = "Junior"

    def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
        """Score the snapshot's ROE and turn it into a buy/hold/sell decision."""
        score, note = self._score_roe(snapshot.return_on_equity)
        signal = self._score_to_signal(score)

        return AnalystDecision(
            analyst=self.name,
            signal=signal,
            score=score,
            reasoning=f"Junior's view on {snapshot.ticker}: {note}",
            key_points=[note],
        )

    def _score_roe(self, value: float | None) -> tuple[int, str]:
        """Score capital efficiency: how much profit a company makes per dollar of equity."""
        if value is None:
            return 40, "ROE is unavailable, so this is a low-confidence guess."
        if value >= 0.18:
            return 90, f"ROE is strong at {value:.1%}."
        if value >= 0.12:
            return 65, f"ROE is respectable at {value:.1%}."
        return 30, f"ROE is weak at {value:.1%}."

    def _score_to_signal(self, score: int) -> Signal:
        """Map the score to a coarse buy/hold/sell recommendation."""
        if score >= 70:
            return "buy"
        if score >= 45:
            return "hold"
        return "sell"
