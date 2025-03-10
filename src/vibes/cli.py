"""Get a commit message from ChatGPT, with emojies! ✨."""

import sys
from pathlib import Path
from typing import Annotated

import git
from cyclopts import App, Parameter, validators
from dotenv import load_dotenv

from vibes.llm import get_chat
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
        repo = git.Repo(path)
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

    chat = get_chat()

    assistant_reply = chat.get_reply(prompt)
    print(assistant_reply)

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
        assistant_reply = chat.get_reply(user_input)
        print()
        print(assistant_reply)


if __name__ == "__main__":
    app()
