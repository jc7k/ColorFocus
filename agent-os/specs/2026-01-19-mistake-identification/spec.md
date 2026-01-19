# Specification: Mistake Identification

## Goal
Help users identify which specific tiles they misidentified during a Stroop puzzle, analyze whether Stroop interference contributed to errors, and present findings in a format useful for health professionals supporting cognitive rehabilitation.

## User Stories
- As a stroke recovery patient, I want to see which specific tiles I counted incorrectly so that I can understand my perception errors and track my cognitive progress
- As a health professional, I want to view a summary of my patient's mistake patterns and Stroop interference indicators so that I can assess their cognitive challenges and rehabilitation progress

## Specific Requirements

**Mistake Detection Trigger**
- Activate mistake identification flow only after user clicks "Check Answers" and has at least one incorrect color count
- Display a new "Identify Mistakes" button in the results section when discrepancies exist
- Store the discrepancy data (user count vs correct count per color) for use in the identification flow

**Guided Tile Selection Mode**
- Enter a special "identification mode" where user selects tiles they believed were a specific color
- Prompt user with one misidentified color at a time (e.g., "Select the tiles you thought were BLUE")
- Show color-specific prompt with color swatch and localized color label
- Allow user to select/deselect tiles using existing tile selection mechanism
- Provide "Done" button to confirm selections for current color before moving to next

**Mistake Visualization**
- After user confirms selections, mark tiles with visual indicators showing correct vs incorrect identifications
- Use distinct styling for: correctly identified tiles, incorrectly selected tiles (user thought it was this color but it wasn't)
- Display tile-level feedback using border colors or overlay icons that don't obscure the tile content
- Maintain accessibility with sufficient color contrast and non-color-only indicators (icons or patterns)

**Stroop Effect Analysis Algorithm**
- For each incorrectly selected tile, check if any orthogonally adjacent tile (up/down/left/right) has TEXT matching the color the user thought the tile was
- Flag tile as "Stroop-influenced" if neighboring tile's word text matches user's incorrect color perception
- Example: User thought tile was BLUE, but it was ORANGE; adjacent tile displays the word "BLUE" - flag as Stroop-influenced
- Store Stroop analysis results per tile for display and summary

**Stroop Influence Visualization**
- Add distinct visual indicator (e.g., subtle highlight or icon) to tiles flagged as Stroop-influenced
- Ensure Stroop indicator is visually distinct from correct/incorrect indicators
- Include legend explaining what the Stroop indicator means

**Summary Panel**
- Display summary after identification flow completes showing: total mistakes, Stroop-influenced count, non-Stroop mistakes
- Present data in clear, printable format suitable for sharing with health professionals
- Include puzzle metadata (seed, grid size, language, difficulty) for reproducibility
- Support multi-language display using existing UI text localization system

**Reset and Retry**
- Allow user to exit identification mode and return to normal puzzle view
- Provide option to clear identification results and start fresh
- Ensure new puzzle generation clears all identification state

## Existing Code to Leverage

**Tile Selection System (`selectedTiles` Set and `toggleTileSelection` function)**
- Reuse existing tile selection state management with `selectedTiles` Set
- Leverage `toggleTileSelection(index)` function for select/deselect behavior
- Use existing `.selected` CSS class and `aria-pressed` attribute pattern
- Extend `clearAllSelections()` function to also clear identification state

**Answer Checking Logic (`checkAnswers` function)**
- Reference `correctAnswers` object to get correct ink color counts per token
- Compare against user input values from answer input fields
- Extend results section to show "Identify Mistakes" button when errors detected

**Puzzle Data Structure (`currentPuzzle` array)**
- Access `currentPuzzle[index].word` to get the text displayed on each tile
- Access `currentPuzzle[index].inkColor` to get the actual ink color of each tile
- Use index-based grid position calculation: `row = Math.floor(index / currentGridSize)`, `col = index % currentGridSize`

**Color Constants and Labels**
- Use `colorsJson` for color hex values in visualizations
- Use `colorLabelsJson[token][currentLanguage]` for localized color names in prompts
- Use `activeColors` array to iterate only over colors in current puzzle

**UI Text Localization (`getUIText` function and `ui_text.json`)**
- Add new localization keys to `shared/ui_text.json` for all user-facing strings
- Use `getUIText(key)` pattern for retrieving localized strings
- Support all four languages: Chinese (zh-TW), English, Spanish, Vietnamese

## Out of Scope
- Automatic mistake correction or hints during puzzle solving (only post-check analysis)
- Detailed cognitive assessment scoring or clinical diagnostic features
- Export to PDF or external file formats (printable HTML view is sufficient)
- Historical tracking of mistakes across multiple puzzles (single-puzzle analysis only)
- Audio feedback for mistake identification
- Animation effects for tile marking (keep static for accessibility)
- Backend storage of identification results (client-side only for this spec)
- Integration with health professional accounts or patient management systems
- Color blindness simulation or alternate color schemes for mistake visualization
- Multi-user comparison or leaderboard features
