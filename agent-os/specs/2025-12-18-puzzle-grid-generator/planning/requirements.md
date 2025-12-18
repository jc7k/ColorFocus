# Spec Requirements: Puzzle Grid Generator

## Initial Description

Build the core algorithm that generates 8x8 word jungle grids with color words rendered in different ink colors, creating Stroop interference patterns. This is Item #2 on the roadmap and depends on the Color Token System (Item #1, completed).

## Requirements Discussion

### First Round Questions

**Q1:** Grid Structure: I'm assuming the 8x8 grid contains one color word per cell (64 total words). Is that correct, or should cells be able to hold multiple words or be empty?
**Answer:** It should hold the Chinese name for a color in our palette. (One word per cell, 64 total)

**Q2:** Color Words vs. Ink Colors: For the Stroop interference, I assume each cell displays a color word rendered in a different ink color from that word's meaning (congruent matches avoided). Should we guarantee 100% incongruent pairings, or allow some percentage of congruent word-ink matches for difficulty variation?
**Answer:** Allow some percentage of congruent matches for difficulty variation.

**Q3:** Color Distribution: Should the algorithm aim for roughly equal distribution of ink colors across the 64 cells (approximately 8 cells per color), or should it be weighted/random? This affects the answer key complexity.
**Answer:** Roughly equal with some variation. It should not be heavily skewed.

**Q4:** Word Language: The Color Token System includes Chinese single-character labels. Should the grid generator support both English words ("BLUE", "ORANGE") and Chinese characters as configurable options, or is English-only sufficient for the MVP?
**Answer:** Default Chinese but configurable.

**Q5:** Reproducibility/Seeding: I assume generated puzzles should be reproducible given a seed value (for sharing, debugging, and caching). Is that correct? Should users be able to input a custom seed or should it always be auto-generated?
**Answer:** Should be reproducible and the seed should be visible with the puzzle for ease of traceability.

**Q6:** API vs. Service: Should this be exposed as a REST API endpoint (e.g., POST /puzzles/generate) that returns JSON representing the grid, or is this purely a backend service class for now that will be wired to an API later?
**Answer:** Keep it simple so the app can be deployed on a service like Railway or Vercel easily.

**Q7:** Data Structure: I'm thinking the output should be a 2D array of cell objects, each containing { word: ColorToken, inkColor: ColorToken }. Should we also include metadata like grid dimensions, seed, and difficulty tier in the response?
**Answer:** Yes, 2D array with { word: ColorToken, inkColor: ColorToken } plus metadata. Always try to keep things simple.

**Q8:** Anything to Exclude: Are there any features you specifically do NOT want in this initial puzzle generator? For example: animation data, timing hints, multi-grid batch generation, or saved puzzle persistence?
**Answer:** Animation data, timing hints, batch generation, saved puzzle persistence.

### Existing Code to Reference

**Similar Features Identified:**
- Feature: Color Token System - Path: `/home/user/projects/ColorFocus/backend/app/constants/colors.py`
- Feature: Color Token System (Frontend) - Path: `/home/user/projects/ColorFocus/frontend/src/constants/colors.ts`
- Feature: Shared Color Data - Path: `/home/user/projects/ColorFocus/shared/colors.json`

No additional existing patterns beyond the Color Token System identified for reference.

### Follow-up Questions

No follow-up questions were needed.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
N/A

## Requirements Summary

### Functional Requirements
- Generate 8x8 grids (64 cells total) with one Chinese color word per cell
- Each cell contains a color word displayed in a potentially different ink color (Stroop interference)
- Support configurable percentage of congruent word-ink matches for difficulty variation
- Distribute ink colors roughly equally across the grid (approximately 8 cells per color) with some natural variation
- Default to Chinese character labels with configuration option for language
- Implement deterministic generation using seeds for reproducibility
- Include seed value in puzzle output for traceability
- Return 2D array structure with cell objects containing `{ word: ColorToken, inkColor: ColorToken }`
- Include metadata in response: grid dimensions, seed, difficulty tier
- Use the 8 canonical color tokens: BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY

### Reusability Opportunities
- Color Token System (`ColorToken` enum, `COLORS` dictionary) from backend constants
- Shared color definitions from `shared/colors.json`
- Existing TypeScript color types for frontend consistency

### Scope Boundaries

**In Scope:**
- Core puzzle generation algorithm
- 8x8 grid structure with color word cells
- Stroop interference pattern creation (word-ink mismatch)
- Configurable congruent match percentage
- Roughly equal ink color distribution
- Seed-based reproducible generation
- Simple data structure output (2D array + metadata)
- Chinese character labels (default) with language configuration
- Simple deployment compatibility (Railway/Vercel)

**Out of Scope:**
- Animation data
- Timing hints
- Batch/multi-grid generation
- Saved puzzle persistence/storage
- Answer key generation (separate roadmap item #3)
- Difficulty tier configuration details (separate roadmap item #4)
- UI/display components (separate roadmap item #5)

### Technical Considerations
- Backend implementation in Python (FastAPI) using existing project structure
- Must integrate with existing `ColorToken` and `ColorVariant` enums from `backend/app/constants/colors.py`
- Deployment target: Railway (backend) - keep architecture simple
- Use `uv` and `pyproject.toml` for any new dependencies
- Follow existing code patterns from Color Token System
- Seed value should be included in puzzle response for debugging and sharing
- Algorithm should be deterministic given the same seed
