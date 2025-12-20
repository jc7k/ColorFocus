# Spec Requirements: Full Localization and Configurable Grid

## Initial Description
The in-game instructions and status labels should all match the language selected for the game board. Also, allow the user to choose the dimension of the game board all the way from 1x1 to 8x8. This allows them to slowly ramp the difficulty of the task.

## Requirements Discussion

### First Round Questions

**Q1:** I notice the current UI has hardcoded English text in several places: the page title ("ColorFocus Stroop Puzzle"), subtitle ("Count the INK colors..."), task instructions, control labels ("Language:", "Colors:", "Seed:", "Match %:"), button text ("Generate", "Random", "Check Answers", "Clear", "Reveal"), section headers ("Enter Your Answers", "Results", "Answer Key"), result messages, and metadata labels. I assume you want ALL of these UI elements to be translated to match the selected language (Chinese, English, or Vietnamese). Is that correct, or should some elements like the app title remain in English?
**Answer:** Translate ALL UI text - nothing stays in English

**Q2:** For the translated text, I assume we should follow the same JSON-based approach as `color_labels.json` - creating a new `shared/ui_text.json` file that contains all translatable strings. Is that correct, or would you prefer a different localization approach?
**Answer:** Yes - use JSON file approach (like color_labels.json) for translations

**Q3:** The current Vietnamese color labels use proper diacritical marks (e.g., "Xanh", "Vang", "Tim"). I assume the Vietnamese UI text should also use proper diacritical marks. Is that correct?
**Answer:** Yes - Vietnamese with proper diacritical marks

**Q4:** You mentioned allowing grid sizes from 1x1 to 8x8. I assume you mean square grids only (NxN), not rectangular grids (e.g., 3x5). Is that correct, or should we also allow non-square grid dimensions?
**Answer:** Square grids only (NxN)

**Q5:** Currently the backend generator is hardcoded to 8x8 (64 cells) with distribution validation tuned for that size. For smaller grids like 1x1 (1 cell), 2x2 (4 cells), or 3x3 (9 cells), the color distribution across all 8 colors becomes impossible. I assume for smaller grids we should automatically limit the number of available colors (e.g., a 2x2 grid would only use 2 colors max). Is that the behavior you expect, or should users still be able to select more colors than cells?
**Answer:** Yes - auto-limit max colors based on grid size

**Q6:** For very small grids (1x1, 2x2), the Stroop interference challenge becomes minimal. I assume these are intended for initial cognitive recovery/accessibility purposes for users just starting out, and the full challenge comes with larger grids. Is that correct?
**Answer:** Yes - small grids are for beginner/recovery use

**Q7:** Should the grid size selector be a dropdown (like the colors selector), a slider, or two separate inputs for rows and columns?
**Answer:** Dropdown for grid size selector (to keep it compact)

**Q8:** Currently, the selected language persists via localStorage. I assume the selected grid size should also persist between sessions. Is that correct?
**Answer:** Optional to persist grid size - needs to be deployable on Vercel (localStorage is fine since it's client-side)

**Q9:** Is there anything specific you want to EXCLUDE from this feature? For example: keeping the page `<title>` tag in English for SEO purposes, or excluding certain UI elements from translation?
**Answer:** No exclusions - translate everything

### Existing Code to Reference

No similar existing features identified for reference. However, the following existing patterns should be followed:

- `shared/color_labels.json`: JSON structure for multi-language translations (Chinese, English, Vietnamese)
- `frontend/puzzle.html`: Current UI implementation with language selector and localStorage persistence
- `backend/app/constants/color_labels.py`: Python module for loading JSON translations with Language enum
- `backend/app/services/puzzle_generator.py`: Current grid generation logic (8x8 hardcoded)
- `backend/app/models/puzzle.py`: PuzzleMetadata dataclass with rows/cols fields

### Follow-up Questions

No follow-up questions were needed.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
N/A - No visuals to analyze.

## Requirements Summary

### Functional Requirements

**Full UI Localization:**
- Translate ALL UI text elements to match selected language (Chinese, English, Vietnamese)
- Include: page title, subtitle, task instructions, control labels, button text, section headers, result messages, metadata labels, warning messages
- Use proper Vietnamese diacritical marks for all Vietnamese text
- Follow JSON-based approach with new `shared/ui_text.json` file containing all translatable strings
- UI language changes dynamically when user selects a different language (no page reload required)

**Configurable Grid Size:**
- Allow user to select grid dimensions from 1x1 to 8x8 (square grids only)
- Implement as dropdown selector (compact UI, consistent with existing color selector)
- Auto-limit maximum available colors based on grid size:
  - 1x1 grid: max 1 color (no Stroop effect possible)
  - 2x2 grid: max 2 colors
  - 3x3 grid: max 3 colors (9 cells / 3 = 3 cells per color minimum)
  - 4x4 grid: max 4 colors
  - And so on, up to 8x8 with max 8 colors
- Update puzzle grid CSS to handle variable column counts (currently hardcoded to 8)
- Adjust cell sizing/font sizing for different grid dimensions

**Persistence:**
- Grid size preference may optionally persist via localStorage (client-side only)
- Must remain deployable on Vercel (no server-side session storage required)

### Reusability Opportunities

- Follow `shared/color_labels.json` structure for new `shared/ui_text.json`
- Reuse Language enum from `backend/app/constants/color_labels.py`
- Extend existing localStorage pattern used for language persistence
- Adapt existing grid generation algorithm in `puzzle_generator.py` for variable dimensions

### Scope Boundaries

**In Scope:**
- Complete UI text localization for all three languages
- New JSON translation file for UI strings
- Grid size dropdown selector (1x1 through 8x8)
- Dynamic color count limiting based on grid size
- Responsive grid CSS for variable dimensions
- Frontend puzzle generation updates for variable grid sizes
- Backend puzzle generator updates for variable grid sizes
- Optional localStorage persistence for grid size

**Out of Scope:**
- Rectangular (non-square) grids
- Additional languages beyond Chinese, English, Vietnamese
- Backend API changes (current implementation is frontend-only)
- User accounts or server-side preference storage
- Difficulty tier presets (separate roadmap item)

### Technical Considerations

- Frontend is vanilla HTML/JS with ES modules (no React framework yet)
- Translations loaded via ES module imports from JSON files
- Grid CSS uses `grid-template-columns: repeat(8, 1fr)` - needs to be dynamic
- Font sizing calculation in `calculatePuzzleFontSize()` may need adjustment for smaller grids
- Backend `PuzzleGenerator` class has hardcoded `ROWS = 8` and `COLS = 8` constants
- `DistributionValidator` bounds need to scale with grid size and color count
- Deployment target is Vercel (static frontend hosting)
