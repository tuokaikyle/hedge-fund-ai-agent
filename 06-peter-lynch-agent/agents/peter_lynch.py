"""A Lynch-style analyst that compares growth with the price paid for it."""

from models import AnalystDecision, Signal, StockSnapshot


class PeterLynchAgent:
    def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
        revenue_score, revenue_note = self._score_revenue_growth(snapshot.revenue_growth)
        peg_score, peg_note = self._score_peg(snapshot.trailing_pe, snapshot.earnings_growth)
        earnings_score, earnings_note = self._score_earnings_growth(snapshot.earnings_growth)

        score = revenue_score + peg_score + earnings_score
        if score >= 70:
            signal: Signal = "buy"
        elif score >= 45:
            signal = "hold"
        else:
            signal = "sell"

        return AnalystDecision(
            analyst="Peter Lynch",
            signal=signal,
            score=score,
            reasoning=" ".join((revenue_note, peg_note, earnings_note)),
        )

    def _score_revenue_growth(self, value: float | None) -> tuple[int, str]:
        if value is None:
            return 17, "Revenue growth is unavailable."
        if value >= 0.20:
            return 35, f"Revenue growth is strong at {value:.1%}."
        if value >= 0.08:
            return 24, f"Revenue growth is moderate at {value:.1%}."
        return 10, f"Revenue growth is low at {value:.1%}."

    def _score_peg(
        self, trailing_pe: float | None, earnings_growth: float | None
    ) -> tuple[int, str]:
        if trailing_pe is None or trailing_pe <= 0 or earnings_growth is None or earnings_growth <= 0:
            return 20, "PEG estimate is unavailable; positive P/E and earnings growth are needed."

        # Growth is a fraction: 0.30 means 30%, so a P/E of 30 gives PEG 1.0.
        peg = trailing_pe / (earnings_growth * 100)
        if peg <= 1.0:
            return 40, f"Estimated PEG is attractive at {peg:.2f}."
        if peg <= 2.0:
            return 25, f"Estimated PEG is fair at {peg:.2f}."
        return 8, f"Estimated PEG is expensive at {peg:.2f}."

    def _score_earnings_growth(self, value: float | None) -> tuple[int, str]:
        if value is None:
            return 12, "Earnings growth is unavailable."
        if value >= 0.15:
            return 25, f"Earnings growth is strong at {value:.1%}."
        if value >= 0.05:
            return 16, f"Earnings growth is moderate at {value:.1%}."
        return 6, f"Earnings growth is low at {value:.1%}."
