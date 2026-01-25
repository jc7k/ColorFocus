# State Management

Vanilla JS state using module-level variables and localStorage.

## State Variables

```javascript
// Transient state (lost on reload)
let currentPuzzle = null;
let correctAnswers = {};
let selectedTiles = new Set();

// Persistent state (localStorage)
let currentLanguage = validateLanguage(localStorage.getItem('colorFocusLanguage'));
let currentGridSize = validateGridSize(localStorage.getItem('colorFocusGridSize'));
let currentDifficulty = validateDifficulty(localStorage.getItem('colorFocusDifficulty'));
let currentSpacing = validateSpacing(localStorage.getItem('colorFocusSpacing'));
```

## Persistence Rules

**Persist to localStorage:**
- User preferences (language, spacing, sound)
- Difficulty settings
- Grid size

**Keep in memory only:**
- Current puzzle data
- Answer state
- UI interaction state (selections, modal state)

## Validation Pattern

Always validate localStorage values before use:

```javascript
function validateLanguage(lang) {
  return VALID_LANGUAGES.includes(lang) ? lang : 'zh-TW';
}

function validateGridSize(size) {
  const num = parseInt(size, 10);
  return VALID_GRID_SIZES.includes(num) ? num : 4;
}
```

## localStorage Keys

Prefix all keys with `colorFocus`:
- `colorFocusLanguage`
- `colorFocusGridSize`
- `colorFocusDifficulty`
- `colorFocusSpacing`
- `colorFocusSoundEnabled`
