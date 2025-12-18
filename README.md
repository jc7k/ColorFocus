# ColorFocus

A color-based cognitive training application featuring Stroop test puzzles with accessibility-first design.

## Interactive Puzzle Demo

Try the interactive Stroop puzzle at `frontend/puzzle.html`:

```bash
# Start a local server
cd /path/to/ColorFocus
python3 -m http.server 8080

# Open in browser
# http://localhost:8080/frontend/puzzle.html
```

### Features

- **Configurable difficulty**: 2-8 colors, 0-100% congruence
- **Multi-language support**: Chinese, English, and Vietnamese color labels
- **Seed-based generation**: Reproducible puzzles for testing
- **Answer submission**: Enter counts and check accuracy
- **Hidden answer key**: Reveal after attempting
- **Scoring feedback**: Perfect/Good/Needs Work tiers
- **Language persistence**: Preference saved across sessions

### Supported Languages

| Language | Labels |
|----------|--------|
| Chinese | 藍, 橙, 紫, 黑, 青, 金, 品, 灰 |
| English | Blue, Orange, Purple, Black, Cyan, Amber, Magenta, Gray |
| Vietnamese | Xanh, Cam, Tím, Đen, Lơ, Vàng, Hồng, Xám |

### Difficulty Levels

| Colors | Congruence | Difficulty | Description |
|--------|------------|------------|-------------|
| 2 | 12.5% | Easy | Only Blue/Orange, minimal choices |
| 4 | 12.5% | Medium | Default setting |
| 8 | 75% | Medium | Many colors but word often matches ink |
| 8 | 0% | Hardest | Maximum Stroop interference |

**Congruence** controls how often the word meaning matches the ink color. Lower congruence = stronger Stroop effect = harder puzzle.

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
# All Python tests (60 tests)
uv run pytest -v

# Frontend tests (10 tests)
cd frontend && npm test

# Total: 70 tests
```

## Deployment

### Deploy to Vercel (Recommended)

The frontend can be deployed as a static site on Vercel's free tier.

**Option 1: Via GitHub (Automatic Deploys)**

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) and sign in with GitHub
3. Click "New Project" and import your repository
4. Configure the project:
   - **Root Directory:** `./` (project root, not frontend)
   - **Build Command:** (leave empty - static files)
   - **Output Directory:** `./` (project root)
5. Click "Deploy"

Your app will be live at `https://your-project.vercel.app/frontend/puzzle.html`

**Option 2: Via Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from project root
cd /path/to/ColorFocus
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: colorfocus (or your choice)
# - Directory: ./
# - Override settings? No
```

After deployment, access the puzzle at: `https://your-project.vercel.app/frontend/puzzle.html`

**Option 3: Deploy Frontend Only**

To deploy just the frontend folder with cleaner URLs:

```bash
cd frontend
vercel
```

Then access at: `https://your-project.vercel.app/puzzle.html`

### Vercel Configuration (Optional)

Create `vercel.json` in project root for custom settings:

```json
{
  "rewrites": [
    { "source": "/", "destination": "/frontend/puzzle.html" },
    { "source": "/puzzle", "destination": "/frontend/puzzle.html" }
  ]
}
```

This enables cleaner URLs like `https://your-project.vercel.app/puzzle`

## Tech Stack

- **Frontend:** TypeScript, Tailwind CSS, Vitest
- **Backend:** Python 3.11+, pytest
- **Shared:** JSON source of truth for cross-platform constants
- **Hosting:** Vercel (static frontend)
