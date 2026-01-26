# Frontend Module Architecture

The frontend uses ES modules for code organization while maintaining static file deployment.

## Structure

```
frontend/
├── puzzle.html          # Entry point (HTML + imports)
├── styles/
│   └── puzzle.css       # All CSS
└── src/
    └── modules/         # ES module JavaScript files
        ├── config.js    # Constants, validation
        ├── state.js     # State management
        ├── puzzle.js    # Puzzle generation
        └── ...          # Other modules
```

## Rules

- **Entry point:** `puzzle.html` contains HTML structure and module imports
- **CSS:** External stylesheet linked via `<link rel="stylesheet">`
- **JavaScript:** ES modules in `src/modules/`, each 300-500 lines max
- **No build step:** Code runs directly in browser via ES module imports
- **Static hosting:** Works with Vercel and any static file server

## Module Organization

Each JS module should:
- Have a single responsibility
- Export named functions/constants
- Stay within 300-500 lines
- Include JSDoc comments for exports

## Imports Pattern

```html
<!-- puzzle.html -->
<link rel="stylesheet" href="styles/puzzle.css">
<script type="module">
  import { generatePuzzle } from './src/modules/puzzle.js';
  import { initState } from './src/modules/state.js';
  // ...
</script>
```

```javascript
// modules can import shared data
const response = await fetch('/shared/colors.json');
const colors = await response.json();
```
