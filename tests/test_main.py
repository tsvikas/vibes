from pytest_mock import MockerFixture


def test_main_module_execution(mocker: MockerFixture) -> None:
    mock_app = mocker.patch("vibes.cli.app")
    import vibes.__main__  # noqa: F401, PLC0415

    mock_app.assert_called_once_with(prog_name="vibes")
