# Cross-Platform Sync Tests

Tests that catch drift between source JSON and platform consumers.

## Test File

`tests/test_cross_platform_sync.py`

## What to Test

1. **Python matches source**: Every JSON key exists in Python StrEnum, hex values match
2. **TypeScript imports source**: Verify TS file imports from `shared/*.json` (not duplicated)
3. **All tokens covered**: Source JSON tokens exist in both platform enums
4. **JSON structure valid**: Expected token count, valid hex format (`#RRGGBB`)

## Example Assertion

```python
def test_python_constants_match_source_json():
    source = json.load(open("shared/colors.json"))
    for token, expected_hex in source.items():
        assert COLORS[ColorToken(token)] == expected_hex
```

## Rules

- No exceptions — sync tests must always pass
- Run on every commit via `uv run pytest`
- Failure = immediate fix required before merge
