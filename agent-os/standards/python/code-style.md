# Python Code Style

Conventions for Python code in ColorFocus.

## Type Hints

Always use type hints for function signatures:

```python
def generate(self, grid_size: int = 8) -> PuzzleGrid:
    ...
```

## StrEnum for Constants

```python
from enum import StrEnum

class ColorToken(StrEnum):
    BLACK = "BLACK"
    BLUE = "BLUE"
```

## Dataclasses for Models

```python
from dataclasses import dataclass

@dataclass
class PuzzleCell:
    word: ColorToken
    ink_color: ColorToken

    def to_dict(self) -> Dict[str, str]:
        return {"word": self.word.value, "inkColor": self.ink_color.value}
```

## Docstrings

Google-style docstrings with module, class, and method documentation:

```python
"""Module docstring explaining purpose.

Usage:
    from module import Class
    instance = Class()
"""

class MyClass:
    """
    Class docstring.

    Attributes:
        attr: Description.
    """

    def method(self, arg: str) -> bool:
        """
        Method docstring.

        Args:
            arg: Description.

        Returns:
            Description.
        """
```
