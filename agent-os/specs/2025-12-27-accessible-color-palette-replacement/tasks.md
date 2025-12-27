# Task Breakdown: Accessible Color Palette Replacement

## Overview
Total Tasks: 28

This feature replaces the current 8-color palette with a luminance-ordered, accessibility-optimized palette. Key changes include:
- New color tokens: BLACK, BROWN, PURPLE, BLUE, GRAY, PINK, ORANGE, YELLOW
- Removed color tokens: CYAN, AMBER, MAGENTA
- Simplified JSON structure (flat hex values, no variants)
- Language key rename: "chinese" to "zh-TW"
- Dark borders on all colored elements
- Recalculated font sizing multipliers

## Task List

### Shared Data Layer

#### Task Group 1: JSON Data Files Update
**Dependencies:** None

- [x] 1.0 Complete shared JSON data updates
  - [x] 1.1 Write 4 focused tests for JSON structure validation
    - Test colors.json contains exactly 8 color tokens with flat hex values
    - Test color_labels.json contains all 8 colors with 4 language keys including "zh-TW"
    - Test ui_text.json contains "zh-TW" key (not "chinese") in all entries
    - Test all hex values are valid 7-character format (#RRGGBB)
  - [x] 1.2 Update `/home/user/projects/ColorFocus/shared/colors.json`
    - Replace nested variant structure with flat hex values
    - New tokens: BLACK (#1A1A1A), BROWN (#8B4513), PURPLE (#7B4BAF), BLUE (#0066CC), GRAY (#808080), PINK (#E75480), ORANGE (#FF8C00), YELLOW (#FFD700)
    - Remove: CYAN, AMBER, MAGENTA tokens
    - Remove: hsl_reference and variants objects entirely
  - [x] 1.3 Update `/home/user/projects/ColorFocus/shared/color_labels.json`
    - Replace all color entries with new 8-color palette labels
    - Rename "chinese" key to "zh-TW" in all color objects
    - Labels per spec: Black/Brown/Purple/Blue/Gray/Pink/Orange/Yellow
    - zh-TW labels: Black=black, Brown=brown, Purple=purple, Blue=blue, Gray=gray, Pink=pink, Orange=orange, Yellow=yellow
    - Vietnamese labels use ASCII-friendly versions (Den, Nau, Tim, Xanh, Xam, Hong, Cam, Vang)
  - [x] 1.4 Update `/home/user/projects/ColorFocus/shared/ui_text.json`
    - Rename all "chinese" keys to "zh-TW" throughout the file
    - Update `language_descriptor_chinese` key to `language_descriptor_zh-TW`
    - Preserve all existing localized text content
  - [x] 1.5 Run JSON structure validation tests
    - Run ONLY the 4 tests written in 1.1
    - Verify all JSON files parse correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- colors.json contains 8 flat hex color definitions (no variants)
- color_labels.json has "zh-TW" key (not "chinese") for all colors
- ui_text.json uses "zh-TW" key throughout
- All 4 JSON validation tests pass

### Backend Layer

#### Task Group 2: Python Constants Update
**Dependencies:** Task Group 1

- [x] 2.0 Complete backend constants update
  - [x] 2.1 Write 4 focused tests for backend color constants
    - Test ColorToken enum has exactly 8 members matching new palette
    - Test COLORS dict loads all 8 colors with valid hex values
    - Test old tokens (CYAN, AMBER, MAGENTA) are not present in ColorToken
    - Test _load_colors_from_json correctly parses flat hex structure
  - [x] 2.2 Update ColorToken enum in `/home/user/projects/ColorFocus/backend/app/constants/colors.py`
    - Replace enum values: remove CYAN, AMBER, MAGENTA
    - Add enum values: BROWN, PINK, YELLOW
    - Final tokens: BLUE, ORANGE, PURPLE, BLACK, BROWN, PINK, YELLOW, GRAY
    - Update docstring to reflect new accessibility-optimized palette
  - [x] 2.3 Remove ColorVariant enum from colors.py
    - Delete ColorVariant class entirely (lines 47-60)
    - ColorVariant is no longer needed since colors.json uses flat structure
  - [x] 2.4 Update `_load_colors_from_json()` function
    - Change return type from `Dict[ColorToken, Dict[ColorVariant, str]]` to `Dict[ColorToken, str]`
    - Simplify parsing: `colors[token] = hex_value` instead of variant dict
    - Update COLORS type annotation to match new flat structure
  - [x] 2.5 Update module docstring and usage examples
    - Remove ColorVariant from import examples
    - Update usage example: `COLORS[ColorToken.BLUE]` returns `"#0066CC"` directly
    - Remove any references to dark/base/bright variants
  - [x] 2.6 Run backend color constants tests
    - Run ONLY the 4 tests written in 2.1
    - Verify ColorToken enum loads correctly
    - Verify COLORS dict contains all 8 colors
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- ColorToken enum has exactly 8 values matching new palette
- ColorVariant enum is completely removed
- COLORS dict returns flat hex strings (not variant dicts)
- All 4 backend tests pass

### Frontend Layer

#### Task Group 3: Frontend JavaScript Update
**Dependencies:** Task Group 1

- [x] 3.0 Complete frontend JavaScript updates
  - [x] 3.1 Write 4 focused tests for frontend color handling
    - Test ALL_COLOR_TOKENS array contains exactly 8 new color tokens
    - Test COLOR_SUBSETS maps correctly: 2->Black/Yellow, 4->Black/Blue/Orange/Yellow, 8->all
    - Test VALID_LANGUAGES contains 'zh-TW' (not 'chinese')
    - Test widthMultipliers object has 'zh-TW' key (not 'chinese')
  - [x] 3.2 Update ALL_COLOR_TOKENS array in `/home/user/projects/ColorFocus/frontend/puzzle.html`
    - Replace array content with new 8 colors in luminance order
    - New order: ['BLACK', 'BROWN', 'PURPLE', 'BLUE', 'GRAY', 'PINK', 'ORANGE', 'YELLOW']
    - Located around line 691
  - [x] 3.3 Update COLOR_SUBSETS object
    - Key 2: ['BLACK', 'YELLOW'] - maximum luminance contrast (Accessible tier)
    - Key 4: ['BLACK', 'BLUE', 'ORANGE', 'YELLOW'] - balanced (Standard tier)
    - Key 8: ALL_COLOR_TOKENS - full palette (Advanced tier)
    - Keep intermediate subsets (3, 5, 6, 7) for Custom mode using logical progressions
    - Located around lines 694-702
  - [x] 3.4 Update VALID_LANGUAGES array
    - Replace 'chinese' with 'zh-TW'
    - Final array: ['zh-TW', 'english', 'spanish', 'vietnamese']
    - Located around line 705
  - [x] 3.5 Update validateLanguage() function
    - Change default fallback from 'chinese' to 'zh-TW'
    - Located around line 747
  - [x] 3.6 Update widthMultipliers object in calculatePuzzleFontSize()
    - Rename 'chinese' key to 'zh-TW' with value 1.15 (unchanged)
    - Update 'vietnamese' to 2.4 (longest: "Vang" = 4 chars)
    - Update 'english' to 3.6 (longest: "Yellow" = 6 chars)
    - Update 'spanish' to 4.8 (longest: "Amarillo" = 8 chars)
    - Update comments to reflect new longest color words
    - Located around lines 1044-1049
  - [x] 3.7 Update language dropdown option value
    - Change option value from 'chinese' to 'zh-TW' in HTML select element
    - Ensure display text remains unchanged (Traditional Chinese indicator)
  - [x] 3.8 Update getLanguageDescriptor() function reference
    - Change key lookup from `language_descriptor_chinese` to `language_descriptor_zh-TW`
  - [x] 3.9 Update color access pattern for flat JSON structure
    - Change from `colorsJson[token].variants.base` to `colorsJson[token]`
    - Search for all instances accessing color hex values
    - Update any color rendering functions that used variant structure
  - [x] 3.10 Run frontend JavaScript tests
    - Run ONLY the 4 tests written in 3.1
    - Verify color arrays and language validation work correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- ALL_COLOR_TOKENS contains new 8-color palette
- COLOR_SUBSETS maps difficulty tiers correctly
- 'zh-TW' replaces 'chinese' throughout
- Font multipliers recalculated for new color names
- All 4 frontend tests pass

#### Task Group 4: CSS Border Styling
**Dependencies:** Task Group 3

- [x] 4.0 Complete CSS border styling updates
  - [x] 4.1 Write 3 focused tests for border styling
    - Test .puzzle-cell has 2px solid #1A1A1A border
    - Test .color-swatch (answer input) has 2px solid #1A1A1A border
    - Test .answer-key-item .color-swatch has 2px solid #1A1A1A border
  - [x] 4.2 Add border to .puzzle-cell CSS rule
    - Add: `border: 2px solid #1A1A1A;`
    - Border color matches Black token for consistency
    - Located in `<style>` section of puzzle.html
  - [x] 4.3 Add border to .color-swatch CSS rule
    - Add: `border: 2px solid #1A1A1A;`
    - Applies to answer input section swatches
  - [x] 4.4 Add border to answer key swatches
    - Add: `border: 2px solid #1A1A1A;` to `.answer-key-item .color-swatch` rule
    - Or create new rule if not existing
  - [x] 4.5 Verify touch target sizes remain adequate
    - Answer input buttons must maintain 44px minimum
    - Large grid cells (8x8) may be smaller - acceptable for display elements
    - Adjust padding if borders affect touch targets
  - [x] 4.6 Run CSS border styling tests
    - Run ONLY the 3 tests written in 4.1
    - Verify borders render on all colored elements
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- All puzzle cells have 2px dark border
- All color swatches have 2px dark border
- Answer key swatches have 2px dark border
- Touch targets remain 44px minimum on answer buttons
- All 3 CSS border tests pass

### Testing Layer

#### Task Group 5: Test Updates and Gap Analysis
**Dependencies:** Task Groups 1-4

- [x] 5.0 Update existing tests and fill critical gaps
  - [x] 5.1 Update existing test files for new color palette
    - Update `/home/user/projects/ColorFocus/tests/test_color_tokens.py` for new tokens
    - Update `/home/user/projects/ColorFocus/tests/test_python_color_constants.py` for flat structure
    - Update `/home/user/projects/ColorFocus/tests/test_puzzle_generator.py` color references
    - Update `/home/user/projects/ColorFocus/frontend/src/constants/colors.test.ts` for new colors
  - [x] 5.2 Update language-related tests for zh-TW
    - Update `/home/user/projects/ColorFocus/tests/test_ui_text.py` for zh-TW key
    - Update `/home/user/projects/ColorFocus/tests/test_ui_localization.py` for zh-TW
    - Replace any 'chinese' references with 'zh-TW'
  - [x] 5.3 Review tests from Task Groups 1-4
    - Review the 4 tests from JSON validation (Task 1.1)
    - Review the 4 tests from backend constants (Task 2.1)
    - Review the 4 tests from frontend JavaScript (Task 3.1)
    - Review the 3 tests from CSS borders (Task 4.1)
    - Total existing new tests: 15 tests
  - [x] 5.4 Analyze test coverage gaps for this feature
    - Identify critical workflows lacking coverage
    - Focus ONLY on accessible color palette feature
    - Prioritize end-to-end color rendering workflows
  - [x] 5.5 Write up to 8 additional strategic tests if needed
    - Test puzzle generation uses new color palette correctly
    - Test difficulty tier presets apply correct color subsets
    - Test language switching works with zh-TW
    - Test all 4 languages display correct color labels
    - Do NOT exceed 8 additional tests
    - Skip edge cases and performance tests
  - [x] 5.6 Run all feature-specific tests
    - Run all tests from Task Groups 1-4 (15 tests)
    - Run updated existing tests related to colors and languages
    - Run any new strategic tests from 5.5
    - Verify all critical workflows pass
    - Do NOT run unrelated application tests

**Acceptance Criteria:**
- All existing color-related tests updated for new palette
- All existing language tests updated for zh-TW key
- No more than 8 additional tests added for gap coverage
- All feature-specific tests pass (approximately 20-25 tests total)
- New accessible color palette works correctly across all languages

## Execution Order

Recommended implementation sequence:

1. **Shared Data Layer (Task Group 1)** - Foundation: JSON files are the source of truth
2. **Backend Layer (Task Group 2)** - Depends on colors.json structure change
3. **Frontend JavaScript (Task Group 3)** - Depends on all JSON files
4. **CSS Borders (Task Group 4)** - Can run parallel with late Task Group 3
5. **Test Updates (Task Group 5)** - Final verification after all changes

## Files to Modify

| File | Task Group | Changes |
|------|------------|---------|
| `/home/user/projects/ColorFocus/shared/colors.json` | 1 | Replace with flat 8-color palette |
| `/home/user/projects/ColorFocus/shared/color_labels.json` | 1 | New labels, zh-TW key |
| `/home/user/projects/ColorFocus/shared/ui_text.json` | 1 | Rename chinese to zh-TW |
| `/home/user/projects/ColorFocus/backend/app/constants/colors.py` | 2 | Update enum, remove variants |
| `/home/user/projects/ColorFocus/frontend/puzzle.html` | 3, 4 | JS constants, CSS borders |
| `/home/user/projects/ColorFocus/tests/test_color_tokens.py` | 5 | Update for new palette |
| `/home/user/projects/ColorFocus/tests/test_python_color_constants.py` | 5 | Update for flat structure |
| `/home/user/projects/ColorFocus/tests/test_ui_text.py` | 5 | Update for zh-TW |
| `/home/user/projects/ColorFocus/frontend/src/constants/colors.test.ts` | 5 | Update for new palette |

## Breaking Changes

- **localStorage "chinese" key**: Users with existing Chinese language preference will reset to default (zh-TW)
- **Color token removal**: CYAN, AMBER, MAGENTA no longer exist - any hardcoded references will break
- **Variant structure removal**: Code accessing `colors[token].variants.base` will break
- **Backend type signature**: COLORS dict returns `str` instead of `Dict[ColorVariant, str]`

## New Color Palette Reference

| Color | Hex | Luminance | Difficulty Tiers |
|-------|-----|-----------|------------------|
| BLACK | #1A1A1A | 10% | Accessible, Standard, Advanced |
| BROWN | #8B4513 | 28% | Advanced only |
| PURPLE | #7B4BAF | 35% | Advanced only |
| BLUE | #0066CC | 38% | Standard, Advanced |
| GRAY | #808080 | 50% | Advanced only |
| PINK | #E75480 | 52% | Advanced only |
| ORANGE | #FF8C00 | 62% | Standard, Advanced |
| YELLOW | #FFD700 | 84% | Accessible, Standard, Advanced |

## Language Labels Reference

| Color | English | zh-TW | Vietnamese | Spanish |
|-------|---------|-------|------------|---------|
| BLACK | Black | black | Den | Negro |
| BROWN | Brown | brown | Nau | Cafe |
| PURPLE | Purple | purple | Tim | Morado |
| BLUE | Blue | blue | Xanh | Azul |
| GRAY | Gray | gray | Xam | Gris |
| PINK | Pink | pink | Hong | Rosa |
| ORANGE | Orange | orange | Cam | Naranja |
| YELLOW | Yellow | yellow | Vang | Amarillo |
