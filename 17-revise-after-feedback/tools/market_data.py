"""Small data functions that agents can use as tools."""

import yfinance as yf
from langchain_core.tools import tool


# changed in lesson 12, 13
@tool
def get_business_summary(ticker: str) -> dict:
    """Fetch a company's business description for the given stock ticker."""
    summary = yf.Ticker(ticker).info.get("longBusinessSummary")
    return {"ticker": ticker.upper(), "business_summary": summary}


# changed in lesson 14
@tool
def get_revenue_history(ticker: str) -> dict:
    """Fetch annual revenue in reported currency units, oldest year first."""
    statement = yf.Ticker(ticker).income_stmt
    if "Total Revenue" not in statement.index:
        return {"ticker": ticker.upper(), "annual_revenue": []}
    revenue = statement.loc["Total Revenue"].dropna().sort_index()
    return {
        "ticker": ticker.upper(),
        "annual_revenue": [
            {"period_end": date.date().isoformat(), "revenue": float(value)}
            for date, value in revenue.items()
        ],
    }
