# Contributing to vibes

Thank you for your interest in contributing! There are many ways to help improve this project.

## Ways to Contribute

### 🐛 Report Issues

Found a bug or have a feature request? [Open an issue](https://github.com/tsvikas/vibes/issues/new) on GitHub.

### 💬 Join Discussions

Have questions or ideas? Join the conversation in [GitHub Discussions](https://github.com/tsvikas/vibes/discussions).

### 🔧 Code Contributions

We welcome pull requests!

If you're new to contributing to open source, check out [How to Contribute to Open Source][how-to-contribute].

Ready to get started? Follow the development setup below.

## Development Setup

### Prerequisites

- Install [git][install-git] and [uv][install-uv]
- **Optional**: install [just][install-just] to use `just` instead of `uv run just`

### Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/tsvikas/vibes.git
   ```

1. Set up the development environment:

   ```bash
   cd vibes
   uv run just prepare
   ```

## Development Workflow

### Code Quality Tools

- **Format code**: `uv run just format` (runs all the formatting tools)
- **Lint code**: `uv run just lint` (runs all the linting tools)
- **Format and lint code**: `uv run just quick-tools` (runs quick formatting and linting tools)
- **Run tests**: `uv run just test` (runs `pytest`)
- **Run pre-commit tests**: `uv run pre-commit run`. This also runs on each commit.
- **Run all checks**: `uv run just format lint test`

### Running Individual Tools

You can run specific tools directly:

```bash
uv run black
uv run ruff check
uv run mypy
uv run pytest
uv run pre-commit run
```

[how-to-contribute]: https://opensource.guide/how-to-contribute/
[install-git]: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
[install-just]: https://just.systems/man/en/
[install-uv]: https://docs.astral.sh/uv/getting-started/installation/
