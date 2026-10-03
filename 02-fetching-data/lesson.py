"""Fetch and print a real stock snapshot."""

from yfinance_service import YFinanceService


def run(ticker: str) -> None:
    snapshot = YFinanceService().get_snapshot(ticker)
    print(snapshot.model_dump_json(indent=2, exclude_none=True))
