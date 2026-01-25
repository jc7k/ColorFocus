# UI Text Structure

JSON structure for localized UI strings.

## File Location

`/shared/ui_text.json`

## Structure

```json
{
  "key_name": {
    "zh-TW": "中文翻譯",
    "english": "English text",
    "spanish": "Texto en español",
    "vietnamese": "Van ban tieng Viet"
  }
}
```

## Key Naming

- Use `snake_case` for all keys
- Suffix pattern: `_btn`, `_label`, `_header`, `_message`
- Examples: `generate_btn`, `language_label`, `results_header`

## Interpolation

Use `{placeholder}` syntax for dynamic values:

```json
{
  "result_good": {
    "english": "You got {correct} out of {total} colors correct."
  }
}
```

## Fallback Chain

```javascript
function getUIText(key) {
  // 1. Try current language
  if (uiTextJson[key]?.[currentLanguage]) return uiTextJson[key][currentLanguage];
  // 2. Fall back to English
  if (uiTextJson[key]?.['english']) return uiTextJson[key]['english'];
  // 3. Return key as last resort
  return key;
}
```
