"""Collect the model settings before building the agent system."""

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path


# introduced in lesson 13
@dataclass
class RuntimeConfig:
    model: str
    base_url: str
    api_key: str
    temperature: float = 0
    reasoning_effort: str = "none"


# modified in lesson 14
def load_config(
    config_path: Path,
    overrides: dict[str, str | float],
) -> RuntimeConfig:
    """Resolve public settings: defaults < environment < TOML < CLI."""
    settings = {
        "model": "gpt-6-luna",
        "base_url": "https://api.openai.com/v1",
        "temperature": 0.0,
        "reasoning_effort": "none",
    }

    for name in settings:
        value = os.getenv(f"LLM_{name.upper()}")
        if value is not None:
            settings[name] = float(value) if name == "temperature" else value

    with config_path.open("rb") as file:
        file_settings = tomllib.load(file)
    settings.update({name: file_settings[name] for name in settings if name in file_settings})
    settings.update(overrides)

    # Keep credentials in the environment, outside TOML and CLI overrides.
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise RuntimeError("Set LLM_API_KEY in the root .env file.")
    return RuntimeConfig(api_key=api_key, **settings)
