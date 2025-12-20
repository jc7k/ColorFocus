# Specification: Full UI Localization and Configurable Grid Size

## Goal
Enable complete localization of all UI text elements to match the selected language (Chinese, English, Vietnamese) and allow users to select square grid dimensions from 1x1 to 8x8 via a dropdown, with automatic color count limiting based on grid size for progressive difficulty ramping.

## User Stories
- As a non-English speaker, I want all UI elements (title, instructions, buttons, labels, messages) to display in my selected language so that I can fully understand and use the application.
- As a cognitive training user, I want to choose smaller grid sizes (1x1 to 8x8) so that I can start with easier puzzles and progressively increase difficulty as I improve.

## Specific Requirements

**UI Text Localization System**
- Create `shared/ui_text.json` file containing all translatable UI strings organized by key and language
- Structure mirrors `color_labels.json`: top-level keys are string identifiers, nested keys are language codes (chinese, english, vietnamese)
- Include all static text: page title, subtitle, control labels, button text, section headers, task instructions template, result messages, metadata labels, reveal warning
- Vietnamese text must use proper diacritical marks (e.g., "ngon ngu" becomes "Ngon ngu")
- Load translations at module initialization, not per-request

**Dynamic UI Text Rendering**
- Replace all hardcoded English text in `puzzle.html` with dynamic text from `ui_text.json`
- Update text content whenever language selector changes (no page reload required)
- Use safe DOM manipulation (textContent, createElement) - no innerHTML with dynamic content
- Page `<title>` tag should update to match selected language

**Grid Size Selector**
- Add dropdown selector for grid size (1x1 through 8x8) in the controls section
- Position between Language and Colors dropdowns for logical grouping
- Display as "NxN" format in dropdown options (e.g., "4x4", "8x8")
- Default to 4x4 for accessible starting point
- Optionally persist selection via localStorage (key: `colorFocusGridSize`)

**Dynamic Grid CSS**
- Update `grid-template-columns` to use dynamic column count based on selected grid size
- Apply via inline style or CSS custom property on `.puzzle-grid` element
- Adjust cell sizing proportionally - larger cells for smaller grids
- Maintain aspect-ratio: 1 for square cells at all grid sizes

**Color Count Auto-Limiting**
- Maximum colors = grid size dimension (e.g., 3x3 grid = max 3 colors, 5x5 = max 5 colors)
- Automatically update Colors dropdown max value when grid size changes
- If current color selection exceeds new max, clamp to new max
- Formula: maxColors = min(8, gridSize) where gridSize is the NxN dimension

**Puzzle Generation Updates**
- Frontend: Update `totalCells` calculation to use `gridSize * gridSize` instead of hardcoded 64
- Frontend: Update ink distribution and answer counting logic for variable cell counts
- Adjust font size calculation to account for variable grid dimensions

**Font Size Calculation**
- Modify `calculatePuzzleFontSize()` to accept grid column count as parameter
- Larger cells (smaller grids) should have proportionally larger fonts
- Maintain language-specific multipliers (Chinese: 1.15, Vietnamese: 2.6, English: 4.2)

**Metadata Display Updates**
- Update "Grid:" metadata value to show current grid size dynamically (e.g., "3x3", "8x8")
- All metadata labels (Seed, Colors, Grid, Congruent) should use translated text from `ui_text.json`

## Visual Design
No mockups provided. UI changes should maintain the existing visual style and layout patterns.

## Existing Code to Leverage

**`shared/color_labels.json`**
- Provides the JSON structure pattern for multi-language translations
- Keys are identifiers, values are objects with `chinese`, `english`, `vietnamese` string properties
- New `ui_text.json` should follow this exact structure

**`frontend/puzzle.html` Language Switching Pattern**
- Language selector already persists via localStorage (`colorFocusLanguage` key)
- Event listener pattern updates multiple UI areas on language change: `renderPuzzleDisplay()`, `renderAnswerInputs()`, `renderAnswerKey()`, `updateTaskInstructions()`
- Extend this pattern to include all UI text elements

**`backend/app/constants/color_labels.py`**
- Demonstrates Python module pattern for loading shared JSON at import time
- `Language` enum (StrEnum) with CHINESE, ENGLISH, VIETNAMESE values
- Path resolution pattern: `Path(__file__).parent.parent.parent.parent / "shared" / "..."

**`backend/app/services/puzzle_generator.py`**
- `DEFAULT_COLOR_SUBSETS` dictionary maps color counts to color token lists
- `ROWS` and `COLS` constants (currently 8) - these need to become configurable
- `_create_ink_distribution()` and `_reshape_to_grid()` use these constants

**`frontend/puzzle.html` Font Size Calculation**
- `calculatePuzzleFontSize()` calculates responsive font based on viewport, language, and grid width
- Uses language-specific width multipliers for proper text fitting
- Called after rendering and on window resize

## Out of Scope
- Rectangular (non-square) grids - only NxN square grids are supported
- Additional languages beyond Chinese, English, and Vietnamese
- Backend API endpoint changes - this spec focuses on frontend-only puzzle generation
- Server-side preference storage or user accounts
- Difficulty tier presets or suggested configurations
- Animation or transition effects when changing grid size
- Backend puzzle generator changes (rows/cols are already in PuzzleMetadata but backend remains 8x8)
- Accessibility improvements beyond what already exists (ARIA labels, etc.)
- Mobile-specific grid size restrictions or recommendations
- Internationalization of number formats or date formats
