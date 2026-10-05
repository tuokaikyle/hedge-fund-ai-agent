"""Collect the model settings before building the agent system."""

import os
from dataclasses import dataclass


# introduced in lesson 13
@dataclass
class RuntimeConfig:
    model: str
    base_url: str
    api_key: str
    temperature: float = 0
    reasoning_effort: str = "none"


# introduced in lesson 13
def load_config() -> RuntimeConfig:
    model = os.getenv("LLM_MODEL")
    base_url = os.getenv("LLM_BASE_URL")
    api_key = os.getenv("LLM_API_KEY")
    if not all((model, base_url, api_key)):
        raise RuntimeError("Set LLM_MODEL, LLM_BASE_URL, and LLM_API_KEY in the root .env file.")

    return RuntimeConfig(model=model, base_url=base_url, api_key=api_key)
