# Specification: Accessible Color Palette Replacement

## Goal

Replace the current 8-color palette with a luminance-ordered, accessibility-optimized palette designed for users with color vision deficiencies, elderly users, and stroke recovery patients, while simplifying the color data structure from variants to single hex values.

## User Stories

- As a color-blind user, I want colors that remain distinguishable so that I can complete the Stroop test without confusion caused by similar-looking colors
- As an elderly user with reduced color discrimination, I want high-contrast borders on colored elements so that I can clearly see the boundaries between puzzle cells

## Specific Requirements

**New 8-Color Palette Definition**
- Replace existing colors with luminance-ordered palette: Black (#1A1A1A, 10%), Brown (#8B4513, 28%), Purple (#7B4BAF, 35%), Blue (#0066CC, 38%), Gray (#808080, 50%), Pink (#E75480, 52%), Orange (#FF8C00, 62%), Yellow (#FFD700, 84%)
- Explicitly excluded colors: Red (color-blind confusion), Green (Vietnamese "xanh" ambiguity + color blindness), Cyan/Teal (too similar to blue for elderly), White (reserved for background)
- Store as flat hex values, removing the `variants` object nesting from `colors.json`
- Backend ColorToken enum must be updated to match new color names (remove CYAN, AMBER, MAGENTA; add BROWN, PINK, YELLOW)

**Difficulty Tier Color Subsets**
- Accessible tier: 2 colors (Black, Yellow) - maximum luminance contrast for easiest discrimination
- Standard tier: 4 colors (Black, Blue, Orange, Yellow) - balanced difficulty with high distinguishability
- Advanced tier: 8 colors (all) - full palette for maximum cognitive challenge
- Remove intermediate 3, 5, 6, 7 color subsets from difficulty presets (keep available in Custom mode)

**Multi-Language Color Labels**
- Update labels for all 4 languages to match new colors: Black (Black/Den/Negro), Brown (Brown/Nau/Cafe), Purple (Purple/Tim/Morado), Blue (Blue/Xanh/Azul), Gray (Gray/Xam/Gris), Pink (Pink/Hong/Rosa), Orange (Orange/Cam/Naranja), Yellow (Yellow/Vang/Amarillo)
- zh-TW labels: Black=黑, Brown=棕, Purple=紫, Blue=藍, Gray=灰, Pink=粉, Orange=橙, Yellow=黃
- Vietnamese labels should use ASCII-friendly versions without diacritics for display compatibility

**Language Key Rename**
- Rename "chinese" to "zh-TW" in `color_labels.json` and `ui_text.json`
- Update `VALID_LANGUAGES` array in frontend from 'chinese' to 'zh-TW'
- Update language dropdown option value from 'chinese' to 'zh-TW'
- Update localStorage key fallback logic (users with old "chinese" preference will reset to default)
- Update `getLanguageDescriptor()` function key from `language_descriptor_chinese` to `language_descriptor_zh-TW`

**Dark Border on Colored Elements**
- Apply 2px solid border (#1A1A1A) to all puzzle grid cells via `.puzzle-cell` CSS
- Apply same 2px border to color swatches in answer input section via `.color-swatch` CSS
- Apply same 2px border to answer key swatches via `.answer-key-item .color-swatch` CSS
- Border color matches Black color value for consistency

**Touch Target Sizing**
- Answer input buttons must meet 44px minimum touch target (already satisfied by current design)
- Puzzle grid cells on large grids (8x8) may be smaller than 44px - this is acceptable for display elements
- Ensure interactive elements in mobile view maintain adequate touch targets

**Font Sizing Multiplier Recalculation**
- Recalculate `widthMultipliers` object based on new longest color words per language
- zh-TW: 1.15 (single character, unchanged)
- Vietnamese: longest word is "Vang" (4 chars) - approximately 2.4 multiplier
- English: longest word is "Yellow" (6 chars) - approximately 3.6 multiplier
- Spanish: longest word is "Amarillo" (8 chars) - approximately 4.8 multiplier

**JSON Structure Simplification**
- Change `colors.json` from nested `{ "COLOR": { "variants": { "base": "#hex" } } }` to flat `{ "COLOR": "#hex" }`
- Update frontend code to access colors directly (e.g., `colorsJson[token]` instead of `colorsJson[token].variants.base`)
- Update backend `_load_colors_from_json()` function to parse flat structure instead of variant structure
- Remove `ColorVariant` enum from backend as it is no longer needed

## Existing Code to Leverage

**`/home/user/projects/ColorFocus/shared/colors.json`**
- Current structure defines 8 colors with variant objects
- Simplify to flat hex values, keeping same color token keys pattern
- New tokens: BLACK, BROWN, PURPLE, BLUE, GRAY, PINK, ORANGE, YELLOW

**`/home/user/projects/ColorFocus/shared/color_labels.json`**
- Existing 4-language label structure per color can be updated in-place
- Change "chinese" key to "zh-TW" in each color object
- Replace color-specific labels with new color names

**`/home/user/projects/ColorFocus/frontend/puzzle.html` COLOR_SUBSETS pattern**
- Lines 694-702 define COLOR_SUBSETS object mapping count to color array
- Update with new color tokens and tier mappings
- DIFFICULTY_PRESETS at lines 717-721 already use colorCount field - update values

**`/home/user/projects/ColorFocus/backend/app/constants/colors.py` ColorToken enum**
- Lines 29-44 define ColorToken StrEnum with 8 values
- Replace token values with new palette (remove CYAN, AMBER, MAGENTA; add BROWN, PINK, YELLOW)
- Remove ColorVariant enum entirely (lines 47-60) as variants are eliminated

**`/home/user/projects/ColorFocus/shared/ui_text.json` language keys**
- Lines with "chinese" key need renaming to "zh-TW" throughout
- language_descriptor keys need updating for new language code

## Out of Scope

- Migration script for users with existing localStorage preferences (users will reset to defaults)
- Adding new languages beyond the current 4 (English, zh-TW, Vietnamese, Spanish)
- Adding new colors beyond the 8 defined in the palette
- Simplified Chinese (zh-CN) support (only preparing key structure with zh-TW naming)
- Changes to seed-based deterministic puzzle generation algorithm (mulberry32 PRNG)
- Changes to spacing options (compact/normal/relaxed/spacious values)
- Changes to grid size options (1x1 through 8x8)
- Changes to congruence percentage controls
- User authentication or accounts
- Progress tracking features
- Print/PDF export functionality
