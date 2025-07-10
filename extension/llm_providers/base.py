"""
Base class for LLM providers using LangChain.
"""
class LLMProviderBase:
    def __init__(self, config):
        self.config = config
    def generate(self, prompt, **kwargs):
        raise NotImplementedError
