# Adding New Languages

Process for adding a new language to ColorFocus.

## Files to Update

1. `/shared/color_labels.json` — 8 color translations
2. `/shared/ui_text.json` — All UI strings (~50+ keys)
3. `backend/app/constants/color_labels.py` — Add to `Language` enum
4. `frontend/puzzle.html` — Add to language dropdown + font multiplier

## Steps

1. **Get translations** — Color labels + all UI text keys
2. **Calculate font multiplier** — `longest_word_chars × 0.6`
3. **Update files** — All 4 locations above
4. **Run tests** — `uv run pytest` + `cd frontend && pnpm test`
5. **Native speaker review** — Required before deploy

## Font Multiplier Calculation

```javascript
// Based on longest color word in language
const widthMultipliers = {
  'zh-TW': 1.15,      // 1 char
  'vietnamese': 2.4,  // 4 chars ("Vang")
  'english': 3.6,     // 6 chars ("Yellow")
  'spanish': 4.8      // 8 chars ("Amarillo")
};
```

## Use `/add-language` Command

The `/add-language` slash command automates this process.
