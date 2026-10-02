"""Shared typed models passed between the parts of the app we'll build lesson by lesson."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


# --- carried forward from lesson 01, unchanged ---
class StockSnapshot(BaseModel):
    """Normalized subset of market and company fields used by the analysts.

    Full, final shape — see lesson 1 for why this is defined wide up front
    instead of grown gradually.
    """
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


# --- carried forward from lesson 03, unchanged ---
Signal = Literal["buy", "hold", "sell"]


# --- carried forward from lesson 03, unchanged ---
class AnalystDecision(BaseModel):
    """A single analyst's recommendation plus the reasoning behind it."""
    analyst: str
    signal: Signal
    score: int = Field(ge=0, le=100)
    reasoning: str
    key_points: list[str] = Field(default_factory=list)
