"""
Configuration management for LLM providers and extension settings.
"""
import os
import json


def get_config_path():
    # Use platform-appropriate config location
    home = os.path.expanduser("~")
    config_dir = os.path.join(home, ".libreai")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")

CONFIG_PATH = get_config_path()


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

def get_env_or_config(key, config):
    # Environment variable takes precedence
    return os.environ.get(key.upper()) or config.get(key, "")
