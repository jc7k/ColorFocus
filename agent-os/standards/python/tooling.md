# Python Tooling

Package management and project configuration.

## Package Manager: uv

**Why uv:**
- Fast dependency resolution (10-100x faster than pip)
- Single tool for venv + deps (simpler than poetry)

**Commands:**
```bash
uv sync              # Install dependencies
uv run pytest -v     # Run with venv activated
uv add <package>     # Add dependency
```

**Never use:**
- `pip install` directly
- `python` directly (use `uv run python`)

## pyproject.toml

```toml
[project]
name = "colorfocus"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## Python Version

- Minimum: Python 3.11
- Features used: StrEnum, type hints, dataclasses
