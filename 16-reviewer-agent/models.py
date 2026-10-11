"""The stock data shape shared by later lessons."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class StockSnapshot(BaseModel):
    """Company and market information in a consistent shape."""

    ticker: str
    company_name: str
    sector: str | None = None
    business_summary: str | None = None
    current_price: float | None = None
    target_mean_price: float | None = None
    market_cap: float | None = None
    trailing_pe: float | None = None
    forward_pe: float | None = None
    return_on_equity: float | None = None
    profit_margin: float | None = None
    operating_margin: float | None = None
    current_ratio: float | None = None
    debt_to_equity: float | None = None
    revenue_growth: float | None = None
    earnings_growth: float | None = None
    recent_headlines: list[str] = Field(default_factory=list)


Signal = Literal["buy", "hold", "sell"]


# changed in lesson 3
class AnalystDecision(BaseModel):
    """One analyst's signal, score, and explanation."""

    analyst: str
    signal: Signal
    score: int = Field(ge=0, le=100)
    reasoning: str


# changed in lesson 7, 15
class FinalRecommendation(BaseModel):
    """The manager's assessment and the signal derived from its score."""

    score: int = Field(ge=0, le=100)
    signal: Signal
    reasoning: str


# changed in lesson 13
class ToolCall(BaseModel):
    """The action Python executed and the evidence it returned."""

    analyst: str
    tool: str
    arguments: dict[str, str]
    result: dict


# changed in lesson 16
class Review(BaseModel):
    """One concrete issue for the manager to address, or no issue."""

    issue: str = Field(description="One concrete evidence issue, or exactly 'no issue'.")


# changed in lesson 6, 7, 13, 16
class TickerAnalysis(BaseModel):
    """One stock snapshot, its analyst decisions, and the combined result."""

    snapshot: StockSnapshot
    analyst_decisions: list[AnalystDecision]
    final_recommendation: FinalRecommendation
    tool_calls: list[ToolCall] = Field(default_factory=list)
    review: Review | None = None


# changed in lesson 10
class LLMJudgment(BaseModel):
    """A model's assessment, before Python derives the signal."""

    score: int = Field(ge=0, le=100)
    reasoning: str
