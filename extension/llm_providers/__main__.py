# For direct testing of provider plugins
if __name__ == '__main__':
    from provider_factory import get_provider
    config = {"api_key": "sk-..."}
    provider = get_provider('openai', config)
    print(provider.generate("Hello, world!"))
