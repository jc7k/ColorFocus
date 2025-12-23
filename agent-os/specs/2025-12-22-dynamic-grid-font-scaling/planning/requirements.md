# Spec Requirements: Dynamic Grid/Font Scaling

## Initial Description
Dynamic Grid and Font Scaling for ColorFocus Puzzle

As the grid size decreases from 8x8 down to 2x2, the puzzle blocks and fonts should scale up proportionally to fill the same available space. The scaling needs to be language-aware since different languages have different word lengths (Chinese characters vs English/Spanish/Vietnamese words). Words need to fit within blocks with appropriate margins for legibility.

This is for the ColorFocus Stroop puzzle app - a cognitive training tool for stroke patients and elderly users.

## Requirements Discussion

### First Round Questions

**Q1:** I assume the puzzle container's max-width (520px) should remain fixed, and we're scaling the cells and fonts within that fixed container space. Is that correct, or should the container itself also expand for smaller grids?
**Answer:** Container should scale to the canvas of the viewing device, but the cells and fonts within should scale according to the grids.

**Q2:** For the font scaling approach, I'm thinking we should either remove the maxFontSize caps entirely, or significantly raise them based on grid size. Which approach do you prefer, or do you have specific size targets in mind?
**Answer:** Max font sizes should be dynamic. Use Playwright to see what is the max for each language or calculate it on the fly. This will be language dependent.

**Q3:** For accessibility, should we establish minimum font sizes that must be maintained even for 8x8 grids? The current minimum is 6px on mobile and 10px on desktop - I assume these are acceptable floors?
**Answer:** They need to fit the cell. A minimum font size cannot be larger than the cell that it is within. Figure it out dynamically, or determine the minimum cell size and font size together.

**Q4:** The current word lengths vary significantly across languages. I assume we should maintain the current proportional relationship where Chinese can be ~3-4x larger than English/Spanish for the same cell. Is that correct?
**Answer:** Correct - maintain current proportional relationship where Chinese can be ~3-4x larger than English/Spanish.

**Q5:** Should there be a visual "margin" or padding within each cell that scales proportionally with the cell size, or should the text always occupy a consistent percentage of the cell width?
**Answer:** There should be a pleasing visual "margin". Follow best practices.

**Q6:** For mobile devices (under 480px viewport), should we apply the same scaling philosophy, or are there specific mobile considerations?
**Answer:** Correct, yes - apply the same scaling philosophy to mobile.

**Q7:** Is there anything specific that should be excluded from this work?
**Answer:** This should be only about the cells and the words within them. Leave the rest alone.

### Existing Code to Reference

No similar existing features identified for reference.

The current implementation in `/home/user/projects/ColorFocus/frontend/puzzle.html` contains:
- `calculatePuzzleFontSize()` function (lines 926-965) - current font sizing logic with fixed maxFontSizes
- `applyPuzzleFontSize()` function (lines 968-973) - applies calculated font size to cells
- `.puzzle-grid` CSS (lines 91-97) - current grid styling with max-width: 520px
- `.puzzle-cell` CSS (lines 98-112) - current cell styling with aspect-ratio: 1
- Language-specific width multipliers: Chinese (1.15), Vietnamese (2.6), English (4.2), Spanish (4.2)

### Follow-up Questions

**Follow-up 1:** Container scaling clarification - Should we remove max-width entirely, use percentage-based width, or keep a maximum on very large screens?
**Answer:** User requested a recommendation. They intuitively think it should not take up the whole viewport if the display is very large, but don't have specific guidance.

**Recommendation provided:** Maximum width of 800px on desktop/large screens. Rationale:
- 54% increase in puzzle area over current 520px
- Not so large that users on 4K monitors have overwhelming puzzles requiring excessive head/eye movement
- Maintains comfortable viewing distance for target demographic (older adults, post-stroke patients)
- Aligns with accessibility-focused design patterns
- On typical 1920px monitors, leaves generous side margins for focused, centered experience

**Follow-up 2:** Dynamic font sizing approach - Option A (runtime calculation), Option B (build-time with Playwright), or Option C (hybrid)?
**Answer:** Option A (runtime calculation) is fine - calculate optimal font size in JavaScript at runtime based on actual rendered cell dimensions and text content.

**Follow-up 3:** Visual margin percentage - target approximately 80% of cell width for text, leaving 10% margin on each side?
**Answer:** Yes, target approximately 80% of cell width for the text, leaving 10% margin on each side.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
N/A

## Requirements Summary

### Functional Requirements
- Container should scale to viewport width up to a recommended maximum of 800px on desktop
- Font sizes must be calculated dynamically at runtime based on actual rendered cell dimensions
- Text should occupy approximately 80% of cell width, leaving 10% margin on each side
- Maintain current proportional relationship between languages:
  - Chinese characters can be ~3-4x larger than English/Spanish for the same cell
  - Vietnamese falls between Chinese and English/Spanish
- Font sizing must work for all supported languages: Chinese, English, Spanish, Vietnamese
- Same scaling philosophy applies to both desktop and mobile viewports
- Font sizes should adapt dynamically - no hardcoded min/max that would prevent proper scaling

### Language-Specific Considerations
Current word lengths to accommodate:
- Chinese: 1 character per color (shortest)
- Vietnamese: 3-5 characters (XAM, DEN, DO, CAM, TIM, LAM, LUC, VANG)
- English: 3-7 characters (BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY)
- Spanish: 4-7 characters (AZUL, NARANJA, MORADO, NEGRO, CIAN, AMBAR, MAGENTA, GRIS)

### Reusability Opportunities
- The runtime font size calculation logic could potentially be extracted into a reusable utility function for future features requiring dynamic text sizing
- Current width multipliers (Chinese: 1.15, Vietnamese: 2.6, English: 4.2, Spanish: 4.2) may serve as starting points for the new calculation

### Scope Boundaries
**In Scope:**
- Puzzle grid container max-width adjustment (520px -> 800px recommended)
- Dynamic font size calculation based on cell dimensions
- Removing or replacing fixed maxFontSize caps
- Cell text margin/padding for 80% text width target
- All four supported languages (Chinese, English, Spanish, Vietnamese)
- All grid sizes (1x1 through 8x8)
- Desktop and mobile viewports
- The `.puzzle-grid` and `.puzzle-cell` CSS
- The `calculatePuzzleFontSize()` and `applyPuzzleFontSize()` JavaScript functions

**Out of Scope:**
- Print layout scaling
- Answer key section styling
- Answer input section styling
- Results section styling
- Control panel / header styling
- Task instructions section
- Any other UI elements outside the puzzle cells
- Adding new languages
- Changing the color tokens or color system

### Technical Considerations
- Implementation is in vanilla JavaScript within `/home/user/projects/ColorFocus/frontend/puzzle.html`
- Uses CSS Grid for puzzle layout with `grid-template-columns: repeat(N, 1fr)`
- Cells use `aspect-ratio: 1` to maintain square shape
- Current approach uses window resize listener to recalculate font sizes
- Browser text measurement APIs may be needed for accurate runtime calculation
- Must handle spacing settings (compact, normal, relaxed, spacious) which affect gap sizes
- Mobile breakpoint at 480px viewport width with additional breakpoint at 375px

### Approximate Cell Sizes with 800px Container
- 8x8 grid: ~100px cells
- 4x4 grid: ~200px cells
- 2x2 grid: ~400px cells
- 1x1 grid: ~800px cell (single cell fills container)
