"""Fetch the stock fields the agents use from Yahoo Finance."""

import yfinance as yf

from models import StockSnapshot


class YFinanceService:
    def get_snapshot(self, ticker: str) -> StockSnapshot:
        symbol = ticker.upper()
        info = yf.Ticker(symbol).info
        if not info:
            raise ValueError(f"No data returned for {symbol}")

        price = info.get("currentPrice")
        if price is None:
            price = info.get("regularMarketPrice")

        # Yahoo reports debt-to-equity as a percentage; use a ratio like the other fields.
        debt_to_equity = info.get("debtToEquity")
        if debt_to_equity is not None:
            debt_to_equity /= 100

        return StockSnapshot(
            ticker=symbol,
            company_name=info.get("longName") or info.get("shortName") or symbol,
            sector=info.get("sector"),
            current_price=price,
            market_cap=info.get("marketCap"),
            return_on_equity=info.get("returnOnEquity"),
            debt_to_equity=debt_to_equity,
            profit_margin=info.get("profitMargins"),
            operating_margin=info.get("operatingMargins"),
            trailing_pe=info.get("trailingPE"),
            revenue_growth=info.get("revenueGrowth"),
            earnings_growth=info.get("earningsGrowth"),
        )
