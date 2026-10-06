"""A first, one-metric analyst agent."""

from models import AnalystDecision, Signal, StockSnapshot


class JuniorAgent:
    def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
        roe = snapshot.return_on_equity

        if roe is None:
            score = 50
            reasoning = "ROE is unavailable, so there is no basis for a call."
        elif roe >= 0.18:
            score = 90
            reasoning = f"ROE is strong at {roe:.1%}."
        elif roe >= 0.12:
            score = 65
            reasoning = f"ROE is moderate at {roe:.1%}."
        else:
            score = 30
            reasoning = f"ROE is low at {roe:.1%}."

        if score >= 70:
            signal: Signal = "buy"
        elif score >= 45:
            signal = "hold"
        else:
            signal = "sell"

        return AnalystDecision(
            analyst="Junior",
            signal=signal,
            score=score,
            reasoning=reasoning,
        )
