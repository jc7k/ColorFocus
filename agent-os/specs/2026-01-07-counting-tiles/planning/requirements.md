# Spec Requirements: Counting Tiles (Interactive Tile Selection)

## Initial Description
A UX enhancement feature to help users (elderly or stroke patients) count how many tiles on the existing game board have a particular ink color. This is NOT a new game mode but a convenience feature added to the existing Stroop puzzle interface.

## Requirements Discussion

### First Round Questions

**Q1:** Is this a new game mode or an enhancement to the existing puzzle?
**Answer:** This is NOT a new game but rather a convenience feature for their ICP (elderly or stroke patients) to help them count how many tiles on the existing game board have a particular color.

**Q2:** How should tile selection work?
**Answer:** Yes to interactive counting, but:
- NOT checkmarks - show the tile as "pressed down" (visual depression state)
- Should toggle back to unselected if clicked/tapped a second time
- When user taps a color in the answer section (where they report count per color), the number of selected tiles should be counted and auto-filled into that color's count field
- There should be a button to unselect all tiles

### Existing Code to Reference
No similar existing features identified for reference.

### Follow-up Questions

**Follow-up 1:** For the auto-fill behavior: when user taps a color swatch to fill in the count, should we (a) count ALL selected tiles regardless of their actual ink color, or (b) only count selected tiles that match that specific color? Option (a) puts the onus on the user to select correctly; option (b) provides automatic color matching.
**Answer:** Count ALL selected tiles. Whether or not selected tiles match the color swatch is for the user to solve - we just count.

**Follow-up 2:** When the count is auto-filled, should there be any validation feedback? For example: (a) simply fill in the count with no judgment, (b) show a subtle indicator if the count seems incorrect, or (c) highlight tiles that don't match the expected color?
**Answer:** Option (a) - Simply fill in the count with no judgment. Let "Check Answers" reveal errors later.

**Follow-up 3:** Should tile selections persist when generating a new puzzle, or should they auto-clear?
**Answer:** Yes, selections should auto-clear when generating a new puzzle.

**Follow-up 4:** For mobile touch targets: should selected tiles have (a) a subtle inset effect, (b) a more pronounced "pressed in" shadow, or (c) a border/outline change? Considering elderly users with potential motor control challenges, we want to balance visual clarity with not being too jarring.
**Answer:** Inset that is visible (more pronounced than subtle).

**Follow-up 5:** Should keyboard navigation be supported for tile selection (e.g., arrow keys to move between tiles, spacebar to toggle selection)?
**Answer:** Yes, support keyboard navigation (arrow keys + spacebar).

**Follow-up 6:** Are there any features you specifically want to EXCLUDE from this enhancement?
**Answer:**
- CAN have a pleasant sound effect, but it must be a setting that can be turned off
- NO count badge showing "X selected" on tiles
- NO undo/redo for individual tile selections

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
N/A

## Requirements Summary

### Functional Requirements
- Tiles can be tapped/clicked to show a "pressed down" visual state (pronounced inset effect)
- Tiles toggle between selected and unselected on repeated taps/clicks
- Tapping a color swatch in the answer section auto-fills the count of ALL currently selected tiles
- No validation or judgment at auto-fill time - "Check Answers" handles validation later
- A "Clear All Selections" button to unselect all tiles at once
- Tile selections auto-clear when generating a new puzzle
- Optional sound effect on tile selection (with setting to disable)
- Keyboard navigation support: arrow keys to move between tiles, spacebar to toggle selection
- This is an enhancement to the existing puzzle UI, not a separate mode

### Reusability Opportunities
- Existing tile hover effects in puzzle.html can inform the selected state styling
- Existing "Check Answers" validation logic remains unchanged
- Existing puzzle generation flow needs hook to clear selections

### Scope Boundaries
**In Scope:**
- Interactive tile selection with visible inset/depression feedback
- Auto-fill count functionality when tapping answer color swatches (counts ALL selected tiles)
- "Clear All Selections" button
- Auto-clear selections on new puzzle generation
- Keyboard navigation (arrow keys + spacebar)
- Optional sound effect with toggle setting

**Out of Scope:**
- Count badge showing "X selected" on tiles
- Undo/redo for individual tile selections
- Color matching validation at selection time
- Smart counting that only counts tiles matching the target color
- Any changes to the existing "Check Answers" validation flow

### Technical Considerations
- Must integrate with existing puzzle.html single-file architecture
- Must work alongside existing tile hover effects
- Must be mobile-friendly with appropriately sized touch targets for elderly users
- Should use CSS for depression/inset effect (box-shadow inset, transform, etc.)
- Keyboard focus states must be clearly visible for accessibility
- Sound effect requires user preference storage (likely LocalStorage, consistent with existing preferences)
- Selection state should be managed in JavaScript (likely a Set or array of selected tile indices)
