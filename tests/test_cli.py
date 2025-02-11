from typer.testing import CliRunner

from vibes import __version__
from vibes.cli import app

runner = CliRunner()


def test_app() -> None:
    result = runner.invoke(app, ["load"])
    assert result.exit_code == 0
    assert "Loading" in result.stdout

    result = runner.invoke(app, ["shoot"])
    assert result.exit_code == 0
    assert "Shooting" in result.stdout

    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout

    result = runner.invoke(app, [])
    assert result.exit_code == 2
