
from .base import LLMProviderBase
from langchain.llms import OpenAI

class OpenAIProvider(LLMProviderBase, OpenAI):
    def __init__(self, config):
        api_key = config.get("api_key")
        model_name = config.get("model_name", "gpt-3.5-turbo")
        params = config.get("params", {})
        OpenAI.__init__(self, openai_api_key=api_key, model_name=model_name, **params)
        LLMProviderBase.__init__(self, config)

    def generate(self, prompt, **kwargs):
        return self(prompt, **kwargs)
