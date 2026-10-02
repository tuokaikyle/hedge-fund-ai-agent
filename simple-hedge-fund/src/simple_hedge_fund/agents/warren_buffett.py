"""Buffett-style analyst that scores quality, balance sheet strength, and valuation."""

from __future__ import annotations

from pydantic import BaseModel, Field

from simple_hedge_fund.llm.base import StructuredLLM
from simple_hedge_fund.models import AnalystDecision, Signal, StockSnapshot


class BuffettResponse(BaseModel):
    """Structured schema expected back from the optional LLM call."""
    signal: Signal
    confidence: int = Field(ge=0, le=100)
    reasoning: str
    key_points: list[str] = Field(default_factory=list)


class WarrenBuffettAgent:
    """Apply a Buffett-flavored heuristic, then optionally refine it with an LLM."""
    name = "Warren Buffett"

    def analyze(self, snapshot: StockSnapshot, llm: StructuredLLM | None) -> AnalystDecision:
        """Return a heuristic decision or an LLM-backed structured response."""
        score, notes = self._score_snapshot(snapshot)
        fallback_decision = self._build_fallback_decision(snapshot, score, notes)

        if llm is None:
            return fallback_decision

        system_prompt = (
            "You are a simplified Warren Buffett style stock analyst. "
            "Use durable-business, profitability, debt discipline, and valuation logic. "
            "Stay close to the supplied heuristic baseline unless the metrics clearly contradict it."
        )
        user_prompt = self._build_user_prompt(snapshot, score, notes, fallback_decision.signal)

        try:
            response = llm.invoke(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_model=BuffettResponse,
            )
        except Exception:
            return fallback_decision

        return AnalystDecision(
            analyst=self.name,
            signal=response.signal,
            confidence=response.confidence,
            score=score,
            reasoning=response.reasoning,
            key_points=response.key_points[:4],
            used_llm=True,
        )

    def _score_snapshot(self, snapshot: StockSnapshot) -> tuple[int, list[str]]:
        """Combine the core Buffett-style subscores into a capped 0-100 score."""
        score = 0
        notes: list[str] = []

        score += self._score_roe(snapshot.return_on_equity, notes)
        score += self._score_debt(snapshot.debt_to_equity, notes)
        score += self._score_margins(snapshot.profit_margin, snapshot.operating_margin, notes)
        score += self._score_liquidity(snapshot.current_ratio, notes)
        score += self._score_valuation(snapshot.trailing_pe, snapshot.current_price, snapshot.target_mean_price, notes)

        return min(score, 100), notes

    def _build_fallback_decision(self, snapshot: StockSnapshot, score: int, notes: list[str]) -> AnalystDecision:
        """Turn the heuristic score into the app's shared decision model."""
        signal = self._score_to_signal(score)
        confidence = self._confidence_from_score(score, signal)
        reasoning = (
            f"Buffett-style view on {snapshot.ticker}: {notes[0]} "
            f"{notes[1] if len(notes) > 1 else ''} "
            f"Overall this looks like a {signal} based on quality, balance sheet strength, and valuation."
        ).strip()

        return AnalystDecision(
            analyst=self.name,
            signal=signal,
            confidence=confidence,
            score=score,
            reasoning=" ".join(reasoning.split()),
            key_points=notes[:4],
            used_llm=False,
        )

    def _build_user_prompt(self, snapshot: StockSnapshot, score: int, notes: list[str], baseline_signal: Signal) -> str:
        """Give the LLM the same data and heuristic baseline used by the rule-based path."""
        return "\n".join(
            [
                f"Ticker: {snapshot.ticker}",
                f"Company: {snapshot.company_name}",
                f"Sector: {snapshot.sector or 'Unknown'}",
                f"Current price: {snapshot.current_price}",
                f"Target mean price: {snapshot.target_mean_price}",
                f"Trailing PE: {snapshot.trailing_pe}",
                f"Return on equity: {snapshot.return_on_equity}",
                f"Profit margin: {snapshot.profit_margin}",
                f"Operating margin: {snapshot.operating_margin}",
                f"Current ratio: {snapshot.current_ratio}",
                f"Debt to equity: {snapshot.debt_to_equity}",
                f"Heuristic score: {score}/100",
                f"Heuristic signal: {baseline_signal}",
                "Heuristic notes:",
                *[f"- {note}" for note in notes],
                "Return a concise structured answer with a signal, confidence, reasoning, and 2 to 4 key points.",
            ]
        )

    def _score_roe(self, value: float | None, notes: list[str]) -> int:
        """Score capital efficiency, which is central to the Buffett profile."""
        if value is None:
            notes.append("ROE is unavailable, so business quality is harder to judge.")
            return 8
        if value >= 0.18:
            notes.append(f"ROE is strong at {value:.1%}, which suggests efficient use of shareholder capital.")
            return 25
        if value >= 0.12:
            notes.append(f"ROE is respectable at {value:.1%}, though not exceptional.")
            return 18
        notes.append(f"ROE is weak at {value:.1%}, which is not ideal for a Buffett-style profile.")
        return 6

    def _score_debt(self, value: float | None, notes: list[str]) -> int:
        """Reward conservative leverage and penalize stretched balance sheets."""
        if value is None:
            notes.append("Debt-to-equity is unavailable, so leverage risk is less clear.")
            return 8
        if value <= 0.5:
            notes.append(f"Debt-to-equity is conservative at {value:.2f}.")
            return 20
        if value <= 1.0:
            notes.append(f"Debt-to-equity is manageable at {value:.2f}.")
            return 14
        notes.append(f"Debt-to-equity is elevated at {value:.2f}, which weakens the balance-sheet story.")
        return 5

    def _score_margins(self, profit_margin: float | None, operating_margin: float | None, notes: list[str]) -> int:
        """Score profitability from both bottom-line and operating perspectives."""
        score = 0
        if profit_margin is None:
            notes.append("Profit margin is unavailable.")
            score += 6
        elif profit_margin >= 0.15:
            notes.append(f"Profit margin is healthy at {profit_margin:.1%}.")
            score += 12
        elif profit_margin >= 0.08:
            notes.append(f"Profit margin is acceptable at {profit_margin:.1%}.")
            score += 8
        else:
            notes.append(f"Profit margin is thin at {profit_margin:.1%}.")
            score += 3

        if operating_margin is None:
            notes.append("Operating margin is unavailable.")
            score += 6
        elif operating_margin >= 0.15:
            notes.append(f"Operating margin is strong at {operating_margin:.1%}.")
            score += 13
        elif operating_margin >= 0.1:
            notes.append(f"Operating margin is decent at {operating_margin:.1%}.")
            score += 9
        else:
            notes.append(f"Operating margin is weak at {operating_margin:.1%}.")
            score += 3

        return score

    def _score_liquidity(self, value: float | None, notes: list[str]) -> int:
        """Use current ratio as a small balance-sheet safety check."""
        if value is None:
            notes.append("Current ratio is unavailable.")
            return 4
        if value >= 1.5:
            notes.append(f"Liquidity looks comfortable with a current ratio of {value:.2f}.")
            return 10
        if value >= 1.0:
            notes.append(f"Liquidity is serviceable with a current ratio of {value:.2f}.")
            return 7
        notes.append(f"Liquidity looks tight with a current ratio of {value:.2f}.")
        return 3

    def _score_valuation(
        self,
        trailing_pe: float | None,
        current_price: float | None,
        target_mean_price: float | None,
        notes: list[str],
    ) -> int:
        """Blend a simple PE check with analyst target upside as a rough valuation anchor."""
        score = 0
        if trailing_pe is None:
            notes.append("Trailing PE is unavailable, so valuation is harder to compare.")
            score += 8
        elif 0 < trailing_pe <= 20:
            notes.append(f"Trailing PE of {trailing_pe:.1f} looks reasonable for a quality business.")
            score += 12
        elif trailing_pe <= 28:
            notes.append(f"Trailing PE of {trailing_pe:.1f} is fair but not especially cheap.")
            score += 8
        else:
            notes.append(f"Trailing PE of {trailing_pe:.1f} looks expensive for a Buffett-style entry point.")
            score += 3

        if current_price is None or target_mean_price is None or current_price == 0:
            notes.append("Analyst target data is unavailable for a rough price anchor.")
            score += 4
            return score

        upside = (target_mean_price - current_price) / current_price
        if upside >= 0.15:
            notes.append(f"Target price suggests about {upside:.1%} upside from current levels.")
            score += 8
        elif upside >= 0.0:
            notes.append(f"Target price suggests only modest upside of {upside:.1%}.")
            score += 5
        else:
            notes.append(f"Target price suggests downside of {upside:.1%}, which reduces the margin of safety.")
            score += 1
        return score

    def _score_to_signal(self, score: int) -> Signal:
        """Map the heuristic score to a coarse buy/hold/sell recommendation."""
        if score >= 70:
            return "buy"
        if score >= 45:
            return "hold"
        return "sell"

    def _confidence_from_score(self, score: int, signal: Signal) -> int:
        """Increase confidence as the score moves farther from the hold range."""
        if signal == "hold":
            return min(80, max(50, 55 + abs(score - 55) // 2))
        return min(95, max(55, 60 + abs(score - 50) // 2))
