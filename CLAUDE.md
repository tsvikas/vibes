# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Development Commands

- **Test**: `just test` or `uv run pytest`
- **Test Single**: `uv run pytest tests/test_file.py::test_name`
- **Lint**: `just lint` (ruff + mypy)
- **Format**: `just format` (isort + black)
- **Quick Check**: `just quick-tools` or `just q` (subset of formatting & linting tools, fast, good for development iterations)

# Code Style

- **Python Version**: 3.13+
- **Type Annotations**: Required, strict mypy (disallow_any_explicit=true)
- **Formatting**: Black with Ruff (docstring-code-format=true)
- **Import Order**: Handled by Ruff (select I001 --fix)
- **Docstrings**: Google-style (pydocstyle.convention = "google")
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Error Handling**: Specific exception messages
- **Git Commits**: Use emoji prefixes (🔧 config, 🏷️ rename, ♻️ refactor, etc.)

# Project Architecture

**vibes** is a CLI tool that generates AI-powered git commit messages with emoji integration. Key architectural components:

## Core Components

- **`cli.py`**: Main CLI application using Cyclopts framework
- **`config.py`**: XDG-compliant configuration management with environment variable support
- **`prompt.py`**: Git repository analysis and AI prompt generation
- **`resources/`**: Template files for prompts and style guides

## AI Integration

- **Pydantic AI Framework**: Multi-provider AI integration (OpenAI, Anthropic, Google Gemini)
- **Provider Configuration**: Support for different models / providers with configuration in config file or environment
- **Interactive Workflow**: REPL-style conversation for commit message refinement

## Configuration System

- **XDG Base Directory**: Config stored in `~/.config/vibes/config.toml`
- **Environment Variables**: `VIBES_PROVIDER`, `*_API_KEY`, `*_MODEL` support
- **Multi-Provider**: OpenAI (gpt-5), Anthropic (claude-sonnet-4-5), Google (gemini-3-pro)

## Git Integration

- **GitPython**: Repository analysis and diff extraction
- **Context Building**: Includes git diff, file structure, README content for AI analysis
- **Gitmoji Convention**: Structured commit messages with emoji prefixes

## Key Development Patterns

- **Strict Typing**: All functions require type annotations with mypy enforcement
- **Resource Templates**: Prompt templates in `resources/` directory for maintainable AI prompts
- **Error Handling**: Comprehensive exception handling with specific error messages
- **Testing**: pytest with mocking for AI provider responses
