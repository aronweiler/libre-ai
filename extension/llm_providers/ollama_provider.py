
from .base import LLMProviderBase
from langchain.llms import Ollama

class OllamaProvider(LLMProviderBase, Ollama):
    def __init__(self, config):
        base_url = config.get("endpoint")
        model_name = config.get("model_name", "llama2")
        params = config.get("params", {})
        Ollama.__init__(self, base_url=base_url, model=model_name, **params)
        LLMProviderBase.__init__(self, config)

    def generate(self, prompt, **kwargs):
        return self(prompt, **kwargs)
