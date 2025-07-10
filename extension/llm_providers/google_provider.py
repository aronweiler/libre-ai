
from .base import LLMProviderBase
from langchain.llms import GooglePalm

class GoogleProvider(LLMProviderBase, GooglePalm):
    def __init__(self, config):
        api_key = config.get("api_key")
        model_name = config.get("model_name", "models/text-bison-001")
        params = config.get("params", {})
        GooglePalm.__init__(self, google_api_key=api_key, model=model_name, **params)
        LLMProviderBase.__init__(self, config)

    def generate(self, prompt, **kwargs):
        return self(prompt, **kwargs)
