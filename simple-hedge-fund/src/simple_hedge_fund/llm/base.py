"""Shared protocol for provider implementations that return structured responses."""

from __future__ import annotations

from typing import Protocol, TypeVar

from pydantic import BaseModel


StructuredResponseT = TypeVar("StructuredResponseT", bound=BaseModel)


class StructuredLLM(Protocol):
    """Minimal interface the agents depend on, independent of any provider SDK."""
    def invoke(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[StructuredResponseT],
    ) -> StructuredResponseT:
        """Return a structured response for the supplied prompt."""
