"""Configuration loading from environment variables, TOML, and CLI overrides."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from simple_hedge_fund.models import AppConfig


DEFAULT_CONFIG_FILE = "config.toml"


def load_app_config(
    config_path: Path | None = None,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool | None = None,
    reasoning: bool | None = None,
) -> AppConfig:
    """Merge config file values, environment variables, and CLI overrides."""
    load_dotenv()

    config_data = _load_config_file(config_path)
    resolved_provider = str(provider or config_data.get("provider") or "openai").lower()

    return AppConfig(
        provider=resolved_provider,
        model=str(model or config_data.get("model") or "gpt-4.1-mini"),
        use_llm=_resolve_bool(use_llm, config_data.get("use_llm"), default=True),
        temperature=float(config_data.get("temperature", 0.1)),
        reasoning=_resolve_bool(reasoning, config_data.get("reasoning"), default=True),
        default_tickers=[str(ticker).upper() for ticker in config_data.get("default_tickers", [])],
        openai_api_key=os.getenv("OPENAI_API_KEY") or _string_or_none(config_data.get("openai_api_key")),
    )


def _load_config_file(config_path: Path | None) -> dict[str, Any]:
    """Load an explicit config file or the default config from the working directory."""
    if config_path is not None:
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        return _read_toml(config_path)

    default_path = Path.cwd() / DEFAULT_CONFIG_FILE
    if default_path.exists():
        return _read_toml(default_path)
    return {}


def _read_toml(path: Path) -> dict[str, Any]:
    """Read a top-level TOML table into a plain dictionary."""
    with path.open("rb") as file_handle:
        data = tomllib.load(file_handle)
    if not isinstance(data, dict):
        raise ValueError("Config file must contain a TOML table at the top level.")
    return data


def _resolve_bool(primary: bool | None, secondary: Any, *, default: bool) -> bool:
    """Prefer an explicit CLI flag, then a config value, then the default."""
    if primary is not None:
        return primary
    if isinstance(secondary, bool):
        return secondary
    return default


def _string_or_none(value: Any) -> str | None:
    """Normalize blank-like values to None."""
    if value is None:
        return None
    text = str(value).strip()
    return text or None
