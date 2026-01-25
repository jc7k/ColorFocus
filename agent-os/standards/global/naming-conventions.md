# Naming Conventions

Per-language naming rules for consistency across the codebase.

## By Language

| Context | Convention | Example |
|---------|------------|---------|
| Python variables, functions, files | snake_case | `puzzle_generator.py`, `ink_color` |
| Python classes | PascalCase | `PuzzleGenerator`, `ColorToken` |
| JavaScript variables, functions | camelCase | `currentGridSize`, `calculateFontSize()` |
| CSS variables, classes | kebab-case | `--color-bg-page`, `.skip-link` |
| JSON data keys | snake_case | `"congruence_percentage"` |
| JSON/Python enum tokens | UPPER_CASE | `"BLACK"`, `ColorToken.BLUE` |

## File Naming

- Python: `snake_case.py` (e.g., `puzzle_generator.py`)
- Tests: `test_<module>.py` (e.g., `test_puzzle_generator.py`)
- Frontend: `kebab-case.html` (e.g., `puzzle.html`)
- Shared data: `snake_case.json` (e.g., `color_labels.json`)

## JSON API Responses

Use camelCase for JSON keys sent to frontend:
- `inkColor` (not `ink_color`)
- `congruencePercentage` (not `congruence_percentage`)
