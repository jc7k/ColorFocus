# Input Sanitization

Functions to prevent injection and validate user input.

## XSS Prevention

```javascript
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
```

Use when inserting user-provided text into DOM.

## Numeric Validation

```javascript
function sanitizeNumber(value, min, max, defaultValue) {
  const num = parseFloat(value);
  if (isNaN(num)) return defaultValue;
  return Math.max(min, Math.min(max, num));
}
```

Use for seed, grid size, congruence percentage.

## Allowlist Validation

```javascript
function validateLanguage(lang) {
  return VALID_LANGUAGES.includes(lang) ? lang : 'zh-TW';
}
```

**Pattern:** Check against known-good values, return default if invalid.

## Rules

- Never insert raw user input into DOM
- Validate localStorage values before use
- Use allowlists, not blocklists
- Return safe defaults for invalid input
