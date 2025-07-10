
from .base import LLMProviderBase
from langchain.llms import Anthropic

class AnthropicProvider(LLMProviderBase, Anthropic):
    def __init__(self, config):
        api_key = config.get("api_key")
        model_name = config.get("model_name", "claude-3-opus-20240229")
        params = config.get("params", {})
        Anthropic.__init__(self, anthropic_api_key=api_key, model=model_name, **params)
        LLMProviderBase.__init__(self, config)

    def generate(self, prompt, **kwargs):
        return self(prompt, **kwargs)
