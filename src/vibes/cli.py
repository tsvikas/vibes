"""Get a commit message from ChatGPT, with emojies! ✨."""

import os
import sys
from pathlib import Path
from typing import Annotated

import git
from cyclopts import App, Parameter, validators
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage

from vibes.prompt import get_prompt

load_dotenv()
app = App()


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
        the path of the repo.
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
        repo = git.Repo(path, search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        print(f"Error: {path} is not a valid git repository", file=sys.stderr)
        sys.exit(1)

    try:
        prompt = get_prompt(repo, commit, description=description.strip())
    except git.exc.BadName as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)
    if only_prompt:
        print(prompt)
        return

    chat_model = init_chat_model(
        model=os.getenv("VIBES_MODEL", "gpt-4o"),
        model_provider=os.getenv("VIBES_PROVIDER", "openai"),
        api_key=os.getenv("VIBES_API_KEY"),
    )

    messages: list[BaseMessage] = [HumanMessage(content=prompt)]
    response = chat_model.invoke(messages)
    print(response.content)
    messages.append(response)

    # REPL loop
    while not skip_chat:
        # Get user input
        try:
            user_input = input("\n\nYou: ")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.lower() in ["exit", "quit", "", "q"]:
            break
        # Get assistant reply
        messages.append(HumanMessage(content=user_input))
        response = chat_model.invoke(messages)
        messages.append(response)
        print()
        print(response.content)


if __name__ == "__main__":
    app()
