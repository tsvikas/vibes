"""Create a commit message prompt based on the current git state."""

import git

from vibes.resources import prompt_md

MESSAGE_FORMAT = prompt_md.read_text(encoding="utf-8")


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


def get_repo_info(repo: git.Repo, commit_range: str) -> dict[str, str]:
    """Get git information for a specific commit."""
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


def get_repo_info_cached(repo: git.Repo) -> dict[str, str]:
    """Get git information for the staging area."""
    # Get diff between commit and its parent
    git_diff = repo.git.diff("--cached") or repo.git.diff()
    if not git_diff:
        return get_repo_info(repo, "HEAD")

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


def get_prompt(repo: git.Repo, commit: str, description: str) -> str:
    """Get a commit message prompt."""
    repo_info = get_repo_info(repo, commit) if commit else get_repo_info_cached(repo)
    return MESSAGE_FORMAT.format(**repo_info, description=description.strip())
