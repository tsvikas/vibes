"""Tests for the prompt module."""

import sys
from collections.abc import Generator
from pathlib import Path
from textwrap import dedent

import git
import pytest

from vibes.prompt import get_prompt, get_repo_info

if sys.platform.startswith("win"):
    pytest.skip("skipping non-windows tests", allow_module_level=True)


class GitRepo:
    def __init__(self, repo_path: Path, *, init: bool = False):
        if init and repo_path.joinpath(".git").exists():
            raise ValueError("Git repo already initialized")
        self.path = repo_path
        self.repo = git.Repo.init(repo_path) if init else git.Repo(repo_path)


@pytest.fixture
def git_repo(tmp_path: Path) -> Generator[GitRepo]:
    """Get a GitRepo."""
    repo = GitRepo(tmp_path, init=True)
    config_writer = repo.repo.config_writer("repository")
    config_writer.set_value("diff", "mnemonicPrefix", "true")
    config_writer.release()
    sample_file = repo.path.joinpath("sample_file")
    sample_file_content = []
    # commit 1
    sample_file_content.append("this is from the 1st commit")
    sample_file.write_text("\n".join(sample_file_content) + "\n")
    readme_file = repo.path.joinpath("README.md")
    readme_file.write_text("This is the README file")
    repo.repo.index.add([str(sample_file), str(readme_file)])
    repo.repo.index.commit(message="commit #1")
    # commit 2
    sample_file_content.append("this is from the 2nd commit")
    sample_file.write_text("\n".join(sample_file_content) + "\n")
    repo.repo.index.add([str(sample_file)])
    repo.repo.index.commit(message="commit #2")
    # commit 3
    sample_file_content[-1] += ", with edits from the 3rd commit"
    sample_file.write_text("\n".join(sample_file_content) + "\n")
    repo.repo.index.add([str(sample_file)])
    repo.repo.index.commit(message="commit #3")
    yield repo
    # Cleanup: close the repo to terminate all subprocesses
    repo.repo.close()


def test_get_repo_info_with_commit_range(git_repo: GitRepo) -> None:
    """Test get_repo_info with a commit range."""
    result = get_repo_info(git_repo.repo, "HEAD~2..HEAD")
    expected_result = {
        "git_diff": dedent(
            """\
            diff --git a/sample_file b/sample_file
            index aeb249a..d0c0d44 100644
            --- a/sample_file
            +++ b/sample_file
            @@ -1 +1,2 @@
             this is from the 1st commit
            +this is from the 2nd commit, with edits from the 3rd commit"""
        ),
        "git_ls_files": "README.md\nsample_file",
        "message": "commit #3\n\ncommit #2",
        "readme_content": "This is the README file",
    }
    assert result == expected_result


def test_get_repo_info_with_commit_range_to_root(git_repo: GitRepo) -> None:
    """Test get_repo_info with a commit range."""
    result = get_repo_info(git_repo.repo, "HEAD~3..HEAD")
    expected_result = {
        "git_diff": dedent(
            """\
            diff --git a/README.md b/README.md
            new file mode 100644
            index 0000000..4f4a730
            --- /dev/null
            +++ b/README.md
            @@ -0,0 +1 @@
            +This is the README file
            \\ No newline at end of file
            diff --git a/sample_file b/sample_file
            new file mode 100644
            index 0000000..d0c0d44
            --- /dev/null
            +++ b/sample_file
            @@ -0,0 +1,2 @@
            +this is from the 1st commit
            +this is from the 2nd commit, with edits from the 3rd commit"""
        ),
        "git_ls_files": "README.md\nsample_file",
        "message": "commit #3\n\ncommit #2\n\ncommit #1",
        "readme_content": "This is the README file",
    }
    assert result == expected_result


def test_get_repo_info_with_single_commit(git_repo: GitRepo) -> None:
    """Test get_repo_info with a single commit reference."""
    result = get_repo_info(git_repo.repo, "HEAD")
    expected_result = {
        "git_diff": dedent(
            """\
            diff --git a/sample_file b/sample_file
            index 2760370..d0c0d44 100644
            --- a/sample_file
            +++ b/sample_file
            @@ -1,2 +1,2 @@
             this is from the 1st commit
            -this is from the 2nd commit
            +this is from the 2nd commit, with edits from the 3rd commit"""
        ),
        "git_ls_files": "README.md\nsample_file",
        "message": "commit #3",
        "readme_content": "This is the README file",
    }
    assert result == expected_result


def test_get_repo_info_with_staging(git_repo: GitRepo) -> None:
    """Test get_repo_info with changes in staging area."""
    # add to staging area
    sample_file = git_repo.path.joinpath("sample_file")
    sample_file_content = sample_file.read_text().splitlines()
    sample_file_content.append("this is from the staging area")
    sample_file.write_text("\n".join(sample_file_content) + "\n")
    git_repo.repo.index.add([str(sample_file)])

    result = get_repo_info(git_repo.repo, "")
    expected_result = {
        "git_diff": dedent(
            """\
            diff --git c/sample_file i/sample_file
            index d0c0d44..3a9fbbf 100644
            --- c/sample_file
            +++ i/sample_file
            @@ -1,2 +1,3 @@
             this is from the 1st commit
             this is from the 2nd commit, with edits from the 3rd commit
            +this is from the staging area"""
        ),
        "git_ls_files": "README.md\nsample_file",
        "message": "",
        "readme_content": "This is the README file",
    }
    assert result == expected_result


def test_get_repo_info_with_working_dir(git_repo: GitRepo) -> None:
    """Test get_repo_info with changes in working directory."""
    # add to working directory
    sample_file = git_repo.path.joinpath("sample_file")
    sample_file_content = sample_file.read_text().splitlines()
    sample_file_content.append("this is from the working directory")
    sample_file.write_text("\n".join(sample_file_content) + "\n")

    result = get_repo_info(git_repo.repo, "")
    expected_result = {
        "git_diff": dedent(
            """\
            diff --git i/sample_file w/sample_file
            index d0c0d44..8dce245 100644
            --- i/sample_file
            +++ w/sample_file
            @@ -1,2 +1,3 @@
             this is from the 1st commit
             this is from the 2nd commit, with edits from the 3rd commit
            +this is from the working directory"""
        ),
        "git_ls_files": "README.md\nsample_file",
        "message": "",
        "readme_content": "This is the README file",
    }
    assert result == expected_result


def test_get_repo_info_handle_readme_not_found(git_repo: GitRepo) -> None:
    """Test get_repo_info handles missing README gracefully."""
    readme_file = git_repo.path.joinpath("README.md")
    readme_file.unlink()
    git_repo.repo.index.remove([str(readme_file)])
    git_repo.repo.index.commit(message="commit #4, remove the readme")

    result = get_repo_info(git_repo.repo, "")
    expected_result = {
        "git_diff": dedent(
            """\
            diff --git a/README.md b/README.md
            deleted file mode 100644
            index 4f4a730..0000000
            --- a/README.md
            +++ /dev/null
            @@ -1 +0,0 @@
            -This is the README file
            \\ No newline at end of file"""
        ),
        "git_ls_files": "sample_file",
        "message": "commit #4, remove the readme",
        "readme_content": "",
    }
    assert result == expected_result


def test_get_prompt(git_repo: GitRepo) -> None:
    """Test get_prompt assembles the prompt correctly."""
    description = "Test description"
    prompt = get_prompt(git_repo.repo, "HEAD", description)
    expected_prompt_end = dedent(
        """\
## README ####################################################################
```
This is the README file
```
<end of README>

## git ls-files (without tests) ##############################################
```
README.md
sample_file
```

## git diff ##################################################################
```
diff --git a/sample_file b/sample_file
index 2760370..d0c0d44 100644
--- a/sample_file
+++ b/sample_file
@@ -1,2 +1,2 @@
 this is from the 1st commit
-this is from the 2nd commit
+this is from the 2nd commit, with edits from the 3rd commit
```

## Previous message ##########################################################
This might be correct or misleading
```
commit #3
```

## Optional description ######################################################
This is important notes about this commit
```
Test description
```
"""
    )
    assert expected_prompt_end in prompt
