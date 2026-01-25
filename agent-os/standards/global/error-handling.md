# Error Handling

Pattern for handling failures gracefully while maintaining visibility.

## Core Pattern

**Log + Return Default**

```python
def get_language(code: str) -> Language:
    if code not in VALID_CODES:
        logger.warning("Invalid language code: %s, using default", code)
        return Language.ZH_TW
    return Language(code)
```

## Rules

1. **Always log unexpected failures** — Use `logger.warning()` for recoverable issues
2. **Return safe defaults** — Never crash on invalid input
3. **Be specific in log messages** — Include the invalid value and what default was used
4. **Don't log expected validation** — Normal input validation doesn't need logging

## JavaScript Pattern

```javascript
function sanitizeNumber(value, min, max, defaultValue) {
  const num = parseFloat(value);
  if (isNaN(num)) {
    console.warn(`Invalid number: ${value}, using default: ${defaultValue}`);
    return defaultValue;
  }
  return Math.max(min, Math.min(max, num));
}
```
