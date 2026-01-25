# Single-File Architecture

The frontend is a single `puzzle.html` file containing HTML, CSS, and JavaScript.

## Structure

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* All CSS here */
  </style>
</head>
<body>
  <!-- All HTML here -->
  <script type="module">
    // All JavaScript here
  </script>
</body>
</html>
```

## Why Single-File

- **Simpler Vercel deployment** — No bundling, no webpack/vite config
- **Static hosting** — Works with any static file server
- **Vanilla JS only** — No React/Vue/framework dependencies

## Rules

- Keep it in one file unless it exceeds ~3000 lines
- Use `<script type="module">` for ES6 imports (JSON files)
- No build step — code runs directly in browser

## Imports Allowed

```javascript
import colorsJson from '../shared/colors.json' with { type: 'json' };
import labelsJson from '../shared/color_labels.json' with { type: 'json' };
import uiTextJson from '../shared/ui_text.json' with { type: 'json' };
```
