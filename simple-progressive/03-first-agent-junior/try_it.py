"""Run this to see the first agent score a real ticker: `python try_it.py AAPL`."""

import sys

from simple_hedge_fund.agents.junior import JuniorAgent
from simple_hedge_fund.data.yfinance_service import YFinanceService

ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"

service = YFinanceService()
snapshot = service.get_snapshot(ticker)

agent = JuniorAgent()
decision = agent.analyze(snapshot)

print(f"{decision.analyst} on {snapshot.ticker}: {decision.signal.upper()} (score {decision.score}/100)")
print(f"Reasoning: {decision.reasoning}")
