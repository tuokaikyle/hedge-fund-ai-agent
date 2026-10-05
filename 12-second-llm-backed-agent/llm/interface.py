"""The small structured-model interface shared by investor agents."""

from typing import Protocol, TypeVar

from pydantic import BaseModel


ResponseT = TypeVar("ResponseT", bound=BaseModel)


class StructuredLLM(Protocol):
    def invoke(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[ResponseT],
    ) -> ResponseT:
        """Return a response matching the agent's model."""
