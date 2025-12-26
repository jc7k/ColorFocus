# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ColorFocus is a Stroop test cognitive training application designed primarily for stroke recovery patients and elderly users. The app displays color words (e.g., "BLUE") rendered in different ink colors, creating Stroop interference patterns for cognitive exercise.

**Live:** https://colorfocus.vercel.app

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

## Architecture

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

## Key Constraints

- **Accessibility first:** All colors validated for deuteranopia, protanopia, tritanopia
- **Target users:** Stroke patients and elderly — prioritize legibility and simplicity
- **Python dependencies:** Always use `uv` and `pyproject.toml`, never `pip` directly
- **Python execution:** Never run python directly; use `uv run` or activate `.venv`
- **Static frontend:** Vercel deployment serves `frontend/` as static files only

## Language-Specific Font Scaling

Font sizing uses multipliers based on longest word per language:
- Chinese: 1.15 (single character)
- Vietnamese: 2.6 (3-5 characters)
- English: 4.2 (MAGENTA = 7 chars)
- Spanish: 4.2 (NARANJA = 7 chars)

Formula: `fontSize = (cellWidth * 0.8) / languageMultiplier`
