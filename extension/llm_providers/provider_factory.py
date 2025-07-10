"""
Factory for instantiating LLM providers based on config.
"""
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .google_provider import GoogleProvider
from .ollama_provider import OllamaProvider

def get_provider_from_config(config):
    provider_name = config.get('provider', 'openai').lower()
    if provider_name == 'openai':
        return OpenAIProvider(config)
    elif provider_name == 'anthropic':
        return AnthropicProvider(config)
    elif provider_name == 'google':
        return GoogleProvider(config)
    elif provider_name == 'ollama':
        return OllamaProvider(config)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
