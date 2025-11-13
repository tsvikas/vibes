"""Get a commit message from ChatGPT, with emojies! ✨."""

import sys
import warnings
from pathlib import Path
from typing import Annotated

# Suppress Pydantic V1 compatibility warning in Python 3.14+
warnings.filterwarnings(
    "ignore",
    message=(
        "Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater"
    ),
    category=UserWarning,
    module="langchain_core._api.deprecation",
)

import git  # noqa: E402
from cyclopts import App, Parameter, validators  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain_core.messages import BaseMessage, HumanMessage  # noqa: E402

from vibes import config  # noqa: E402
from vibes.prompt import get_prompt  # noqa: E402

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

    chat_model = init_chat_model(
        model=config.get_model(),
        model_provider=config.get_provider(),
        api_key=config.get_api_key(),
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
    return 0
