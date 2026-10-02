"""CLI entrypoint that wires config, orchestration, and terminal output."""

from __future__ import annotations

from pathlib import Path

import typer

from simple_hedge_fund.config import load_app_config
from simple_hedge_fund.orchestrator import SimpleHedgeFundOrchestrator
from simple_hedge_fund.output import render_report


def app() -> None:
    """Expose the Typer app for the console script and module entrypoint."""
    typer.run(main)


def main(
    tickers: list[str] = typer.Argument(None, help="Ticker symbols to analyze, for example AAPL MSFT."),
    config: Path | None = typer.Option(None, "--config", help="Path to a TOML config file."),
    provider: str | None = typer.Option(None, "--provider", help="LLM provider name, for example openai."),
    model: str | None = typer.Option(None, "--model", help="Model name for the chosen provider."),
    use_llm: bool | None = typer.Option(None, "--llm/--no-llm", help="Enable or disable LLM calls."),
    reasoning: bool | None = typer.Option(None, "--reasoning/--no-reasoning", help="Show detailed reasoning."),
) -> None:
    """Run the simplified hedge fund analysis."""
    settings = load_app_config(
        config_path=config,
        provider=provider,
        model=model,
        use_llm=use_llm,
        reasoning=reasoning,
    )

    # CLI args override config defaults; otherwise use the configured ticker list.
    resolved_tickers = [ticker.upper() for ticker in tickers] if tickers else settings.default_tickers
    if not resolved_tickers:
        raise typer.BadParameter("Provide at least one ticker or set default_tickers in the config file.")

    orchestrator = SimpleHedgeFundOrchestrator(settings)
    result = orchestrator.run(resolved_tickers)
    typer.echo(render_report(result, show_reasoning=settings.reasoning))


if __name__ == "__main__":
    app()
