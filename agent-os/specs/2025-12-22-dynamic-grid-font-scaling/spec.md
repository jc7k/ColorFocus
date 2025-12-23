# Specification: Dynamic Grid/Font Scaling

## Goal
Enable puzzle cells and fonts to scale dynamically based on grid size and language, ensuring text fills approximately 80% of cell width while maintaining legibility for stroke patients and elderly users doing cognitive training.

## User Stories
- As a stroke patient, I want larger puzzle cells and fonts for smaller grids so that I can easily read and interact with the cognitive training exercise.
- As an elderly user using different languages, I want the font size to automatically adjust based on word length so that all color words remain readable regardless of my language preference.

## Specific Requirements

**Container Width Scaling**
- Change max-width from current 520px to 800px for the `.puzzle-grid` container
- Container should fill available viewport width up to the 800px maximum
- Maintains centered layout with comfortable side margins on large monitors
- Mobile devices (under 480px) continue to use 100% width minus padding
- This provides 54% more puzzle area while keeping comfortable viewing for target demographic

**Runtime Font Size Calculation**
- Replace current fixed maxFontSize caps with dynamic calculation at runtime
- Calculate font size based on actual rendered cell width from the DOM
- Use formula: baseFontSize = (cellWidth * 0.8) / languageWidthMultiplier
- Recalculate on window resize, grid size change, spacing change, and language change
- No hardcoded min/max font sizes that would prevent proper scaling

**80% Text Width with 10% Margins**
- Text should occupy approximately 80% of each cell's width
- 10% visual margin on left and right sides within the cell
- Achieve via font sizing calculation, not CSS padding
- Provides consistent visual breathing room across all grid sizes

**Language-Specific Proportional Scaling**
- Maintain current proportional relationship: Chinese can be 3-4x larger than English/Spanish
- Current width multipliers to use as starting points:
  - Chinese: 1.15 (single character per color)
  - Vietnamese: 2.6 (3-5 characters: XAM, DEN, DO, CAM, TIM, LAM, LUC, VANG)
  - English: 4.2 (3-7 characters: BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY)
  - Spanish: 4.2 (4-7 characters: AZUL, NARANJA, MORADO, NEGRO, CIAN, AMBAR, MAGENTA, GRIS)
- Same scaling philosophy applies to both desktop and mobile

**Spacing Setting Integration**
- Account for gap sizes when calculating available cell width
- SPACING_VALUES: compact (1px), normal (2px), relaxed (6px), spacious (12px)
- Formula must subtract total gap width from container width before dividing by columns

**Grid Size Responsiveness**
- Support all grid sizes from 1x1 through 8x8
- Approximate cell sizes at 800px container: 8x8 (~100px), 4x4 (~200px), 2x2 (~400px), 1x1 (~800px)
- Font sizes should scale proportionally with cell sizes
- Smaller grids yield larger cells and correspondingly larger fonts

**Mobile Viewport Handling**
- Apply same scaling philosophy on mobile (under 480px viewport)
- Account for mobile-specific gap of 1px and cell padding of 0.1rem
- Recalculate font size on orientation changes

## Visual Design

No visual assets provided.

## Existing Code to Leverage

**`calculatePuzzleFontSize()` function (lines 926-965)**
- Current font sizing logic in `/home/user/projects/ColorFocus/frontend/puzzle.html`
- Contains language width multipliers (chinese: 1.15, vietnamese: 2.6, english: 4.2, spanish: 4.2)
- Has cell width calculation logic that accounts for gaps
- Replace the fixed maxFontSizes object with dynamic calculation
- Keep the resize event listener pattern for recalculation triggers

**`applyPuzzleFontSize()` function (lines 968-973)**
- Applies calculated font size to all `.puzzle-cell` elements
- Can be reused as-is, just receives new calculated values

**`.puzzle-grid` CSS (lines 91-97)**
- Current grid styling with max-width: 520px to update to 800px
- Uses CSS Grid with `grid-template-columns: repeat(N, 1fr)`
- Gap is set dynamically via JavaScript in `updateGridCSS()`

**`.puzzle-cell` CSS (lines 98-112)**
- Uses `aspect-ratio: 1` to maintain square cells
- Uses flexbox for centering text within cells
- Mobile overrides at line 400-408 reduce border-radius and add overflow handling

**SPACING_VALUES constant (lines 646-651)**
- Defines gap values in pixels for each spacing option
- Must be factored into cell width calculation for accurate font sizing

## Out of Scope
- Print layout scaling
- Answer key section styling
- Answer input section styling
- Results section styling
- Control panel and header styling
- Task instructions section styling
- Any UI elements outside the puzzle cells (metadata, buttons, dropdowns)
- Adding new languages beyond the four currently supported
- Changing color tokens or the color system
- Hover effects on puzzle cells
- Browser text measurement APIs for exact glyph width detection
