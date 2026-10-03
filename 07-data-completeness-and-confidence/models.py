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


class AnalystDecision(BaseModel):
    """One analyst's signal, score, data completeness, confidence, and explanation."""

    analyst: str
    signal: Signal
    score: int = Field(ge=0, le=100)
    data_completeness: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    reasoning: str
