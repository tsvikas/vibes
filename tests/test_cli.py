from pathlib import Path

import git
import pytest

from vibes import __version__, cli
from vibes.cli import (
    EX_NOINPUT,
    EX_NOPERM,
    EX_SOFTWARE,
    EX_UNAVAILABLE,
    app,
    main,
)


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


def test_main_usage_error() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--not-an-option"])
    # Cyclopts >=5 exits 2 on invalid usage, as argparse, click and clap do.
    # sysexits(3) would say 64, but 2 is the far wider convention.
    assert exc_info.value.code == 2


@pytest.mark.parametrize(
    ("error", "code"),
    [
        (FileNotFoundError("missing.txt"), EX_NOINPUT),
        (PermissionError("locked.txt"), EX_NOPERM),
        (ConnectionError("down"), EX_UNAVAILABLE),
        # a subclass lands on its parent's code
        (ConnectionRefusedError("refused"), EX_UNAVAILABLE),
    ],
)
def test_main_reported_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    code: int,
) -> None:
    def explode(*_args: object, **_kwargs: object) -> None:
        raise error

    monkeypatch.setattr(cli, "app", explode)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == code
    assert capsys.readouterr().err == f"error: {error}\n"


def test_main_unhandled_error(monkeypatch: pytest.MonkeyPatch) -> None:
    # Accept the call that `main` makes, so that the RuntimeError below is what
    # reaches it, rather than a TypeError over the signature.
    def explode(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError

    monkeypatch.setattr(cli, "app", explode)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == EX_SOFTWARE
