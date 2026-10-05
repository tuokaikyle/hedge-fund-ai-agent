"""A Buffett-style analyst that checks business quality and price."""

from models import AnalystDecision, Signal, StockSnapshot


class WarrenBuffettAgent:
    def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
        roe_score, roe_note = self._score_roe(snapshot.return_on_equity)
        debt_score, debt_note = self._score_debt(snapshot.debt_to_equity)
        margin_score, margin_note = self._score_margins(
            snapshot.profit_margin, snapshot.operating_margin
        )
        price_score, price_note = self._score_price(snapshot.trailing_pe)

        score = roe_score + debt_score + margin_score + price_score
        if score >= 70:
            signal: Signal = "buy"
        elif score >= 45:
            signal = "hold"
        else:
            signal = "sell"

        return AnalystDecision(
            analyst="Warren Buffett",
            signal=signal,
            score=score,
            reasoning=" ".join((roe_note, debt_note, margin_note, price_note)),
        )

    def _score_roe(self, value: float | None) -> tuple[int, str]:
        if value is None:
            return 15, "ROE is unavailable."
        if value >= 0.18:
            return 30, f"ROE is strong at {value:.1%}."
        if value >= 0.12:
            return 20, f"ROE is moderate at {value:.1%}."
        return 8, f"ROE is low at {value:.1%}."

    def _score_debt(self, value: float | None) -> tuple[int, str]:
        if value is None:
            return 12, "Debt-to-equity is unavailable."
        if value <= 0.5:
            return 25, f"Debt-to-equity is low at {value:.2f}."
        if value <= 1.0:
            return 17, f"Debt-to-equity is moderate at {value:.2f}."
        return 6, f"Debt-to-equity is high at {value:.2f}."

    def _score_margins(
        self, profit: float | None, operating: float | None
    ) -> tuple[int, str]:
        if profit is None or operating is None:
            return 12, "Profit or operating margin is unavailable."
        if profit >= 0.15 and operating >= 0.15:
            return 25, f"Margins are healthy: profit {profit:.1%}, operating {operating:.1%}."
        if profit >= 0.08 or operating >= 0.10:
            return 16, f"Margins are moderate: profit {profit:.1%}, operating {operating:.1%}."
        return 6, f"Margins are low: profit {profit:.1%}, operating {operating:.1%}."

    def _score_price(self, trailing_pe: float | None) -> tuple[int, str]:
        if trailing_pe is None or trailing_pe <= 0:
            return 10, "Trailing P/E is unavailable; the price check is incomplete."
        if trailing_pe <= 20:
            return 20, f"Trailing P/E is {trailing_pe:.1f}, a reasonable price by this rule."
        if trailing_pe <= 28:
            return 13, f"Trailing P/E is {trailing_pe:.1f}, a fair price by this rule."
        return 5, f"Trailing P/E is {trailing_pe:.1f}, an expensive price by this rule."
