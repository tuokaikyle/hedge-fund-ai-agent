"""Lynch-style analyst that emphasizes understandable growth at a reasonable price."""

from __future__ import annotations

from pydantic import BaseModel, Field

from simple_hedge_fund.llm.base import StructuredLLM
from simple_hedge_fund.models import AnalystDecision, Signal, StockSnapshot


class LynchResponse(BaseModel):
    """Structured schema expected back from the optional LLM call."""
    signal: Signal
    confidence: int = Field(ge=0, le=100)
    reasoning: str
    key_points: list[str] = Field(default_factory=list)


class PeterLynchAgent:
    """Apply a Lynch-flavored heuristic, then optionally refine it with an LLM."""
    name = "Peter Lynch"

    def analyze(self, snapshot: StockSnapshot, llm: StructuredLLM | None) -> AnalystDecision:
        """Return a heuristic decision or an LLM-backed structured response."""
        score, notes = self._score_snapshot(snapshot)
        fallback_decision = self._build_fallback_decision(snapshot, score, notes)

        if llm is None:
            return fallback_decision

        system_prompt = (
            "You are a simplified Peter Lynch style stock analyst. "
            "Focus on understandable growth, reasonable valuation, and manageable debt. "
            "Use the heuristic baseline as an anchor unless the metrics strongly suggest otherwise."
        )
        user_prompt = self._build_user_prompt(snapshot, score, notes, fallback_decision.signal)

        try:
            response = llm.invoke(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_model=LynchResponse,
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
        """Combine growth, debt, valuation, clarity, and headlines into one score."""
        score = 0
        notes: list[str] = []

        score += self._score_growth(snapshot.revenue_growth, snapshot.earnings_growth, notes)
        score += self._score_debt(snapshot.debt_to_equity, notes)
        score += self._score_peg(snapshot.trailing_pe, snapshot.earnings_growth, notes)
        score += self._score_business_clarity(snapshot.business_summary, snapshot.sector, notes)
        score += self._score_headlines(snapshot.recent_headlines, notes)

        return min(score, 100), notes

    def _build_fallback_decision(self, snapshot: StockSnapshot, score: int, notes: list[str]) -> AnalystDecision:
        """Turn the heuristic score into the app's shared decision model."""
        signal = self._score_to_signal(score)
        confidence = self._confidence_from_score(score, signal)
        reasoning = (
            f"Lynch-style view on {snapshot.ticker}: {notes[0]} "
            f"{notes[1] if len(notes) > 1 else ''} "
            f"Overall this looks like a {signal} based on growth, debt, and valuation at a reasonable price."
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
                f"Trailing PE: {snapshot.trailing_pe}",
                f"Revenue growth: {snapshot.revenue_growth}",
                f"Earnings growth: {snapshot.earnings_growth}",
                f"Debt to equity: {snapshot.debt_to_equity}",
                f"Business summary: {snapshot.business_summary or 'Unavailable'}",
                f"Recent headlines: {snapshot.recent_headlines}",
                f"Heuristic score: {score}/100",
                f"Heuristic signal: {baseline_signal}",
                "Heuristic notes:",
                *[f"- {note}" for note in notes],
                "Return a concise structured answer with a signal, confidence, reasoning, and 2 to 4 key points.",
            ]
        )

    def _score_growth(self, revenue_growth: float | None, earnings_growth: float | None, notes: list[str]) -> int:
        """Reward businesses showing decent top-line and bottom-line growth."""
        score = 0
        if revenue_growth is None:
            notes.append("Revenue growth is unavailable.")
            score += 8
        elif revenue_growth >= 0.15:
            notes.append(f"Revenue growth is strong at {revenue_growth:.1%}.")
            score += 20
        elif revenue_growth >= 0.05:
            notes.append(f"Revenue growth is positive at {revenue_growth:.1%}.")
            score += 14
        else:
            notes.append(f"Revenue growth is weak at {revenue_growth:.1%}.")
            score += 5

        if earnings_growth is None:
            notes.append("Earnings growth is unavailable.")
            score += 8
        elif earnings_growth >= 0.15:
            notes.append(f"Earnings growth is strong at {earnings_growth:.1%}.")
            score += 20
        elif earnings_growth >= 0.05:
            notes.append(f"Earnings growth is positive at {earnings_growth:.1%}.")
            score += 14
        else:
            notes.append(f"Earnings growth is weak at {earnings_growth:.1%}.")
            score += 5

        return score

    def _score_debt(self, value: float | None, notes: list[str]) -> int:
        """Favor growth funded without excessive leverage."""
        if value is None:
            notes.append("Debt-to-equity is unavailable.")
            return 8
        if value <= 0.5:
            notes.append(f"Debt-to-equity is low at {value:.2f}, which supports growth.")
            return 15
        if value <= 1.0:
            notes.append(f"Debt-to-equity is manageable at {value:.2f}.")
            return 10
        notes.append(f"Debt-to-equity is high at {value:.2f}, which makes the growth story less attractive.")
        return 4

    def _score_peg(self, trailing_pe: float | None, earnings_growth: float | None, notes: list[str]) -> int:
        """Approximate Lynch's GARP lens with a simple PEG estimate."""
        if trailing_pe is None or earnings_growth is None or earnings_growth <= 0:
            notes.append("PEG ratio could not be estimated from the available data.")
            return 8

        peg = trailing_pe / (earnings_growth * 100)
        if peg <= 1.5:
            notes.append(f"Estimated PEG is {peg:.2f}, which looks reasonable for growth.")
            return 20
        if peg <= 2.5:
            notes.append(f"Estimated PEG is {peg:.2f}, which is acceptable but not cheap.")
            return 12
        notes.append(f"Estimated PEG is {peg:.2f}, which looks expensive for Lynch-style GARP investing.")
        return 4

    def _score_business_clarity(self, summary: str | None, sector: str | None, notes: list[str]) -> int:
        """Reward companies that are understandable from the available description."""
        if summary and sector:
            notes.append(f"The company story is at least understandable at a high level in the {sector} sector.")
            return 15
        if summary or sector:
            notes.append("The business appears somewhat understandable, but context is incomplete.")
            return 10
        notes.append("The business description is sparse, which makes a Lynch-style read harder.")
        return 5

    def _score_headlines(self, headlines: list[str], notes: list[str]) -> int:
        """Use a small news sample as a lightweight context signal."""
        if not headlines:
            notes.append("Recent headlines were not available.")
            return 5
        notes.append(f"Recent headline sample: {headlines[0]}")
        return 10

    def _score_to_signal(self, score: int) -> Signal:
        """Map the heuristic score to a coarse buy/hold/sell recommendation."""
        if score >= 68:
            return "buy"
        if score >= 45:
            return "hold"
        return "sell"

    def _confidence_from_score(self, score: int, signal: Signal) -> int:
        """Increase confidence as the score moves farther from the hold range."""
        if signal == "hold":
            return min(78, max(50, 54 + abs(score - 56) // 2))
        return min(95, max(55, 60 + abs(score - 50) // 2))
