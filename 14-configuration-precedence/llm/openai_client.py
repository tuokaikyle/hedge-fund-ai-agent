"""Use ChatOpenAI behind the shared structured-model interface."""

from langchain_openai import ChatOpenAI
from config import RuntimeConfig
from llm.interface import ResponseT


class OpenAIStructuredLLM:
    # modified in lesson 13
    def __init__(self, config: RuntimeConfig) -> None:
        self.chat_model = ChatOpenAI(
            model=config.model,
            base_url=config.base_url,
            api_key=config.api_key,
            temperature=config.temperature,
            reasoning_effort=config.reasoning_effort,
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
