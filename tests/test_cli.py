from pathlib import Path

import git
import pytest

from vibes import __version__
from vibes.cli import app


def test_version(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        app("--version")
    assert exc_info.value.code == 0
    assert capsys.readouterr().out.strip() == __version__


def test_only_prompt_prints_prompt_and_exits(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """--only-prompt should print the prompt to stdout and return 0."""
    repo = git.Repo.init(tmp_path)
    (tmp_path / "file.txt").write_text("hello\n")
    repo.index.add(["file.txt"])
    repo.index.commit("init")
    (tmp_path / "file.txt").write_text("hello world\n")
    repo.index.add(["file.txt"])

    with pytest.raises(SystemExit) as exc_info:
        app(["--repo", str(tmp_path), "--only-prompt"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr().out
    # The prompt should contain the diff
    assert "hello world" in captured
    repo.close()


def test_invalid_repo_path(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Passing a path that is not a git repo should exit with error."""
    not_a_repo = tmp_path / "nope"
    not_a_repo.mkdir()
    with pytest.raises(SystemExit) as exc_info:
        app(["--repo", str(not_a_repo)])
    assert exc_info.value.code == 1
    assert "not a valid git repository" in capsys.readouterr().err


def test_bad_commit_ref(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Passing an invalid commit reference should exit with error."""
    repo = git.Repo.init(tmp_path)
    (tmp_path / "f.txt").write_text("x\n")
    repo.index.add(["f.txt"])
    repo.index.commit("init")

    with pytest.raises(SystemExit) as exc_info:
        app(["--repo", str(tmp_path), "-c", "nonexistent_ref_xyz"])
    assert exc_info.value.code == 1
    assert "Error" in capsys.readouterr().err
    repo.close()
