"""Get a commit message from ChatGPT, with emojies! ✨."""

import os
import sys
import traceback
from collections.abc import Sequence
from pathlib import Path
from typing import Annotated, NoReturn

import git
from cyclopts import App, Parameter, validators
from pydantic import BaseModel
from pydantic_ai import Agent

from vibes import config
from vibes.prompt import get_prompt


class CommitMessageResponse(BaseModel):
    """Structured response for commit message generation."""

    message: str
    emoji_legend: dict[str, str]


app = App(name="vibes")
app.register_install_completion_command()


# --- Commands -------------------------------------------------------------------------
# This is the part to replace. `@app.default()` runs when no subcommand is
# given, so switch these to `@app.command()` once there is more than one, and
# keep the exit codes each returns listed in its docstring.
@app.default()
def vibes(
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

    Args:
        path: The path of the repo.
        commit: Commit-ish to analyze.
        description: Optional description.
        only_prompt: Just print the prompt, don't open it.
        skip_chat: Don't start a chat with the LLM.

    Returns:
        The process exit code.

    Exit Codes:
        0: Success.
        1: Not a git repository, or a bad commit reference.
        2: Invalid usage.
        64-78: Reserved, an internal failure.
        129-159: Reserved, terminated by signal N, as 128 + N.
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

    # Get initial response with structured output
    result = agent.run_sync(prompt, output_type=CommitMessageResponse)
    response = result.output
    print(response.message)
    print("\n\nEmoji Legend:")
    for emoji, meaning in response.emoji_legend.items():
        print(f"{emoji}: {meaning}")

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
        result = agent.run_sync(user_input, message_history=result.all_messages())  # type: ignore[assignment]
        print()
        print()
        print(result.output)
    return 0


# --- Entry point ----------------------------------------------------------------------
# Maps the commands above onto exit codes, and is what `[project.scripts]` and
# `__main__` both call.

# Cyclopts itself exits 2 on invalid usage. These are sysexits(3) codes.
# `os.EX_*` holds the same values but only exists on Unix, so they are inlined
# to keep the CLI importable on Windows.
EX_NOINPUT = 66
EX_UNAVAILABLE = 69
EX_SOFTWARE = 70
EX_NOPERM = 77


def _fail(exc: Exception, code: int) -> NoReturn:
    """Report `exc` on stderr and exit with `code`."""
    print(f"error: {exc}", file=sys.stderr)
    sys.exit(code)


def main(tokens: Sequence[str] | None = None) -> None:
    """Run the CLI, reporting failures and mapping them onto exit codes.

    Args:
        tokens: The command line to parse. Defaults to `sys.argv[1:]`.
    """
    try:
        # `tokens` is a parameter so that tests can pass a command line here.
        # Under pytest, a bare `app()` warns, since it would parse pytest's own
        # argv, and a test that does so passes while testing nothing.
        app(tokens)
    # Nothing reports the errors below, so without `_fail` the CLI would exit on
    # a bare code and no output. Match on the exception rather than on
    # `type(exc)`, so that subclasses such as ConnectionRefusedError still land
    # on the right code. Specific OSError subclasses must precede any bare
    # `except OSError`, which would otherwise swallow them.
    except FileNotFoundError as exc:
        _fail(exc, EX_NOINPUT)
    except PermissionError as exc:
        _fail(exc, EX_NOPERM)
    except ConnectionError as exc:
        _fail(exc, EX_UNAVAILABLE)
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        sys.exit(EX_SOFTWARE)
