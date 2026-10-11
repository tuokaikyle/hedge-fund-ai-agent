"""Ask the chat model for a response that matches a Pydantic model."""

import os
from typing import TypeVar

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

ResponseT = TypeVar("ResponseT", bound=BaseModel)


class LLMClient:
    def __init__(self) -> None:
        model = os.getenv("LLM_MODEL")
        base_url = os.getenv("LLM_BASE_URL")
        api_key = os.getenv("LLM_API_KEY")
        if not all((model, base_url, api_key)):
            raise RuntimeError("Set LLM_MODEL, LLM_BASE_URL, and LLM_API_KEY in the root .env file.")

        self.chat_model = ChatOpenAI(
            model=model,
            base_url=base_url,
            api_key=api_key,
            temperature=0,
            reasoning_effort="none",
        )

    def invoke(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[ResponseT],
    ) -> ResponseT:
        return self.chat_model.with_structured_output(response_model).invoke(
            [("system", system_prompt), ("human", user_prompt)]
        )
