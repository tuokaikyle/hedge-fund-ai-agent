"""Create the configured LLM provider or explain why heuristic mode is being used."""

from __future__ import annotations

from simple_hedge_fund.llm.base import StructuredLLM
from simple_hedge_fund.llm.openai_provider import OpenAIStructuredLLM
from simple_hedge_fund.models import AppConfig


def build_llm(config: AppConfig) -> tuple[StructuredLLM | None, str]:
    """Resolve the runtime provider and return a status message for the CLI report."""
    if not config.use_llm:
        return None, "LLM disabled by configuration."

    if config.provider == "none":
        return None, "No provider selected; using heuristic-only mode."

    if config.provider == "openai":
        if not config.openai_api_key:
            return None, "OPENAI_API_KEY not set; using heuristic-only mode."
        return (
            OpenAIStructuredLLM(
                model=config.model,
                temperature=config.temperature,
                api_key=config.openai_api_key,
            ),
            f"OpenAI enabled with model {config.model}.",
        )

    raise ValueError(f"Unsupported provider: {config.provider}")
