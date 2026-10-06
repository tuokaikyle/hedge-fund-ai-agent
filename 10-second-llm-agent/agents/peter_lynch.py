"""A Lynch-style analyst that compares growth with the price paid for it."""

from llm.client import LLMClient
from utils.confidence import decision_confidence
from utils.data_completeness import data_completeness
from models import AnalystDecision, LynchModelDecision, Signal, StockSnapshot


class PeterLynchAgent:
    # changed in lesson 10
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    # changed in lesson 5, 6, 10
    def analyze(self, snapshot: StockSnapshot) -> AnalystDecision:
        revenue_score, revenue_note = self._score_revenue_growth(snapshot.revenue_growth)
        peg_score, peg_note = self._score_peg(snapshot.trailing_pe, snapshot.earnings_growth)
        earnings_score, earnings_note = self._score_earnings_growth(snapshot.earnings_growth)

        rule_score = revenue_score + peg_score + earnings_score
        model_decision = self._decide_with_llm(
            snapshot,
            rule_score,
            (revenue_note, peg_note, earnings_note),
        )
        score = model_decision.score
        if score >= 70:
            signal: Signal = "buy"
        elif score >= 45:
            signal = "hold"
        else:
            signal = "sell"

        completeness = data_completeness(
            snapshot.revenue_growth,
            snapshot.earnings_growth,
            snapshot.trailing_pe,
        )
        return AnalystDecision(
            analyst="Peter Lynch",
            signal=signal,
            score=score,
            data_completeness=completeness,
            confidence=decision_confidence(score, completeness),
            reasoning=model_decision.reasoning,
        )

    # changed in lesson 10
    def _decide_with_llm(
        self, snapshot: StockSnapshot, rule_score: int, notes: tuple[str, ...]
    ) -> LynchModelDecision:
        return self.llm.invoke(
            system_prompt=(
                "Make a Lynch-style assessment from the supplied rule-based notes. "
                "Focus on revenue growth, earnings growth, and growth at a reasonable price. "
                "Return a score from 0 to 100 and a two-sentence explanation. "
                "Use the rule score as a starting point, changing it only when the notes "
                "justify a different assessment. Treat missing data as unknown."
            ),
            user_prompt=(
                f"Company: {snapshot.company_name} ({snapshot.ticker})\n"
                f"Rule score: {rule_score}/100\n"
                f"Rule-based notes: {' '.join(notes)}"
            ),
            response_model=LynchModelDecision,
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
