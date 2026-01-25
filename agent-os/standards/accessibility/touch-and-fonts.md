# Touch Targets & Font Sizing

Minimum sizes for elderly users and tablet use.

## Touch Targets

- **44px minimum** for all interactive elements (buttons, inputs, clickable cells)
- No exceptions — even puzzle grid cells must meet this threshold
- CSS: `min-height: var(--btn-min-height);` where `--btn-min-height: 44px`

## Base Font Size

- Body: `1.0625rem` (17px) — larger than default for elderly users
- Use system fonts: `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

## Language-Specific Font Multipliers

Puzzle cells scale font based on longest word per language:

```javascript
const widthMultipliers = {
  'zh-TW': 1.15,      // Single character
  'vietnamese': 2.4,  // "Vang" (4 chars)
  'english': 3.6,     // "Yellow" (6 chars)
  'spanish': 4.8      // "Amarillo" (8 chars)
};
```

Formula: `fontSize = (cellWidth * 0.8) / multiplier`
