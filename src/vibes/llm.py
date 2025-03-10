"""A chat with a large language model (LLM)."""

import os
from typing import override

import anthropic
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLM:
    """A chat with an LLM."""

    def add_message(self, content: str, role: str = "user") -> None:
        """Add a message to the chat."""
        raise NotImplementedError

    def query_llm(self) -> str:
        """Get LLM's reply to the chat."""
        raise NotImplementedError

    def get_reply(self, prompt: str | None = None) -> str:
        """Get LLM's reply to the chat, and add it to the messages."""
        if prompt is not None:
            self.add_message(prompt, role="user")
        assistant_reply = self.query_llm()
        self.add_message(assistant_reply, role="assistant")
        return assistant_reply


class ChatGPT(LLM):
    """A chat with OpenAI LLM."""

    def __init__(self, api_key: None | str = None, model: None | str = None):
        """Create a chat with OpenAI LLM."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        assert api_key is not None  # noqa: S101
        model = model or os.getenv("MODEL", "gpt-4o")
        assert model is not None  # noqa: S101
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.messages: list[dict[str, str]] = []

    @override
    def add_message(self, content: str, role: str = "user") -> None:
        """Add a message to the chat."""
        self.messages.append({"role": role, "content": content})

    @override
    def query_llm(self) -> str:
        """Get LLM's reply to the chat."""
        response = self.client.chat.completions.create(
            model=self.model, messages=self.messages  # type: ignore[arg-type]
        )
        if len(response.choices) != 1:
            raise RuntimeError
        assistant_reply = response.choices[0].message.content
        if not isinstance(assistant_reply, str):
            raise RuntimeError  # noqa: TRY004
        return assistant_reply


class Claude(LLM):
    """A chat with Anthropic LLM."""

    def __init__(self, api_key: None | str = None, model: None | str = None):
        """Create a chat with Anthropic LLM."""
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        if model is None:
            model = os.getenv("MODEL", "claude-3-7-sonnet-20250219")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.messages: list[dict[str, str]] = []

    @override
    def add_message(self, content: str, role: str = "user") -> None:
        """Add a message to the chat."""
        self.messages.append({"role": role, "content": content})

    @override
    def query_llm(self) -> str:
        """Get LLM's reply to the chat."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=self.messages,  # type: ignore[arg-type]
        )
        if len(response.content) > 1:
            raise RuntimeError
        if not isinstance(response.content[0], anthropic.types.TextBlock):
            raise RuntimeError  # noqa: TRY004
        assistant_reply = response.content[0].text
        return assistant_reply


def get_chat(llm: str | None = None, **llm_kwargs: str) -> LLM:
    """Get an instance of an LLM chat."""
    if llm is None:
        llm = os.getenv("LLM", "openai")
    return {"openai": ChatGPT, "anthropic": Claude}[llm](**llm_kwargs)
