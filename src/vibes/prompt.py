"""Create a commit message prompt based on the current git state."""

import git
from langchain_core.prompts import PromptTemplate

from vibes.resources import prompt_md

MESSAGE_FORMAT_STR = prompt_md.read_text(encoding="utf-8")
MESSAGE_FORMAT = PromptTemplate.from_template(MESSAGE_FORMAT_STR)


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


def split_commit_range(repo: git.Repo, commit_range: str) -> tuple[str, str]:
    """Split a commit range to start and end.

    Handle a single commit, and a commit to the empty object
    """
    if ".." not in commit_range:
        commit_range = f"{commit_range}~..{commit_range}"
    commit_start, commit_end = commit_range.split("..")
    # fix for commit before first commit
    try:
        _commit_start_hexsha = repo.commit(commit_start).hexsha
    except git.exc.BadName as e:
        if "not enough parent commits to reach" in str(e):
            # use the empty root object
            object_format = repo.config_reader().get_value(
                "extensions", "objectFormat", "sha1"
            )
            assert isinstance(object_format, str)  # noqa: S101
            commit_start = {
                "sha1": "4b825dc642cb6eb9a060e54bf8d69288fbee4904",
                "sha256": "6ef19b41225c5369f1c104d45d8d85ef"
                "a9b057b53b14b4b9b939dd74decc5321",
            }[object_format]
        else:
            raise
    return commit_start, commit_end


def get_repo_info(repo: git.Repo, commit_range: str) -> dict[str, str]:
    """Get git information for a specific commit."""
    if commit_range:
        # Get commit range
        commit_range = commit_range.replace("@", "HEAD")
        commit_start, commit_end = split_commit_range(repo, commit_range)

        # Get diff
        git_diff = repo.git.diff(commit_start, commit_end)

        # Get ls-files
        git_ls_files = list_files_in_commit(repo.commit(commit_end))

        # Get commit message
        message = "\n\n".join(
            str(commit.message)
            for commit in repo.iter_commits(f"{commit_start}..{commit_end}")
        )
    else:
        # use staging area or working directory
        # Get diff
        git_diff = repo.git.diff("--cached") or repo.git.diff()
        # FIX: it ignores untracked files
        if not git_diff:
            return get_repo_info(repo, "HEAD")

        # Get ls-files
        git_ls_files = repo.git.ls_files().splitlines()

        # commit_end for README
        commit_end = ":0"

        # Get commit message
        message = ""

    # remove test files from ls-files
    git_ls_files = [
        line
        for line in git_ls_files
        if not line.startswith("tests") and not line.startswith('"tests')
    ]

    # Get README content
    readme_content = ""
    for readme_path in ["README.md", "README.MD", "Readme.md", "readme.md"]:
        try:
            readme_content = repo.git.show(f"{commit_end}:{readme_path}")
            break
        except git.exc.GitCommandError:
            continue

    return {
        "git_diff": git_diff.strip(),
        "git_ls_files": "\n".join(git_ls_files).strip(),
        "readme_content": readme_content.strip(),
        "message": message.strip(),
    }


def get_prompt(repo: git.Repo, commit: str, description: str) -> str:
    """Get a commit message prompt."""
    repo_info = get_repo_info(repo, commit)
    return MESSAGE_FORMAT.format(**repo_info, description=description.strip())
