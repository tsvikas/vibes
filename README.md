# vibes

[![Tests][tests-badge]][tests-link]
[![uv][uv-badge]][uv-link]
[![Ruff][ruff-badge]][ruff-link]
[![Black][black-badge]][black-link]
[![codecov][codecov-badge]][codecov-link]
\
[![Made Using tsvikas/python-template][template-badge]][template-link]
[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![PRs Welcome][prs-welcome-badge]][prs-welcome-link]

## Overview

Get a commit message from ChatGPT or Claude, with [gitmoji](https://gitmoji.dev/) ✨.\
Talk to the AI and request changes, until you're happy with the message.

![Screenshot](assets/screenshot.png)

## Install

Install with pipx or uv:

```bash
pipx install git+https://github.com/tsvikas/vibes.git
```

or

```bash
uv tool install git+https://github.com/tsvikas/vibes.git
```

## Configuration

Configure your AI provider using either a TOML config file or environment variables.

### Option 1: TOML Config File

Create `~/.config/vibes/config.toml`:

```toml
provider = "anthropic"  # or "openai" or "google"

[providers.anthropic]
api_key = "sk-ant-..."
model = "claude-sonnet-4-5"  # optional
```

### Option 2: Environment Variables

```bash
export VIBES_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...
export ANTHROPIC_MODEL=claude-sonnet-4-5  # optional
```

## Usage

Just run `vibes` in your git repo, to get an LLM to suggest a commit message for
your current changes (the index, or the working directory, or the last commit)

Use `-r` to specify a path to the repo (default `.`).
Use `-c` to specify a specific commit, or a commit range.
Use `-d` to describe the change to the LLM yourself.

Use `vibes --help` to learn more.

You can chat with the LLM and request changes.
When you finish, end the conversation (^C, ^D, exit, quit, or Enter)
and use the message.

Future improvements: The ability to control the prompt, and the template.

## Contributing

Interested in contributing?
See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guideline.

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]: https://github.com/psf/black
[codecov-badge]: https://codecov.io/gh/tsvikas/vibes/graph/badge.svg
[codecov-link]: https://codecov.io/gh/tsvikas/vibes
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]: https://github.com/tsvikas/vibes/discussions
[prs-welcome-badge]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg
[prs-welcome-link]: https://opensource.guide/how-to-contribute/
[ruff-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[ruff-link]: https://github.com/astral-sh/ruff
[template-badge]: https://img.shields.io/badge/%F0%9F%9A%80_Made_Using-tsvikas%2Fpython--template-gold
[template-link]: https://github.com/tsvikas/python-template
[tests-badge]: https://github.com/tsvikas/vibes/actions/workflows/ci.yml/badge.svg
[tests-link]: https://github.com/tsvikas/vibes/actions/workflows/ci.yml
[uv-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json
[uv-link]: https://github.com/astral-sh/uv
