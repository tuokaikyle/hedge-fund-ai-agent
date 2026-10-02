"""Translate raw yfinance objects into the app's normalized stock snapshot model."""

from __future__ import annotations

from typing import Any

import yfinance as yf

from simple_hedge_fund.models import StockSnapshot


class YFinanceService:
    """Fetches and normalizes a small stock snapshot from yfinance."""

    def get_snapshot(self, ticker: str) -> StockSnapshot:
        """Collect the subset of company, valuation, growth, and headline fields the agents use."""
        symbol = ticker.upper()
        ticker_client = yf.Ticker(symbol)
        info = self._safe_mapping(getattr(ticker_client, "info", {}))
        fast_info = self._safe_mapping(getattr(ticker_client, "fast_info", {}))
        news = getattr(ticker_client, "news", []) or []

        current_price = self._first_float(
            info.get("currentPrice"),
            info.get("regularMarketPrice"),
            fast_info.get("lastPrice"),
            fast_info.get("regularMarketPreviousClose"),
        )

        revenue_growth = self._first_float(
            info.get("revenueGrowth"),
            self._extract_growth(getattr(ticker_client, "income_stmt", None), ["Total Revenue"]),
        )
        earnings_growth = self._first_float(
            info.get("earningsGrowth"),
            self._extract_growth(getattr(ticker_client, "income_stmt", None), ["Net Income", "Diluted EPS"]),
        )

        return StockSnapshot(
            ticker=symbol,
            company_name=str(info.get("longName") or info.get("shortName") or symbol),
            sector=self._string_or_none(info.get("sector")),
            business_summary=self._string_or_none(info.get("longBusinessSummary")),
            current_price=current_price,
            target_mean_price=self._first_float(info.get("targetMeanPrice")),
            market_cap=self._first_float(info.get("marketCap"), fast_info.get("marketCap")),
            trailing_pe=self._first_float(info.get("trailingPE")),
            forward_pe=self._first_float(info.get("forwardPE")),
            return_on_equity=self._first_float(info.get("returnOnEquity")),
            profit_margin=self._first_float(info.get("profitMargins")),
            operating_margin=self._first_float(info.get("operatingMargins")),
            current_ratio=self._first_float(info.get("currentRatio")),
            debt_to_equity=self._normalize_debt_to_equity(info.get("debtToEquity")),
            revenue_growth=revenue_growth,
            earnings_growth=earnings_growth,
            recent_headlines=self._extract_headlines(news),
        )


    def _safe_mapping(self, value: Any) -> dict[str, Any]:
        """Best-effort conversion of third-party objects into dictionaries."""
        if isinstance(value, dict):
            return value
        try:
            return dict(value)
        except Exception:
            return {}


    def _first_float(self, *values: Any) -> float | None:
        """Return the first value that can be interpreted as a float."""
        for value in values:
            number = self._safe_float(value)
            if number is not None:
                return number
        return None


    def _safe_float(self, value: Any) -> float | None:
        """Convert loosely typed values from yfinance into floats when possible."""
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None


    def _normalize_debt_to_equity(self, value: Any) -> float | None:
        """Convert percentage-style debt-to-equity values into ratio-style values."""
        raw_value = self._safe_float(value)
        if raw_value is None:
            return None
        if raw_value > 10:
            return raw_value / 100.0
        return raw_value


    def _extract_growth(self, statement: Any, row_names: list[str]) -> float | None:
        """Estimate simple growth from the latest and oldest available statement values."""
        if statement is None or getattr(statement, "empty", True):
            return None

        for row_name in row_names:
            if row_name not in statement.index:
                continue

            row = statement.loc[row_name].dropna()
            if len(row) < 2:
                continue

            latest = self._safe_float(row.iloc[0])
            older = self._safe_float(row.iloc[-1])
            if latest is None or older in (None, 0.0):
                continue

            return (latest - older) / abs(older)

        return None


    def _extract_headlines(self, news_items: list[Any]) -> list[str]:
        """Keep only a short headline sample for display and prompts."""
        headlines: list[str] = []
        for item in news_items[:3]:
            title = self._extract_title(item)
            if title:
                headlines.append(title)
        return headlines


    def _extract_title(self, item: Any) -> str | None:
        """Handle the different title shapes returned by yfinance news items."""
        if isinstance(item, dict):
            direct_title = item.get("title")
            if isinstance(direct_title, str) and direct_title.strip():
                return direct_title.strip()

            content = item.get("content")
            if isinstance(content, dict):
                nested_title = content.get("title")
                if isinstance(nested_title, str) and nested_title.strip():
                    return nested_title.strip()

        return None


    def _string_or_none(self, value: Any) -> str | None:
        """Normalize blank-like values to None."""
        if value is None:
            return None
        text = str(value).strip()
        return text or None
