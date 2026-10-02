"""Command-line entrypoint: parse arguments, run the orchestrator, print the report.

Run it with `uv run simple-hedge-fund AAPL MSFT`. Typer reads the type hints
on main() to build the argument parser and the --help text for us.
"""

from __future__ import annotations

import typer

from simple_hedge_fund.orchestrator import SimpleHedgeFundOrchestrator
from simple_hedge_fund.output import render_analysis


# --- carried forward from lesson 07, unchanged ---
def app() -> None:
    """Entry point for the `simple-hedge-fund` command (see pyproject.toml)."""
    typer.run(main)


# --- modified in lesson 08: hands the work to the orchestrator instead of running agents itself ---
def main(
    tickers: list[str] = typer.Argument(..., help="Ticker symbols to analyze, for example AAPL MSFT."),
    explanation: bool = typer.Option(True, "--explanation/--no-explanation", help="Show each analyst's key points."),
) -> None:
    """Score each ticker with every analyst and combine their calls into one recommendation."""
    orchestrator = SimpleHedgeFundOrchestrator()
    analyses = orchestrator.run(tickers)

    typer.echo("Simple Hedge Fund")
    typer.echo("=" * 17)

    for analysis in analyses:
        typer.echo("")
        typer.echo(render_analysis(analysis, show_explanation=explanation))


if __name__ == "__main__":
    app()
