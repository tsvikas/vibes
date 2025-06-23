"""Configuration management for Vibes."""

import os
import tomllib
from pathlib import Path

from dotenv import load_dotenv
from platformdirs import user_config_dir

# Load environment variables
load_dotenv()

# Try to load from XDG config file if it exists
config_file = Path(user_config_dir("vibes")) / "config.toml"
try:
    with config_file.open("rb") as f:
        _file_config = tomllib.load(f)
except FileNotFoundError:
    _file_config = {}


def get_provider() -> str:
    """Get the configured provider."""
    provider = _file_config.get("provider") or os.getenv("VIBES_PROVIDER")
    if not provider:
        raise ValueError(
            "No provider configured. "
            f"Set provider in {config_file} or VIBES_PROVIDER environment variable."
        )
    return provider


def get_api_key(provider: str | None = None) -> str:
    """Get API key for the specified or current provider."""
    target_provider = provider or get_provider()

    api_key = None

    # Check file config
    api_key = _file_config.get("providers", {}).get(target_provider, {}).get("api_key")
    # Check environment
    api_key = api_key or os.getenv(f"{target_provider.upper()}_API_KEY")

    if not api_key:
        raise ValueError(
            f"No API key found for provider '{target_provider}'. "
            f"Set API key in '{config_file}' "
            f"or {target_provider.upper()}_API_KEY environment variable."
        )
    return api_key


def get_model(provider: str | None = None) -> str:
    """Get model for the specified or current provider."""
    target_provider = provider or get_provider()

    defaults = {
        "openai": "gpt-4.1",
        "anthropic": "claude-sonnet-4-0",
        "google": "gemini-2.5-pro",
    }

    model = None

    # Check file config
    model = _file_config.get("providers", {}).get(target_provider, {}).get("model")
    # Check environment
    model = model or os.getenv(f"{target_provider.upper()}_MODEL")
    # Check defaults
    model = model or defaults.get(target_provider)

    if not model:
        raise ValueError(
            f"No model found for provider '{target_provider}'. "
            f"Set model in '{config_file}' "
            f"or {target_provider.upper()}_MODEL environment variable."
        )
    return model
