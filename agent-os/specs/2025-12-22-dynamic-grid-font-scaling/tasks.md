# Task Breakdown: Dynamic Grid/Font Scaling

## Overview
Total Tasks: 4 Task Groups (Frontend-only implementation in puzzle.html)

This feature enhances the ColorFocus puzzle grid to scale dynamically based on grid size and language, ensuring text fills approximately 80% of cell width while maintaining legibility for stroke patients and elderly users.

## Task List

### CSS Layer

#### Task Group 1: Container and Cell CSS Updates
**Dependencies:** None

- [x] 1.0 Complete CSS layer updates
  - [x] 1.1 Write 3-5 focused Playwright tests for container scaling
    - Test container max-width changes from 520px to 800px
    - Test container fills viewport width up to 800px maximum
    - Test mobile viewport (under 480px) uses 100% width minus padding
    - Test container remains centered with side margins on large screens
  - [x] 1.2 Update `.puzzle-grid` max-width from 520px to 800px
    - Location: `/home/user/projects/ColorFocus/frontend/puzzle.html` lines 91-97
    - Change `max-width: 520px` to `max-width: 800px`
    - Maintain existing `display: grid`, `margin: 0 auto`, and gap properties
  - [x] 1.3 Verify mobile CSS overrides remain functional
    - Location: lines 396-408 (mobile media query)
    - Ensure `width: 100%` and `gap: 1px` still apply under 480px viewport
    - No changes needed if existing mobile rules work correctly
  - [x] 1.4 Run container scaling tests
    - Run ONLY the 3-5 tests written in 1.1
    - Verify container scales correctly at various viewport widths
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 3-5 tests written in 1.1 pass
- Container scales to 800px max on desktop
- Container fills 100% width minus padding on mobile
- Centered layout with margins on large monitors preserved

### JavaScript Layer

#### Task Group 2: Dynamic Font Size Calculation
**Dependencies:** Task Group 1

- [x] 2.0 Complete dynamic font sizing logic
  - [x] 2.1 Write 5-8 focused Playwright tests for font calculation
    - Test font size scales proportionally with cell size (8x8, 4x4, 2x2, 1x1)
    - Test 80% text width target (font sizing leaves ~10% margin each side)
    - Test language-specific multipliers produce proportional sizes (Chinese ~3-4x larger than English)
    - Test font recalculates on window resize
    - Test font recalculates on grid size change
    - Test font recalculates on language change
    - Test font recalculates on spacing setting change
  - [x] 2.2 Refactor `calculatePuzzleFontSize()` to remove hardcoded max caps
    - Location: `/home/user/projects/ColorFocus/frontend/puzzle.html` lines 926-965
    - Remove the fixed `maxFontSizes` object (lines 958-960)
    - Remove the `Math.min(maxFontSize, fontSize)` clamping (line 962)
    - Keep language width multipliers: Chinese (1.15), Vietnamese (2.6), English (4.2), Spanish (4.2)
  - [x] 2.3 Implement dynamic font calculation formula
    - Formula: `baseFontSize = (cellWidth * 0.8) / languageWidthMultiplier`
    - The 0.8 factor achieves the 80% text width with 10% margins
    - Cell width calculation must account for spacing gaps
    - Use `SPACING_VALUES` constant (lines 646-651) for accurate gap calculation
  - [x] 2.4 Update cell width calculation for all spacing options
    - Current code only handles 1px (mobile) and 2px (desktop) gaps
    - Must support: compact (1px), normal (2px), relaxed (6px), spacious (12px)
    - Formula: `cellWidth = (gridWidth - (columns - 1) * gapValue) / columns`
    - Get current spacing from dropdown selection or state variable
  - [x] 2.5 Implement minimum font size floor based on cell dimensions
    - Remove fixed minFontSize values (currently 6px mobile, 10px desktop)
    - Set minimum based on cell fitting: font cannot exceed cell dimensions
    - Consider a practical floor (e.g., 4px) below which text becomes unreadable
  - [x] 2.6 Add recalculation triggers for all relevant events
    - Window resize (already exists, verify still works)
    - Grid size change (call `applyPuzzleFontSize()` in grid size handler)
    - Language change (call `applyPuzzleFontSize()` in language handler)
    - Spacing change (call `applyPuzzleFontSize()` in spacing handler)
  - [x] 2.7 Run font calculation tests
    - Run ONLY the 5-8 tests written in 2.1
    - Verify font sizes scale correctly across grid sizes
    - Verify language-specific proportions are maintained
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 5-8 tests written in 2.1 pass
- No hardcoded max font sizes limiting scaling
- Font sizes scale proportionally with cell sizes
- Chinese characters ~3-4x larger than English/Spanish for same cell
- Text occupies approximately 80% of cell width
- Font recalculates on resize, grid change, language change, and spacing change

### Integration Layer

#### Task Group 3: Cross-Browser and Responsive Integration
**Dependencies:** Task Groups 1-2

- [x] 3.0 Complete integration and responsive handling
  - [x] 3.1 Write 4-6 focused Playwright tests for integration scenarios
    - Test orientation change on mobile triggers font recalculation
    - Test all four languages render correctly at 8x8 grid
    - Test all four languages render correctly at 2x2 grid
    - Test all spacing options (compact, normal, relaxed, spacious) with font scaling
    - Test backward compatibility: difficulty presets (accessible, standard, advanced) still work
  - [x] 3.2 Verify mobile orientation change handling
    - Add orientation change event listener if not present
    - Call `applyPuzzleFontSize()` on orientation change
    - Test portrait and landscape orientations
  - [x] 3.3 Ensure backward compatibility with difficulty presets
    - Verify accessible preset (3x3 grid) scales correctly
    - Verify standard preset (4x4 grid) scales correctly
    - Verify advanced preset (8x8 grid) scales correctly
    - No changes to `DIFFICULTY_PRESETS` constant needed
  - [x] 3.4 Test grid sizes from 1x1 through 8x8
    - Approximate cell sizes at 800px container: 8x8 (~100px), 4x4 (~200px), 2x2 (~400px), 1x1 (~800px)
    - Verify fonts scale proportionally with these cell sizes
    - Verify all languages remain legible at all grid sizes
  - [x] 3.5 Run integration tests
    - Run ONLY the 4-6 tests written in 3.1
    - Verify all integration scenarios pass
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 4-6 tests written in 3.1 pass
- Orientation changes trigger proper recalculation
- All difficulty presets continue to work
- All grid sizes from 1x1 to 8x8 scale correctly
- All four languages (Chinese, English, Spanish, Vietnamese) render correctly

### Testing Layer

#### Task Group 4: Test Review and Comprehensive Verification
**Dependencies:** Task Groups 1-3

- [x] 4.0 Review existing tests and verify feature completeness
  - [x] 4.1 Review tests from Task Groups 1-3
    - Review the 3-5 tests written for CSS layer (Task 1.1)
    - Review the 5-8 tests written for JavaScript layer (Task 2.1)
    - Review the 4-6 tests written for integration (Task 3.1)
    - Total existing tests: approximately 12-19 tests
  - [x] 4.2 Analyze test coverage gaps for THIS feature only
    - Identify critical user workflows that lack test coverage
    - Focus ONLY on gaps related to dynamic grid/font scaling
    - Do NOT assess entire application test coverage
    - Prioritize end-to-end workflows over unit test gaps
  - [x] 4.3 Write up to 8 additional strategic tests maximum
    - Test matrix: all 4 languages x key grid sizes (2x2, 4x4, 8x8) if not covered
    - Test edge cases: smallest grid (1x1), largest grid (8x8), viewport extremes
    - Test all spacing options with multiple languages if not covered
    - Focus on visual verification that text fits within cells with margins
  - [x] 4.4 Run all feature-specific tests
    - Run all tests from 1.1, 2.1, 3.1, and 4.3 together
    - Expected total: approximately 20-27 tests maximum
    - Verify all critical workflows pass
    - Do NOT run unrelated application tests
  - [x] 4.5 Manual visual verification checklist
    - Verify Chinese text (single character) displays ~3-4x larger than English
    - Verify English/Spanish longest words (MAGENTA, NARANJA) fit within cells
    - Verify Vietnamese words fit within cells with proper margins
    - Verify no text overflow or clipping occurs at any grid size
    - Verify 10% visual margins are present on cell sides

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 20-27 tests total)
- Critical user workflows for this feature are covered
- No more than 8 additional tests added when filling in gaps
- Visual verification confirms text fits properly across all scenarios
- Backward compatibility with existing difficulty presets confirmed

## Execution Order

Recommended implementation sequence:
1. CSS Layer (Task Group 1) - Update container max-width
2. JavaScript Layer (Task Group 2) - Refactor font calculation logic
3. Integration Layer (Task Group 3) - Handle responsive and cross-browser scenarios
4. Testing Layer (Task Group 4) - Review, fill gaps, and verify

## Technical Notes

### File to Modify
- `/home/user/projects/ColorFocus/frontend/puzzle.html` (single file implementation)

### Key Code Locations
- `.puzzle-grid` CSS: lines 91-97
- `.puzzle-cell` CSS: lines 98-112
- Mobile media query: lines 395-408
- `SPACING_VALUES` constant: lines 646-651
- `calculatePuzzleFontSize()` function: lines 926-965
- `applyPuzzleFontSize()` function: lines 968-973

### Language Width Multipliers (existing values to maintain)
- Chinese: 1.15 (single character per color)
- Vietnamese: 2.6 (3-5 characters)
- English: 4.2 (3-7 characters)
- Spanish: 4.2 (4-7 characters)

### Spacing Values (existing constant)
- compact: 1px
- normal: 2px
- relaxed: 6px
- spacious: 12px

### Testing Framework
- Use Playwright for browser-based testing
- Tests location: `/home/user/projects/ColorFocus/tests/`
- Python test runner with `uv run pytest`
