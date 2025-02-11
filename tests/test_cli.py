from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from vibes import __version__
from vibes.cli import app


def client_chat_completions_create(
    model: str, messages: list[dict[str, str]]  # noqa: ARG001
) -> Mock:
    reply = f"RE: {messages[-1]['content']}"
    response = Mock()
    response.choices[0].message.content = reply
    return response


@pytest.fixture
def mock_openai_client(mocker: MockerFixture) -> Mock:
    client = mocker.patch("openai.OpenAI")
    client.chat.completions.create = client_chat_completions_create
    return client


def test_version(
    mock_openai_client: Mock, capsys: pytest.CaptureFixture[str]  # noqa: ARG001
) -> None:
    app("--version")
    assert capsys.readouterr().out.strip() == __version__
