"""Get a commit message from ChatGPT, with emojies! ✨."""

import os
import sys
from pathlib import Path
from typing import Annotated

import git
from cyclopts import App, Parameter, validators
from pydantic_ai import Agent

from vibes import config
from vibes.prompt import get_prompt

app = App(name="vibes")
app.register_install_completion_command()


@app.default()
def main(
    path: Annotated[
        Path,
        Parameter(
            name=("--repo", "-r"),
            validator=validators.Path(exists=True, file_okay=False),
        ),
    ] = Path(),
    *,
    commit: Annotated[str, Parameter(alias=("-c"))] = "",
    description: Annotated[str, Parameter(alias=("-d"))] = "",
    only_prompt: Annotated[bool, Parameter(negative="")] = False,
    skip_chat: Annotated[bool, Parameter(alias=("-s"))] = False,
) -> int:
    """Ask the model for a commit message.

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
        with git.Repo(path, search_parent_directories=True) as repo:
            prompt = get_prompt(repo, commit, description=description.strip())
    except git.exc.InvalidGitRepositoryError:
        print(f"Error: {path} is not a valid git repository", file=sys.stderr)
        sys.exit(1)
    except git.exc.BadName as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)
    if only_prompt:
        print(prompt)
        return 0

    # Set API key in environment (automatically cleaned up when process exits)
    env_var = f"{config.get_provider().upper()}_API_KEY"
    os.environ[env_var] = config.get_api_key()

    # Create agent using provider:model string format
    model_string = f"{config.get_provider()}:{config.get_model()}"
    agent = Agent(model_string)

    # Get initial response
    result = agent.run_sync(prompt)
    print(result.output)

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
        result = agent.run_sync(user_input, message_history=result.all_messages())
        print()
        print(result.output)
    return 0
