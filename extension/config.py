"""
Configuration management for LLM providers and extension settings.
"""
import os
import json

CONFIG_PATH = os.path.expanduser("~/.libreai_config.json")


def load_config():
    config = {}
    # Load from file if exists
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
    # Environment variable overrides
    env_provider = os.environ.get('LIBREAI_PROVIDER')
    env_api_key = os.environ.get('LIBREAI_API_KEY')
    env_model = os.environ.get('LIBREAI_MODEL')
    env_temp = os.environ.get('LIBREAI_TEMPERATURE')
    if env_provider:
        config['provider'] = env_provider
    if env_api_key:
        config['api_key'] = env_api_key
    if env_model:
        config['model_name'] = env_model
    if env_temp:
        try:
            config.setdefault('params', {})['temperature'] = float(env_temp)
        except Exception:
            pass
    return config

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
