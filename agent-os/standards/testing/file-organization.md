# Test File Organization

Naming and location conventions for test files.

## File Location

- **Python tests**: `/tests/test_*.py`
- **Frontend tests**: `/frontend/src/**/*.test.ts`

## Naming Convention

- Feature-based naming: `test_<feature>.py`
- Examples:
  - `test_cross_platform_sync.py` — tests JSON sync across platforms
  - `test_font_size_calculation.py` — tests font scaling logic
  - `test_mistake_identification.py` — tests mistake tracking feature

## Test Class Grouping

```python
class TestFeatureBasics:
    """Basic functionality tests."""
    def test_core_behavior(self): ...

class TestFeatureEdgeCases:
    """Edge case tests (add after core tests pass)."""
    def test_boundary_condition(self): ...
```

## Rules

- One test file per feature/concern
- Group related tests in classes with descriptive names
- Prefix all test files with `test_` (pytest discovery)
