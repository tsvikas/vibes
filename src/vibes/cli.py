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

from .resources import prompt_md

load_dotenv()
app = App()

MESSAGE_FORMAT = prompt_md.read_text(encoding="utf-8")


def get_repo(path: Path) -> git.Repo:
    """Get git repository from path."""
    try:
        return git.Repo(path)
    except git.exc.InvalidGitRepositoryError:
        print(f"Error: {path} is not a valid git repository", file=sys.stderr)
        sys.exit(1)


def list_files_in_commit(commit: git.Commit) -> list[str]:
    """List all the files in a repo at a given commit.

    :param commit: A gitpython Commit object
    """
    file_list: list[str] = []
    stack = [commit.tree]
    while len(stack) > 0:
        tree = stack.pop()
        # enumerate blobs (files) at this level
        file_list.extend(str(b.path) for b in tree.blobs)
        stack.extend(tree.trees)
    return file_list


def commit_to_obj(commit: str, repo: git.Repo) -> git.Commit:
    """Convert a commit-ish to commit object."""
    try:
        commit_obj = repo.commit(commit)
    except git.exc.BadName as e:
        if "not enough parent commits to reach" in str(e):
            return repo.commit("4b825dc642cb6eb9a060e54bf8d69288fbee4904")
        raise
    return commit_obj


def get_repo_info(path: Path, commit_range: str) -> dict[str, str]:
    """Get git information for a specific commit."""
    repo = get_repo(path)

    commit_range = commit_range.replace("@", "HEAD")
    if ".." in commit_range:
        commit_start, commit_end = commit_range.split("..")
    else:
        commit_start = commit_range + "~"
        commit_end = commit_range

    # Validate commits exists
    start_obj = commit_to_obj(commit_start, repo)
    end_obj = commit_to_obj(commit_end, repo)

    # Get diff between commit and its parent
    git_diff = repo.git.diff(start_obj.hexsha, end_obj.hexsha)

    # Get ls-files
    git_ls_files = list_files_in_commit(end_obj)
    git_ls_files = [fn for fn in git_ls_files if not fn.startswith("tests")]

    # Get README content
    readme_paths = ["README.md", "README.MD", "Readme.md", "readme.md"]
    readme_content = ""

    for readme_path in readme_paths:
        try:
            readme_content = repo.git.show(f"{commit_end}:{readme_path}")
            break
        except git.exc.GitCommandError:
            continue

    message = "\n\n".join(
        str(commit.message) for commit in repo.iter_commits(commit_range)
    )

    return {
        "git_diff": git_diff.strip(),
        "git_ls_files": "\n".join(git_ls_files).strip(),
        "readme_content": readme_content.strip(),
        "message": message.strip(),
    }


def get_repo_info_cached(path: Path) -> dict[str, str]:
    """Get git information for the staging area."""
    repo = get_repo(path)

    # Get diff between commit and its parent
    git_diff = repo.git.diff("--cached") or repo.git.diff()
    if not git_diff:
        return get_repo_info(path, "HEAD")

    # Get ls-files
    git_ls_files = repo.git.ls_files().splitlines()
    git_ls_files = "\n".join(
        line
        for line in git_ls_files
        if not line.startswith("tests") and not line.startswith('"tests')
    )

    # Get README content
    readme_paths = ["README.md", "README.MD", "Readme.md", "readme.md"]
    readme_content = ""

    for readme_path in readme_paths:
        try:
            readme_content = repo.git.show(f":0:{readme_path}")
            break
        except git.exc.GitCommandError:
            continue

    return {
        "git_diff": git_diff.strip(),
        "git_ls_files": git_ls_files.strip(),
        "readme_content": readme_content.strip(),
        "message": "",
    }


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
        repo_info = (
            get_repo_info(path, commit) if commit else get_repo_info_cached(path)
        )
    except git.exc.BadName as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)

    prompt = MESSAGE_FORMAT.format(**repo_info, description=description.strip())
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
