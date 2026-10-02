import os
import json
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from enum import Enum
from pydantic import BaseModel
from typing import Tuple, List
from pathlib import Path


class ModelProvider(str, Enum):
    """Supported LLM providers"""
    ANTHROPIC = "Anthropic"
    OPENAI = "OpenAI"
    OLLAMA = "Ollama"


class LLMModel(BaseModel):
    """An LLM model configuration"""
    display_name: str
    model_name: str
    provider: ModelProvider

    def to_choice_tuple(self) -> Tuple[str, str, str]:
        return (self.display_name, self.model_name, self.provider.value)

    def is_custom(self) -> bool:
        return self.model_name == "-"

    def has_json_mode(self) -> bool:
        if self.is_ollama():
            return "llama3" in self.model_name or "neural-chat" in self.model_name
        return True

    def is_ollama(self) -> bool:
        return self.provider == ModelProvider.OLLAMA


def load_models_from_json(json_path: str) -> List[LLMModel]:
    with open(json_path, 'r') as f:
        models_data = json.load(f)
    models = []
    for model_data in models_data:
        try:
            provider_enum = ModelProvider(model_data["provider"])
        except ValueError:
            continue  # skip models for removed providers
        models.append(LLMModel(
            display_name=model_data["display_name"],
            model_name=model_data["model_name"],
            provider=provider_enum,
        ))
    return models


current_dir = Path(__file__).parent
AVAILABLE_MODELS = load_models_from_json(str(current_dir / "api_models.json"))
OLLAMA_MODELS = load_models_from_json(str(current_dir / "ollama_models.json"))

LLM_ORDER = [model.to_choice_tuple() for model in AVAILABLE_MODELS]
OLLAMA_LLM_ORDER = [model.to_choice_tuple() for model in OLLAMA_MODELS]


def get_model_info(model_name: str, model_provider: str) -> LLMModel | None:
    all_models = AVAILABLE_MODELS + OLLAMA_MODELS
    return next((m for m in all_models if m.model_name == model_name and m.provider == model_provider), None)


def find_model_by_name(model_name: str) -> LLMModel | None:
    all_models = AVAILABLE_MODELS + OLLAMA_MODELS
    return next((m for m in all_models if m.model_name == model_name), None)


def get_model(model_name: str, model_provider: ModelProvider, api_keys: dict = None):
    if model_provider == ModelProvider.OPENAI:
        api_key = (api_keys or {}).get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in your .env file.")
        base_url = os.getenv("OPENAI_API_BASE")
        return ChatOpenAI(model=model_name, api_key=api_key, base_url=base_url)
    elif model_provider == ModelProvider.ANTHROPIC:
        api_key = (api_keys or {}).get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY in your .env file.")
        return ChatAnthropic(model=model_name, api_key=api_key)
    elif model_provider == ModelProvider.OLLAMA:
        ollama_host = os.getenv("OLLAMA_HOST", "localhost")
        base_url = os.getenv("OLLAMA_BASE_URL", f"http://{ollama_host}:11434")
        return ChatOllama(model=model_name, base_url=base_url)
    else:
        raise ValueError(f"Unsupported model provider: {model_provider}. Supported: OpenAI, Anthropic, Ollama.")
