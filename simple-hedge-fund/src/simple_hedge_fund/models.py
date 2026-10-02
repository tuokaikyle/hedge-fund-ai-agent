"""Shared typed models passed between the CLI, data layer, agents, and output."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Signal = Literal["buy", "hold", "sell"]


class AppConfig(BaseModel):
    """Runtime settings resolved from config files, env vars, and CLI flags."""
    provider: str = "openai"
    model: str = "gpt-4.1-mini"
    use_llm: bool = True
    temperature: float = 0.1
    reasoning: bool = True
    default_tickers: list[str] = Field(default_factory=list)
    openai_api_key: str | None = None


class StockSnapshot(BaseModel):
    """Normalized subset of market and company fields used by the analysts."""
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


class AnalystDecision(BaseModel):
    """A single analyst's recommendation plus the reasoning behind it."""
    analyst: str
    signal: Signal
    confidence: int = Field(ge=0, le=100)
    score: int = Field(ge=0, le=100)
    reasoning: str
    key_points: list[str] = Field(default_factory=list)
    used_llm: bool = False


class FinalRecommendation(BaseModel):
    """Combined recommendation produced by the orchestrator."""
    signal: Signal
    confidence: int = Field(ge=0, le=100)
    summary: str


class TickerAnalysis(BaseModel):
    """All intermediate and final analysis artifacts for one ticker."""
    snapshot: StockSnapshot
    analyst_decisions: list[AnalystDecision]
    final_recommendation: FinalRecommendation


class RunResult(BaseModel):
    """Top-level result returned for the full CLI run."""
    provider: str
    model: str
    llm_enabled: bool
    llm_status: str
    analyses: list[TickerAnalysis]
