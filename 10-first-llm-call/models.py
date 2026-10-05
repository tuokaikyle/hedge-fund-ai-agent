"""The stock data shape shared by later lessons."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


# introduced in lesson 01
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


# introduced in lesson 03
# modified in lesson 07
class AnalystDecision(BaseModel):
    """One analyst's signal, score, data completeness, confidence, and explanation."""

    analyst: str
    signal: Signal
    score: int = Field(ge=0, le=100)
    data_completeness: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    reasoning: str


# introduced in lesson 10
class BuffettModelDecision(BaseModel):
    """The two fields Buffett asks the model to decide."""

    score: int = Field(ge=0, le=100)
    reasoning: str


# introduced in lesson 09
class FinalRecommendation(BaseModel):
    """Equal and confidence-weighted views of the analysts' scores."""

    plain_score: int = Field(ge=0, le=100)
    plain_signal: Signal
    weighted_score: int = Field(ge=0, le=100)
    signal: Signal


# introduced in lesson 08
# modified in lesson 09
class TickerAnalysis(BaseModel):
    """One stock snapshot, its analyst decisions, and the combined result."""

    snapshot: StockSnapshot
    analyst_decisions: list[AnalystDecision]
    final_recommendation: FinalRecommendation
