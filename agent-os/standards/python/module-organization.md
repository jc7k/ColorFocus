# Module Organization

Backend package structure.

## Directory Layout

```
backend/
└── app/
    ├── constants/     # Enums, static values loaded from JSON
    │   ├── colors.py
    │   ├── color_labels.py
    │   └── ui_text.py
    ├── models/        # Dataclasses for domain objects
    │   └── puzzle.py
    └── services/      # Business logic, generators
        ├── puzzle_generator.py
        └── distribution_validator.py
```

## Layer Responsibilities

- **constants/**: Load shared JSON, expose as StrEnums
- **models/**: Pure data containers with `to_dict()` serialization
- **services/**: Stateful classes with business logic

## Import Pattern

```python
from backend.app.constants.colors import ColorToken, COLORS
from backend.app.models.puzzle import PuzzleCell, PuzzleGrid
from backend.app.services.puzzle_generator import PuzzleGenerator
```

## File Placement

- New constant: `backend/app/constants/`
- New data structure: `backend/app/models/`
- New logic: `backend/app/services/`
