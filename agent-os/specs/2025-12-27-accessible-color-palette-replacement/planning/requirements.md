# Spec Requirements: Accessible Color Palette Replacement

## Initial Description

Replace the current 8-color palette with a new accessibility-optimized color palette designed for color-blind users, elderly users, and stroke recovery patients. The new palette uses luminance-ordered colors to maximize distinguishability across various forms of color vision deficiency.

## Requirements Discussion

### First Round Questions

**Q1:** Should we use single hex values or retain the dark/base/bright variant system for the new colors?
**Answer:** Use single hex values only (no dark/base/bright variants). Use CSS for hover/focus effects if needed.

**Q2:** How should we handle borders on colored elements for contrast and accessibility?
**Answer:** Apply 2px dark border (#1A1A1A) to ALL colored elements for consistency: puzzle grid cells, color swatches in answer input section, and answer key swatches.

**Q3:** What are the acceptable minimum touch target sizes for interactive elements?
**Answer:** Accept smaller cells on large grids (8x8), but ensure answer input buttons meet 44px minimum.

**Q4:** Should we rename the "chinese" language key to a more specific locale code?
**Answer:** Rename "chinese" to "zh-TW" (breaking change for localStorage, but enables future simplified Chinese support).

**Q5:** How should difficulty tiers map to color subsets?
**Answer:** Use 3 tiers, skip 6-color subset:
- Accessible: 2 colors (Black, Yellow)
- Standard: 4 colors (Black, Blue, Orange, Yellow)
- Advanced: 8 colors (all)

**Q6:** What colors should be excluded and why?
**Answer:** Exclude Red (confuses with brown/orange for color-blind users), Green (Vietnamese "xanh" ambiguity + color blindness issues), Cyan/Teal (too similar to blue for elderly), and White (reserved for background).

**Q7:** Should font sizing multipliers be recalculated based on new color names?
**Answer:** Recalculate as needed based on new color names.

**Q8:** What features should remain unchanged?
**Answer:** Preserve seed-based deterministic generation, spacing options (compact/normal/relaxed/spacious), and all other features not discussed.

### Existing Code to Reference

**Similar Features Identified:**
- Feature: Current color system - Path: `/home/user/projects/ColorFocus/shared/colors.json`
- Feature: Current labels - Path: `/home/user/projects/ColorFocus/shared/color_labels.json`
- Feature: Backend constants - Path: `/home/user/projects/ColorFocus/backend/app/constants/colors.py`
- Feature: Frontend puzzle - Path: `/home/user/projects/ColorFocus/frontend/puzzle.html`

The existing color system structure should be referenced for understanding current implementation patterns, while simplifying from variant-based to single-hex-value approach.

### Follow-up Questions

No follow-up questions were required. All requirements were confirmed in the first round.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
N/A

## Requirements Summary

### Functional Requirements

#### New Color Palette (8 colors, luminance-ordered)
| Color  | Hex      | Luminance |
|--------|----------|-----------|
| Black  | #1A1A1A  | 10%       |
| Brown  | #8B4513  | 28%       |
| Purple | #7B4BAF  | 35%       |
| Blue   | #0066CC  | 38%       |
| Gray   | #808080  | 50%       |
| Pink   | #E75480  | 52%       |
| Orange | #FF8C00  | 62%       |
| Yellow | #FFD700  | 84%       |

#### Color Labels (4 languages)
| Color  | English | zh-TW | Vietnamese | Spanish  |
|--------|---------|-------|------------|----------|
| Black  | Black   | 黑    | Den        | Negro    |
| Brown  | Brown   | 棕    | Nau        | Cafe     |
| Purple | Purple  | 紫    | Tim        | Morado   |
| Blue   | Blue    | 藍    | Xanh       | Azul     |
| Gray   | Gray    | 灰    | Xam        | Gris     |
| Pink   | Pink    | 粉    | Hong       | Rosa     |
| Orange | Orange  | 橙    | Cam        | Naranja  |
| Yellow | Yellow  | 黃    | Vang       | Amarillo |

#### Difficulty Tier Color Subsets
- **Accessible (Tier 1):** 2 colors - Black, Yellow (maximum luminance contrast)
- **Standard (Tier 2):** 4 colors - Black, Blue, Orange, Yellow
- **Advanced (Tier 3):** 8 colors - All colors

#### UI Changes
- Apply 2px dark border (#1A1A1A) to all colored elements (grid cells, swatches, answer key)
- Answer input buttons must meet 44px minimum touch target
- Rename language key from "chinese" to "zh-TW" (breaking localStorage change)
- Recalculate font sizing multipliers based on new color word lengths

### Reusability Opportunities

- Existing JSON structure in `/shared/colors.json` can be simplified (remove variants object nesting)
- Existing label structure in `/shared/color_labels.json` can be updated in-place
- Backend ColorToken enum pattern in `/backend/app/constants/colors.py` remains valid
- Frontend COLOR_SUBSETS pattern in `/frontend/puzzle.html` can be updated with new tier mappings

### Scope Boundaries

**In Scope:**
- Replace all 8 color definitions with new accessible palette
- Update all 4 language labels for new colors
- Change difficulty tier color subsets (2/4/8 instead of current mapping)
- Add 2px borders to all colored UI elements
- Rename "chinese" to "zh-TW" throughout codebase
- Recalculate font sizing multipliers for new color names
- Update frontend COLOR_SUBSETS configuration

**Out of Scope:**
- Authentication or user accounts
- Progress tracking features
- Print/PDF functionality
- Adding new languages
- Adding new colors beyond the 8 defined
- Simplified Chinese (zh-CN) support (just preparing the key structure)
- Migration script for existing localStorage preferences

### Technical Considerations

#### Files to Update
1. `/home/user/projects/ColorFocus/shared/colors.json` - Remove variant structure, update to single hex values
2. `/home/user/projects/ColorFocus/shared/color_labels.json` - Update color names, rename "chinese" to "zh-TW"
3. `/home/user/projects/ColorFocus/backend/app/constants/colors.py` - Update ColorToken enum values
4. `/home/user/projects/ColorFocus/frontend/puzzle.html` - Update COLOR_SUBSETS, add borders, update font multipliers, change language key

#### Breaking Changes
- localStorage key "chinese" becomes "zh-TW" - existing users with Chinese preference will reset to default
- Color names change completely (e.g., CYAN, AMBER, MAGENTA removed; BROWN, PINK, YELLOW added)

#### Colors Explicitly Excluded (with rationale)
- **Red:** Confuses with brown/orange for color-blind users (deuteranopia, protanopia)
- **Green:** Vietnamese "xanh" ambiguity (means both blue and green) + color blindness issues
- **Cyan/Teal:** Too similar to blue for elderly users with reduced color discrimination
- **White:** Reserved for background to ensure contrast

#### Alignment with Product Mission
This change directly supports the product mission of accessibility-first design for older adults and post-stroke patients by:
- Using luminance-ordered colors that remain distinguishable even with reduced color vision
- Avoiding colors that cause confusion for common forms of color blindness
- Adding borders to improve element distinction for users with visual impairments
- Preparing locale infrastructure (zh-TW) for future internationalization
