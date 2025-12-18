# Specification: Puzzle Grid Generator

## Goal

Build a deterministic algorithm that generates 8x8 word jungle grids with color words rendered in different ink colors, creating Stroop interference patterns for cognitive training exercises.

## User Stories

- As a user, I want to receive a randomized puzzle grid so that I can practice attention control by counting ink colors while ignoring word meanings
- As a developer, I want reproducible puzzle generation via seeds so that puzzles can be shared, debugged, and cached reliably

## Specific Requirements

**Grid Structure**
- Generate an 8x8 grid (64 cells total)
- Each cell contains exactly one color word (Chinese character by default)
- Use the 8 canonical color tokens: BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY
- Chinese labels per PRD Section 5.2: BLUE=藍, ORANGE=橙, PURPLE=紫, BLACK=黑, CYAN=青, AMBER=金, MAGENTA=品, GRAY=灰
- Language should be configurable with Chinese as the default

**Stroop Interference Pattern**
- Each cell has two properties: the word (semantic meaning) and the ink color (display color)
- Support configurable percentage of congruent matches (word meaning equals ink color)
- Default should be mostly incongruent pairings for maximum Stroop interference
- Congruence percentage parameter enables difficulty variation

**Color Distribution**
- Distribute ink colors roughly equally across the 64 cells (approximately 8 cells per color)
- Allow natural variation but prevent heavy skewing toward any single color
- Ensure no color appears significantly more or less than others

**Seed-Based Reproducibility**
- Accept an optional seed parameter for deterministic generation
- Auto-generate a seed if none provided
- Use Python's random module with explicit seeding for reproducibility
- Include the seed value in the puzzle output for traceability and sharing

**Output Data Structure**
- Return a 2D array (list of lists) with cell objects containing `{ word: ColorToken, inkColor: ColorToken }`
- Include metadata: grid dimensions (rows, columns), seed value, congruence percentage
- Keep the structure simple and JSON-serializable for API responses
- Follow existing ColorToken enum pattern from `backend/app/constants/colors.py`

**Service Architecture**
- Implement as a Python service class in the backend, not an API endpoint initially
- Design for easy integration into a FastAPI route later
- Keep architecture simple for deployment on Railway or Vercel
- Place in `backend/app/services/` following project conventions

**Algorithm Design**
- First, generate the ink color distribution (roughly equal across colors)
- Then, assign word values based on congruence percentage parameter
- Shuffle cell positions for spatial randomness
- Validate output meets distribution constraints before returning

## Visual Design

No visual assets provided.

## Existing Code to Leverage

**Color Token System (Backend)**
- Path: `/home/user/projects/ColorFocus/backend/app/constants/colors.py`
- Provides `ColorToken` StrEnum with all 8 canonical colors
- Provides `ColorVariant` enum for brightness variants (DARK, BASE, BRIGHT)
- Use `ColorToken` enum directly in the puzzle generator for type safety

**Shared Color Data**
- Path: `/home/user/projects/ColorFocus/shared/colors.json`
- Source of truth for hex values and HSL references
- Generator does not need hex values directly (those are for rendering)
- Labels (Chinese characters) should be added to shared data or defined in generator

**Color Token System (Frontend)**
- Path: `/home/user/projects/ColorFocus/frontend/src/constants/colors.ts`
- Same enum pattern mirrored in TypeScript
- Frontend will consume puzzle JSON and use this for rendering

**Project Configuration**
- Path: `/home/user/projects/ColorFocus/pyproject.toml`
- Use `uv` for dependency management, not pip directly
- Tests go in `/home/user/projects/ColorFocus/tests/`

## Out of Scope

- Animation data or timing information in puzzle output
- Timing hints or performance metrics
- Batch/multi-grid generation in a single request
- Saved puzzle persistence or database storage
- Answer key generation (separate roadmap item)
- Difficulty tier configuration or presets (separate roadmap item)
- UI/display components or rendering logic
- REST API endpoint creation (will be added later)
- Spatial constraints validation (max adjacent identical colors)
- Grid size configuration beyond 8x8 (future enhancement)
