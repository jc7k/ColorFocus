# Python Test Patterns

pytest conventions for ColorFocus.

## Run Tests

```bash
uv run pytest -v              # All tests
uv run pytest tests/test_puzzle_generator.py -v  # Single file
```

## Test Structure

```python
"""Module docstring explaining what this file tests."""

from backend.app.constants.colors import ColorToken

# Module-level constants
EXPECTED_TOKEN_COUNT = 8

class TestFeatureName:
    """Class docstring describing test group."""

    def test_specific_behavior(self):
        """Test docstring explaining expected outcome."""
        result = do_thing()
        assert result == expected
```

## Setup Patterns

- **Inline setup**: For simple, isolated tests
- **Class constants**: For shared expected values across tests
- **pytest fixtures**: For complex shared resources (generators, file handles)

## Docstrings

- Module: What feature/area is tested
- Class: Group purpose (basics, edge cases, validation)
- Method: What specific behavior is verified
