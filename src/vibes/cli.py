"""Get a commit message from ChatGPT, with emojies! ✨."""

import os
import sys
from pathlib import Path
from typing import Annotated

import anthropic
import git
from cyclopts import App, Parameter, validators
from dotenv import load_dotenv
from openai import OpenAI

from vibes.prompt import get_prompt

load_dotenv()
app = App()


def get_repo(path: Path) -> git.Repo:
    """Get git repository from path."""
    try:
        return git.Repo(path)
    except git.exc.InvalidGitRepositoryError:
        print(f"Error: {path} is not a valid git repository", file=sys.stderr)
        sys.exit(1)


@app.default()
def main(
    path: Annotated[
        Path,
        Parameter(
            name=("repo", "-r"), validator=validators.Path(exists=True, file_okay=False)
        ),
    ] = Path(),
    /,
    *,
    commit: Annotated[str, Parameter(name=("--commit", "-c"))] = "",
    description: Annotated[str, Parameter(name=("--description", "-d"))] = "",
    only_prompt: bool = False,
    skip_chat: Annotated[bool, Parameter(name=("--skip-chat", "-s"))] = False,
) -> None:
    """Create a prompt to ask for a commit message.

    Parameters
    ----------
    path
        path to the repo.
    commit
        Commit-ish to analyze.
    description
        optional description.
    only_prompt
        just print the prompt, don't open it.
    skip_chat
        don't start a chat with the LLM
    """
    try:
        prompt = get_prompt(get_repo(path), commit, description=description.strip())
    except git.exc.BadName as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)
    if only_prompt:
        print(prompt)
        return

    chat = ChatGPT()
    chat.add_message(prompt)

    # REPL loop
    while True:
        print()
        assistant_reply = chat.get_reply()
        print(assistant_reply)
        print()
        if skip_chat:
            break
        # Get user input
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.lower() in ["exit", "quit", ""]:
            break
        chat.add_message(user_input)


class ChatGPT:
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

    def add_message(self, content: str, role: str = "user") -> None:
        """Add a message to the chat."""
        self.messages.append({"role": role, "content": content})

    def get_reply(self) -> str:
        """Get LLM's reply to the chat."""
        response = self.client.chat.completions.create(
            model=self.model, messages=self.messages  # type: ignore[arg-type]
        )
        assistant_reply = response.choices[0].message.content
        if assistant_reply is None:
            raise RuntimeError("No reply")
        self.messages.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply


class Claude:
    """A chat with Anthropic LLM."""

    def __init__(self, api_key: None | str = None, model: None | str = None):
        """Create a chat with Anthropic LLM."""
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        assert api_key is not None  # noqa: S101
        model = model or os.getenv("MODEL", "claude-3-7-sonnet-20250219")
        assert model is not None  # noqa: S101

        self.client = anthropic.Anthropic()
        self.model = model
        self.messages: list[dict[str, str]] = []

    def add_message(self, content: str, role: str = "user") -> None:
        """Add a message to the chat."""
        self.messages.append({"role": role, "content": content})

    def get_reply(self) -> str:
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
        if assistant_reply is None:
            raise RuntimeError("No reply")
        self.messages.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply


if __name__ == "__main__":
    app()
