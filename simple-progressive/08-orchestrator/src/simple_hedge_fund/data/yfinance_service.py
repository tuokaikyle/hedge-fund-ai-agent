"""Translate raw yfinance objects into the app's normalized stock snapshot model."""

from __future__ import annotations

from simple_hedge_fund.models import StockSnapshot

import yfinance as yf


# --- carried forward from lesson 02, unchanged ---
class YFinanceService:
    """Fetches and normalizes a stock snapshot from yfinance.

    StockSnapshot is already fully widened as of lesson 1, so this service
    populates it in one pass rather than growing over later lessons.
    """

    def get_snapshot(self, ticker: str) -> StockSnapshot:
        """Collect the company, valuation, and quality fields StockSnapshot needs."""
        symbol = ticker.upper()
        ticker_client = yf.Ticker(symbol)
        info = ticker_client.info or {}

        # yfinance reports ROE, margins, and growth as fractions (0.18 = 18%),
        # but debt-to-equity as a percentage (78.4 = 0.784x). Convert it here so
        # every ratio in StockSnapshot uses the same fraction-style units.
        debt_to_equity = info.get("debtToEquity")
        if debt_to_equity is not None:
            debt_to_equity = debt_to_equity / 100

        return StockSnapshot(
            ticker=symbol,
            company_name=info.get("longName") or info.get("shortName") or symbol,
            sector=info.get("sector"),
            business_summary=info.get("longBusinessSummary"),
            current_price=info.get("currentPrice") or info.get("regularMarketPrice"),
            target_mean_price=info.get("targetMeanPrice"),
            market_cap=info.get("marketCap"),
            trailing_pe=info.get("trailingPE"),
            forward_pe=info.get("forwardPE"),
            return_on_equity=info.get("returnOnEquity"),
            profit_margin=info.get("profitMargins"),
            operating_margin=info.get("operatingMargins"),
            current_ratio=info.get("currentRatio"),
            debt_to_equity=debt_to_equity,
            revenue_growth=info.get("revenueGrowth"),
            earnings_growth=info.get("earningsGrowth"),
        )
