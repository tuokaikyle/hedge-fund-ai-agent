"""OpenAI-backed implementation of the structured LLM protocol."""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


class OpenAIStructuredLLM:
    """Wrap a LangChain chat model so agents can request typed responses."""
    def __init__(self, *, model: str, temperature: float, api_key: str):
        self._chat_model = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
        )

    def invoke(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[BaseModel],
    ) -> BaseModel:
        """Run a two-message prompt and coerce the reply into the requested schema."""
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "{system_prompt}"),
                ("human", "{user_prompt}"),
            ]
        )
        chain = prompt | self._chat_model.with_structured_output(response_model)
        return chain.invoke(
            {
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
            }
        )
