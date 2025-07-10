"""
Test script for LLM provider integration.
"""
from extension.llm_providers.provider_factory import get_provider

def main():
    config = {
        "api_key": "sk-...",
        "model_name": "gpt-3.5-turbo",
        "params": {"temperature": 0.7}
    }
    provider = get_provider("openai", config)
    print(provider.generate("Say hello to LibreOffice!"))

if __name__ == "__main__":
    main()
