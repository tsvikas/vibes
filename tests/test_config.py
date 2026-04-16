"""Tests for the config module."""

import importlib
import os
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

if TYPE_CHECKING:
    import vibes.config


def _clean_env() -> dict[str, str]:
    """Return os.environ without any vibes/provider keys."""
    return {
        k: v
        for k, v in os.environ.items()
        if not k.startswith(("VIBES_", "OPENAI_", "ANTHROPIC_", "GOOGLE_"))
    }


@contextmanager
def _config_env(
    tmp_path: Path,
    config_toml: str = "",
    env: dict[str, str] | None = None,
) -> Generator["vibes.config"]:
    """Context manager that reloads vibes.config with controlled file+env.

    The patched environment stays active for the duration of the block,
    so function calls inside will see the right env vars.
    """
    config_file = tmp_path / "config.toml"
    if config_toml:
        config_file.write_text(config_toml)

    merged_env = _clean_env()
    if env:
        merged_env.update(env)

    with (
        patch("platformdirs.user_config_dir", return_value=str(tmp_path)),
        patch.dict(os.environ, merged_env, clear=True),
    ):
        import vibes.config  # noqa: PLC0415

        importlib.reload(vibes.config)
        yield vibes.config


class TestGetProvider:
    def test_from_config_file(self, tmp_path: Path) -> None:
        with _config_env(tmp_path, 'provider = "anthropic"\n') as cfg:
            assert cfg.get_provider() == "anthropic"

    def test_from_env_var(self, tmp_path: Path) -> None:
        with _config_env(tmp_path, env={"VIBES_PROVIDER": "openai"}) as cfg:
            assert cfg.get_provider() == "openai"

    def test_config_file_takes_precedence_over_env(self, tmp_path: Path) -> None:
        with _config_env(
            tmp_path,
            'provider = "anthropic"\n',
            env={"VIBES_PROVIDER": "openai"},
        ) as cfg:
            assert cfg.get_provider() == "anthropic"

    def test_missing_raises(self, tmp_path: Path) -> None:
        with (
            _config_env(tmp_path) as cfg,
            pytest.raises(ValueError, match="No provider configured"),
        ):
            cfg.get_provider()


class TestGetApiKey:
    def test_from_config_file(self, tmp_path: Path) -> None:
        toml = """\
provider = "anthropic"

[providers.anthropic]
api_key = "sk-from-file"
"""
        with _config_env(tmp_path, toml) as cfg:
            assert cfg.get_api_key() == "sk-from-file"

    def test_from_env_var(self, tmp_path: Path) -> None:
        with _config_env(
            tmp_path,
            'provider = "openai"\n',
            env={"OPENAI_API_KEY": "sk-from-env"},
        ) as cfg:
            assert cfg.get_api_key() == "sk-from-env"

    def test_explicit_provider_arg(self, tmp_path: Path) -> None:
        with _config_env(
            tmp_path,
            'provider = "anthropic"\n',
            env={"OPENAI_API_KEY": "sk-openai"},
        ) as cfg:
            assert cfg.get_api_key("openai") == "sk-openai"

    def test_config_file_takes_precedence_over_env(self, tmp_path: Path) -> None:
        toml = """\
provider = "anthropic"

[providers.anthropic]
api_key = "sk-from-file"
"""
        with _config_env(
            tmp_path, toml, env={"ANTHROPIC_API_KEY": "sk-from-env"}
        ) as cfg:
            assert cfg.get_api_key() == "sk-from-file"

    def test_missing_raises(self, tmp_path: Path) -> None:
        with (
            _config_env(tmp_path, 'provider = "anthropic"\n') as cfg,
            pytest.raises(ValueError, match="No API key found"),
        ):
            cfg.get_api_key()


class TestGetModel:
    def test_from_config_file(self, tmp_path: Path) -> None:
        toml = """\
provider = "anthropic"

[providers.anthropic]
model = "claude-opus-4"
"""
        with _config_env(tmp_path, toml) as cfg:
            assert cfg.get_model() == "claude-opus-4"

    def test_from_env_var(self, tmp_path: Path) -> None:
        with _config_env(
            tmp_path,
            'provider = "openai"\n',
            env={"OPENAI_MODEL": "gpt-4o"},
        ) as cfg:
            assert cfg.get_model() == "gpt-4o"

    def test_defaults(self, tmp_path: Path) -> None:
        with _config_env(tmp_path, 'provider = "openai"\n') as cfg:
            assert cfg.get_model() == "gpt-5"

        with _config_env(tmp_path, 'provider = "anthropic"\n') as cfg:
            assert cfg.get_model() == "claude-sonnet-4-5"

        with _config_env(tmp_path, 'provider = "google"\n') as cfg:
            assert cfg.get_model() == "gemini-3-pro"

    def test_config_file_takes_precedence_over_env_and_defaults(
        self, tmp_path: Path
    ) -> None:
        toml = """\
provider = "openai"

[providers.openai]
model = "gpt-4o"
"""
        with _config_env(tmp_path, toml, env={"OPENAI_MODEL": "gpt-3.5-turbo"}) as cfg:
            assert cfg.get_model() == "gpt-4o"

    def test_env_takes_precedence_over_defaults(self, tmp_path: Path) -> None:
        with _config_env(
            tmp_path,
            'provider = "openai"\n',
            env={"OPENAI_MODEL": "gpt-4o"},
        ) as cfg:
            assert cfg.get_model() == "gpt-4o"

    def test_explicit_provider_arg(self, tmp_path: Path) -> None:
        with _config_env(
            tmp_path,
            'provider = "anthropic"\n',
            env={"OPENAI_MODEL": "gpt-4o"},
        ) as cfg:
            assert cfg.get_model("openai") == "gpt-4o"

    def test_unknown_provider_no_model_raises(self, tmp_path: Path) -> None:
        with (
            _config_env(tmp_path, 'provider = "custom"\n') as cfg,
            pytest.raises(ValueError, match="No model found"),
        ):
            cfg.get_model()
