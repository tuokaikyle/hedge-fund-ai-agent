"""Fetch a few stock fields from Yahoo Finance."""

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

        return StockSnapshot(
            ticker=symbol,
            company_name=info.get("longName") or info.get("shortName") or symbol,
            sector=info.get("sector"),
            current_price=price,
            market_cap=info.get("marketCap"),
            return_on_equity=info.get("returnOnEquity"),
        )
