"""Small data functions that agents can use as tools."""

import yfinance as yf
from langchain_core.tools import tool


# changed in lesson 12, 13
@tool
def get_business_summary(ticker: str) -> dict:
    """Fetch a company's business description for the given stock ticker."""
    summary = yf.Ticker(ticker).info.get("longBusinessSummary")
    return {"ticker": ticker.upper(), "business_summary": summary}
