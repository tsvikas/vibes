import importlib

import vibes


def test_version() -> None:
    assert importlib.metadata.version("vibes") == vibes.__version__
