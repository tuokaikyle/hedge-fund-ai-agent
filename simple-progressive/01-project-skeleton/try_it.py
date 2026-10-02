"""Run this to see the data contract in action: `python try_it.py`."""

from simple_hedge_fund.models import StockSnapshot

snapshot = StockSnapshot(
    ticker="aapl",
    company_name="Apple Inc.",
    current_price=227.5,
    sector="Technology",
)
print(snapshot)
print (111)
print(snapshot.model_dump_json(indent=2))

try:
    StockSnapshot(company_name="Missing ticker")
except Exception as error:
    print("\nValidation caught a missing required field, as expected:")
    print(error)
