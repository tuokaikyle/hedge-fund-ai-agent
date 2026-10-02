"""Command-line entrypoint: parse arguments, run the agents, print the report.

Run it with `uv run simple-hedge-fund AAPL MSFT`. Typer reads the type hints
on main() to build the argument parser and the --help text for us.
"""

from __future__ import annotations

import typer

from simple_hedge_fund.agents.peter_lynch import PeterLynchAgent
from simple_hedge_fund.agents.warren_buffett import WarrenBuffettAgent
from simple_hedge_fund.data.yfinance_service import YFinanceService
from simple_hedge_fund.output import render_analysis


# --- added in lesson 07 ---
def app() -> None:
    """Entry point for the `simple-hedge-fund` command (see pyproject.toml)."""
    typer.run(main)


def main(
    tickers: list[str] = typer.Argument(..., help="Ticker symbols to analyze, for example AAPL MSFT."),
    explanation: bool = typer.Option(True, "--explanation/--no-explanation", help="Show each analyst's key points."),
) -> None:
    """Score each ticker with the Warren Buffett and Peter Lynch agents."""
    service = YFinanceService()
    agents = [WarrenBuffettAgent(), PeterLynchAgent()]

    typer.echo("Simple Hedge Fund")
    typer.echo("=" * 17)

    for ticker in tickers:
        snapshot = service.get_snapshot(ticker)
        decisions = [agent.analyze(snapshot) for agent in agents]
        typer.echo("")
        typer.echo(render_analysis(snapshot, decisions, show_explanation=explanation))


if __name__ == "__main__":
    app()
