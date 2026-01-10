# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start (Read First)

**New session?** Read these files to get oriented:
1. This file (`CLAUDE.md`) — you're here
2. `/agent-os/product/roadmap.md` — current priorities and completed work
3. Active spec in `/agent-os/specs/` — if working on a feature, check for existing spec

**Verify current behavior:**
- **Live site:** https://colorfocus.vercel.app (always available)
- **CLI only:** Run `uv run pytest -v` and `cd frontend && pnpm test`

## Guidelines
1. First think through the problem, read the codebase for relevant files.
2. Before you make any major changes, check in with me and I will verify the plan.
3. Please every step of the way just give me a high level explanation of what changes you made
4. Make every task and code change you do as simple as possible. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
5. Maintain a documentation file that describes how the architecture of the app works inside and out.
6. Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering. Make sure to investigate and read relevant files BEFORE answering questions about the codebase. Never make any claims about code before investigating unless you are certain of the correct answer - give grounded and hallucination-free answers.
7. Assume no context from previous sessions. Each session (CLI or Web) starts fresh — always re-read relevant files rather than assuming prior knowledge.

## Session Handoff Notes

When switching between CLI and Web, or starting a new session:
- **Check git status** — See what files have uncommitted changes
- **Check roadmap** — `/agent-os/product/roadmap.md` shows completed vs pending work
- **Check active specs** — Look in `/agent-os/specs/` for in-progress features with `tasks.md`
- **Don't duplicate work** — If a spec exists, continue from its current state rather than starting over

## Project Overview

ColorFocus is a Stroop test cognitive training application designed primarily for stroke recovery patients and elderly users. The app displays color words (e.g., "BLUE") rendered in different ink colors, creating Stroop interference patterns for cognitive exercise.

**Live:** https://colorfocus.vercel.app

## Environment Setup

```bash
# First-time setup
uv sync                     # Install Python dependencies
cd frontend && pnpm install # Install frontend dependencies
```

## Commands

### Python Tests (from project root)
```bash
# Run all tests
uv run pytest -v

# Run a single test file
uv run pytest tests/test_puzzle_generator.py -v

# Run a specific test
uv run pytest tests/test_puzzle_generator.py::TestPuzzleGenerator::test_generate_creates_valid_grid -v
```

### Frontend Tests
```bash
cd frontend && pnpm test
```

### Local Development Server
```bash
python3 -m http.server 8080
# Open http://localhost:8080/frontend/puzzle.html
```

### Deploy to Vercel
```bash
vercel --prod
```

## Development Practices

### Code Style
- **Python:** Use `ruff` for linting and formatting (configured in `pyproject.toml`)
- **JavaScript:** Keep code in existing single-file pattern; no build step required
- **CSS:** Mobile-first; use existing spacing/color variables

### Testing
- Add tests for any new puzzle generation logic or color handling
- Run `uv run pytest -v` before committing Python changes
- Run `cd frontend && pnpm test` before committing frontend changes

### Git Commits
- Use imperative mood: "Add feature" not "Added feature"
- Keep commits atomic — one logical change per commit
- Reference issue numbers when applicable: "Fix grid overflow (#42)"

## Architecture

### Directory Structure
```
ColorFocus/
├── frontend/
│   └── puzzle.html      # Main app (single-file: HTML + CSS + JS)
├── backend/app/
│   ├── constants/       # Python enums (colors, labels)
│   ├── models/          # Dataclasses (puzzle, grid)
│   └── services/        # Puzzle generation logic
├── shared/              # Source of truth JSON files
│   ├── colors.json
│   ├── color_labels.json
│   └── ui_text.json
├── tests/               # Python tests
├── agent-os/
│   ├── product/         # Roadmap, mission
│   └── specs/           # Feature specifications
└── CLAUDE.md            # This file
```

### Data Flow: Shared JSON → Platform Constants

The `/shared/` directory contains JSON files that serve as the single source of truth:
- `colors.json` — 8 color tokens (BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY) with hex values
- `color_labels.json` — Multi-language labels (Chinese, English, Spanish, Vietnamese)
- `ui_text.json` — Full UI localization strings

These are consumed by:
- **Frontend:** `puzzle.html` imports JSON directly via ES modules
- **Backend:** Python constants in `backend/app/constants/` load and expose as StrEnums

### Frontend Architecture (Vanilla JS)

The main application is in `frontend/puzzle.html` — a single-file implementation containing:
- CSS styles (including mobile media queries at 480px breakpoint)
- JavaScript puzzle generator (seeded PRNG for reproducibility)
- Dynamic font sizing based on grid size, language, and viewport
- LocalStorage persistence for user preferences

Key JavaScript patterns:
- `currentGridSize`, `currentLanguage`, `currentSpacing` — state variables
- `calculatePuzzleFontSize()` — dynamic font scaling with language-specific multipliers
- `DIFFICULTY_PRESETS` — accessible (3x3), standard (4x4), advanced (8x8)
- `SPACING_VALUES` — compact (1px), normal (2px), relaxed (6px), spacious (12px)

### Backend Architecture (Python)

Located in `backend/app/`:
- `constants/colors.py` — ColorToken enum with hex values
- `constants/color_labels.py` — Language enum and label lookup
- `models/puzzle.py` — PuzzleCell, PuzzleGrid, PuzzleMetadata dataclasses
- `services/puzzle_generator.py` — Deterministic puzzle generation with seed support

### Agent OS Workflow

The project uses Agent OS for spec-driven development:
- `/agent-os/product/roadmap.md` — Product roadmap with checkboxes
- `/agent-os/specs/` — Feature specifications with planning, tasks, and verification
- `/.claude/commands/agent-os/` — Slash commands for spec workflow

Workflow: `/shape-spec` → `/write-spec` → `/create-tasks` → `/implement-tasks`

### File Placement
- **New shared data:** Add to `/shared/*.json`, then update both frontend and backend consumers
- **New Python modules:** Place in appropriate `backend/app/` subdirectory
- **New tests:** Mirror source structure in `/tests/` (e.g., `test_puzzle_generator.py`)
- **Specs:** Create in `/agent-os/specs/YYYY-MM-DD-feature-name/`

## Key Constraints

- **Accessibility first:** All colors validated for deuteranopia, protanopia, tritanopia
- **Target users:** Stroke patients and elderly — prioritize legibility and simplicity
- **Python dependencies:** Always use `uv` and `pyproject.toml`, never `pip` directly
- **Python execution:** Never run python directly; use `uv run` or activate `.venv`
- **Static frontend:** Vercel deployment serves `frontend/` as static files only

### Browser Compatibility
- Support modern evergreen browsers (Chrome, Firefox, Safari, Edge — latest 2 versions)
- Must work on iOS Safari and Android Chrome (tablet use is common for elderly users)
- Avoid features requiring polyfills; keep JavaScript simple and widely compatible

### Performance Guidelines
- Keep initial page load fast — no heavy frameworks or large assets
- Avoid animations that could cause disorientation or seizures
- Test on slower devices; target users may have older hardware

### Protected Files (Require Extra Review)
- `/shared/colors.json` — Color changes affect accessibility; validate with color blindness simulators
- `/shared/color_labels.json` — Translations require native speaker verification
- `frontend/puzzle.html` — Core app; changes ripple widely

## Language-Specific Font Scaling

Font sizing uses multipliers based on longest word per language:
- Chinese: 1.15 (single character)
- Vietnamese: 2.6 (3-5 characters)
- English: 4.2 (MAGENTA = 7 chars)
- Spanish: 4.2 (NARANJA = 7 chars)

Formula: `fontSize = (cellWidth * 0.8) / languageMultiplier`

## Common Tasks by Context

| Task | CLI | Web |
|------|-----|-----|
| Read/edit code | ✓ Full access | ✓ Full access |
| Run tests | ✓ `uv run pytest` | ✗ Check live site instead |
| Start dev server | ✓ `python3 -m http.server` | ✗ Use live site |
| Deploy | ✓ `vercel --prod` | ✗ Request CLI deploy |
| Git operations | ✓ Full access | ✗ Read-only status |
| Check behavior | ✓ Tests + live site | ✓ Live site only |
| Review specs | ✓ Full access | ✓ Full access |
