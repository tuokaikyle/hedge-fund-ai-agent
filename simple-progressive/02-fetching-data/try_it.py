"""Run this to fetch a real snapshot: `python try_it.py AAPL`."""

import sys

from simple_hedge_fund.data.yfinance_service import YFinanceService

ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"

service = YFinanceService()
snapshot = service.get_snapshot(ticker)

print(snapshot)
print(snapshot.model_dump_json(indent=2))
