"""Shared typed models passed between the parts of the app we'll build lesson by lesson."""

from __future__ import annotations

from pydantic import BaseModel, Field


# --- added in lesson 01 ---
class StockSnapshot(BaseModel):
    """Normalized subset of market and company fields used by the analysts.

    This is the full, final shape the finished app uses. We define it wide
    up front so later lessons never need to come back and add fields to
    this model — each new agent just reads more of what's already here.
    Only `ticker` and `company_name` are required; everything else is
    optional because not every data source (or every lesson's fetch logic)
    populates all of it right away.
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
