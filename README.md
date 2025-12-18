# ColorFocus

A color-based cognitive training application featuring Stroop test puzzles with accessibility-first design.

## Color Token System

The foundation of the application is a color token system optimized for color-blind accessibility.

### 8 Canonical Colors

| Token   | Dark | Base | Bright |
|---------|------|------|--------|
| BLUE    | Yes  | Yes  | Yes    |
| ORANGE  | Yes  | Yes  | Yes    |
| PURPLE  | Yes  | Yes  | Yes    |
| BLACK   | No   | Yes  | Yes    |
| CYAN    | Yes  | Yes  | Yes    |
| AMBER   | Yes  | Yes  | Yes    |
| MAGENTA | Yes  | Yes  | Yes    |
| GRAY    | Yes  | Yes  | Yes    |

**23 total color values** - All colors validated for deuteranopia, protanopia, and tritanopia accessibility.

### Architecture

```
/shared/
  colors.json              # Single source of truth

/frontend/
  src/constants/colors.ts  # TypeScript constants (ColorToken enum, COLORS object)
  tailwind.config.js       # Extended with color utilities (e.g., text-blue-base, bg-orange-bright)

/backend/
  app/constants/colors.py  # Python constants (StrEnums, COLORS dict)
```

### Usage

**TypeScript:**
```typescript
import { ColorToken, COLORS, getColor } from '@/constants/colors';

// Access color directly
const blueBase = COLORS[ColorToken.BLUE].base; // "#2563EB"

// Or use helper
const color = getColor(ColorToken.ORANGE, 'bright'); // "#FB923C"
```

**Python:**
```python
from backend.app.constants import ColorToken, ColorVariant, COLORS

# Access color
blue_base = COLORS[ColorToken.BLUE]["base"]  # "#2563EB"
```

**Tailwind CSS:**
```html
<div class="text-blue-base bg-orange-bright border-purple-dark">
  Color token classes
</div>
```

## Development

### Prerequisites

- Node.js 18+
- Python 3.11+
- uv (Python package manager)

### Setup

**Frontend:**
```bash
cd frontend
npm install
npm test
```

**Backend:**
```bash
uv sync
uv run pytest
```

### Running Tests

```bash
# All Python tests (21 tests)
uv run pytest -v

# Frontend tests (10 tests)
cd frontend && npm test

# Total: 31 tests
```

## Tech Stack

- **Frontend:** TypeScript, Tailwind CSS, Vitest
- **Backend:** Python 3.11+, pytest
- **Shared:** JSON source of truth for cross-platform constants
