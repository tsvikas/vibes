# vibes

<!-- prettier-ignore-start -->
[![Tests][tests-badge]][tests-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]


[tests-badge]:              https://github.com/tsvikas/vibes/actions/workflows/lint_and_test.yml/badge.svg
[tests-link]:               https://github.com/tsvikas/vibes/actions/workflows/lint_and_test.yml
[rtd-badge]:                https://readthedocs.org/projects/vibes/badge/?version=latest
[rtd-link]:                 https://vibes.readthedocs.io/en/latest/?badge=latest
[pypi-version]:             https://img.shields.io/pypi/v/vibes
[pypi-link]:                https://pypi.org/project/vibes/
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/vibes
[conda-link]:               https://github.com/conda-forge/vibes-feedstock
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/vibes
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/tsvikas/vibes/discussions

<!-- prettier-ignore-end -->

## Usage

```
import vibes
```

## Development

- install [git][install-git], [uv][install-uv].
- git clone this repo
- run `uv run just prepare`

[install-git]: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
[install-uv]: https://docs.astral.sh/uv/getting-started/installation/

## Code formatting

- use `uv run black .` to format code
- use
  `git ls-files -z -- '*.md' '*.rst' '*.tex' '*.py' | xargs -0 uv run blacken-docs`
  to format docs

## Code quality

- use `uv run ruff check .` to verify code quality
- use `uv run mypy` to verify check typing
- use `uv run pytest` to run tests

## Build

- run formatting, linting, and tests.
- optionally, use `uv run dunamai from git` to see the current version
- replace the version in `src/vibes/__init__.py`
- commit
- use
  `VER="vX.Y.Z" && git tag -a "$VER" -m "version $VER" -e && git push origin tag "$VER"`
- use `uv build` to build
- add '+dev' to the version in `src/vibes/__init__.py`
- commit
- push
