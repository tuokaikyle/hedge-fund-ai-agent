"""Resolve runtime settings, run the agents, and show their decisions."""

import argparse
from pathlib import Path

from dotenv import load_dotenv

from config import load_config
from orchestrator import HedgeFundOrchestrator
from output import render_report


# introduced in lesson 14
def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", dest="config_path", type=Path,
                        default=Path(__file__).with_name("config.toml"),
                        help="TOML settings file (default: this lesson's config.toml)")
    parser.add_argument("--model", help="Override the model name")
    parser.add_argument("--base-url", help="Override the model endpoint")
    parser.add_argument("--temperature", type=float, help="Override the temperature")
    parser.add_argument("--reasoning-effort", help="Override the reasoning effort")


# modified in lesson 14
# modified in lesson 15
def run(
    ticker: str,
    config_path: Path,
    model: str | None = None,
    base_url: str | None = None,
    temperature: float | None = None,
    reasoning_effort: str | None = None,
) -> None:
    load_dotenv(".env")
    overrides = {
        name: value
        for name, value in {
            "model": model,
            "base_url": base_url,
            "temperature": temperature,
            "reasoning_effort": reasoning_effort,
        }.items()
        if value is not None
    }
    config = load_config(config_path, overrides)
    analysis = HedgeFundOrchestrator(config).run(ticker)
    print(render_report(analysis))
