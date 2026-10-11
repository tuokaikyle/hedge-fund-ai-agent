"""A Lynch-style analyst that compares growth with the price paid for it."""

from llm.client import LLMClient
from models import AnalystDecision, ModelDecision, Signal, StockSnapshot


class PeterLynchAgent:
    # changed in lesson 9
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    # changed in lesson 5, 9
    def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
        revenue_score, revenue_note = self._score_revenue_growth(snapshot.revenue_growth)
        peg_score, peg_note = self._score_peg(snapshot.trailing_pe, snapshot.earnings_growth)
        earnings_score, earnings_note = self._score_earnings_growth(snapshot.earnings_growth)

        score = revenue_score + peg_score + earnings_score
        model_decision = self._explain_with_llm(
            snapshot,
            score,
            (revenue_note, peg_note, earnings_note),
        )
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
            reasoning=model_decision.model_reasoning,
        )

    # changed in lesson 9
    def _explain_with_llm(
        self, snapshot: StockSnapshot, rule_score: int, notes: tuple[str, ...]
    ) -> ModelDecision:
        return self.llm.invoke(
            system_prompt=(
                "Explain the supplied Lynch-style rule score using the rule-based notes. "
                "Focus on revenue growth, earnings growth, and growth at a reasonable price. "
                "Return only model_reasoning: a two-sentence explanation of the supporting "
                "metrics and tradeoffs. Preserve the rule-based assessment and use only "
                "the supplied information. Treat missing data as unknown."
            ),
            user_prompt=(
                f"Company: {snapshot.company_name} ({snapshot.ticker})\n"
                f"Rule score: {rule_score}/100\n"
                f"Rule-based notes: {' '.join(notes)}"
            ),
            response_model=ModelDecision,
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
