import os
import sys
from pathlib import Path
from typing import Annotated

import git
from cyclopts import App, Parameter, validators
from dotenv import load_dotenv
from openai import OpenAI

from .resources import prompt_md

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = App()

MODEL = "gpt-4o"
MESSAGE_FORMAT = prompt_md.read_text()


def get_repo(path: Path) -> git.Repo:
    """Get git repository from path."""
    try:
        return git.Repo(path)
    except git.exc.InvalidGitRepositoryError:
        print(f"Error: {path} is not a valid git repository", file=sys.stderr)
        sys.exit(1)


def list_files_in_commit(commit: git.Commit) -> list[str]:
    """
    Lists all the files in a repo at a given commit

    :param commit: A gitpython Commit object
    """
    file_list: list[str] = []
    stack = [commit.tree]
    while len(stack) > 0:
        tree = stack.pop()
        # enumerate blobs (files) at this level
        for b in tree.blobs:
            file_list.append(b.path)
        for subtree in tree.trees:
            stack.append(subtree)
    return file_list


def get_repo_info(path: Path, commit: str) -> dict[str, str]:
    """
    Get git information for a specific commit.
    """
    repo = get_repo(path)

    # Validate commit exists
    try:
        commit_obj = repo.commit(commit)
    except git.exc.BadName:
        print(f"Error: Invalid commit: {commit}", file=sys.stderr)
        sys.exit(1)

    # Get diff between commit and its parent
    try:
        parent = commit_obj.parents[0]
        git_diff = repo.git.diff(f"{parent.hexsha}", commit_obj.hexsha)
    except IndexError:
        root_hexsha = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
        git_diff = repo.git.diff(root_hexsha, commit_obj.hexsha)

    # Get ls-files
    git_ls_files = list_files_in_commit(commit_obj)
    git_ls_files = [fn for fn in git_ls_files if not fn.startswith("tests")]

    # Get README content
    readme_paths = ["README.md", "README.MD", "Readme.md", "readme.md"]
    readme_content = ""

    for readme_path in readme_paths:
        try:
            readme_content = repo.git.show(f"{commit}:{readme_path}")
            break
        except git.exc.GitCommandError:
            continue

    message = str(commit_obj.message)

    return {
        "git_diff": git_diff.strip(),
        "git_ls_files": "\n".join(git_ls_files).strip(),
        "readme_content": readme_content.strip(),
        "message": message.strip(),
    }


def get_repo_info_cached(path: Path) -> dict[str, str]:
    """
    Get git information for the staging area.
    """
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
    ] = Path("."),
    commit: Annotated[str, Parameter(name=("--commit", "-c"))] = "",
    description: Annotated[str, Parameter(name=("--description", "-d"))] = "",
    just_print: bool = False,
) -> None:
    """Create a prompt to ask for a commit message

    Parameters
    ----------
    path
        path to the repo.
    commit
        Commit-ish to analyze.
    description
        optional description.
    just_print
        just print the prompt, don't open it.
    """
    repo_info = get_repo_info(path, commit) if commit else get_repo_info_cached(path)
    prompt = MESSAGE_FORMAT.format(**repo_info, description=description.strip())
    if just_print:
        print(prompt)
    else:
        messages = [{"role": "user", "content": prompt}]
        while True:
            response = client.chat.completions.create(model=MODEL, messages=messages)  # type: ignore[arg-type]
            assistant_reply = response.choices[0].message.content
            assert assistant_reply is not None
            messages.append({"role": "assistant", "content": assistant_reply})
            print(assistant_reply)
            print()

            # Get user input
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", ""]:
                break
            messages.append({"role": "user", "content": user_input})


if __name__ == "__main__":
    app()
