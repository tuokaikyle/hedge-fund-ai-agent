"""Create and print a stock snapshot."""

from models import StockSnapshot


def run(ticker: str) -> None:
    snapshot = StockSnapshot(
        ticker=ticker.upper(),
        company_name="Example Company",
        current_price=100.0,
        sector="Technology",
    )
    print(snapshot.model_dump_json(indent=2))
