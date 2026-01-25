# Plan: Enhanced Stroop Interference Messaging & Rehabilitation Guidance

## Spec Folder
`agent-os/specs/2026-01-25-stroop-guidance-messaging/`

## Goal
When Stroop interference is detected, provide educational explanations, evidence-based implications, and rehabilitation guidance to help users understand and improve.

---

## Task 1: Save Spec Documentation

Create `agent-os/specs/2026-01-25-stroop-guidance-messaging/` with:

- **plan.md** — This full plan
- **shape.md** — Shaping notes (scope, decisions, context)
- **standards.md** — Relevant standards (localization, single-file architecture, accessibility)
- **references.md** — Reference implementations (mistakeSummarySection, about modal)

## Task 2: Add UI Text Keys

**File:** `shared/ui_text.json`

Add 12 new localization keys with translations for zh-TW, english, spanish, vietnamese:

| Key | Purpose |
|-----|---------|
| `guidance_education_header` | "Understanding the Stroop Effect" |
| `guidance_education_text` | Explanation of word-color conflict |
| `guidance_pattern_header` | "What Your Results Suggest" |
| `guidance_pattern_high_stroop` | High interference feedback |
| `guidance_pattern_moderate_stroop` | Moderate feedback |
| `guidance_pattern_mixed_errors` | Mixed errors feedback |
| `guidance_pattern_non_stroop` | Non-Stroop feedback |
| `guidance_tips_header` | "Practice Tips" |
| `guidance_tips_high_stroop` | Tips for high Stroop influence |
| `guidance_tips_moderate_stroop` | Tips for moderate influence |
| `guidance_tips_mixed_errors` | Tips for mixed errors |
| `guidance_tips_non_stroop` | Tips for non-Stroop errors |

## Task 3: Add CSS for Guidance Section

**File:** `frontend/puzzle.html` (CSS section, after line ~936)

Add styles for `.stroop-guidance-section`:
- Collapsible subsection within summary panel
- Headers for education, pattern, tips
- Readable typography for elderly users
- Mobile responsive at 480px breakpoint

## Task 4: Add HTML Structure for Guidance Section

**File:** `frontend/puzzle.html` (HTML section, inside `mistakeSummarySection` after legend ~line 1854)

Add new div with:
- Education section (header + text)
- Pattern feedback section (header + dynamic text)
- Practice tips section (header + dynamic text)

## Task 5: Add JavaScript Functions

**File:** `frontend/puzzle.html` (JavaScript section, near displaySummary ~line 4242)

Add two new functions:

### `calculateStroopPattern(totalMistakes, stroopCount)`
Returns pattern category:
- `high_stroop` (≥70% Stroop-influenced)
- `moderate_stroop` (40-69%)
- `mixed_errors` (<40% but some)
- `non_stroop` (0% Stroop, or no mistakes)

### `displayStroopGuidance(totalMistakes, stroopCount)`
- Calls `calculateStroopPattern()`
- Shows/hides guidance section based on whether mistakes exist
- Populates education text (always shown if mistakes)
- Populates pattern-specific feedback
- Populates pattern-specific tips

## Task 6: Integrate with displaySummary()

**File:** `frontend/puzzle.html`

Modify `displaySummary()` to call `displayStroopGuidance(totalMistakes, stroopInfluencedCount)` before showing the summary panel.

## Task 7: Verify Implementation

1. Generate puzzle, make intentional Stroop mistakes
2. Check Answers → Identify Mistakes → Complete flow
3. Verify guidance section appears with correct content
4. Test all 4 languages (zh-TW, english, spanish, vietnamese)
5. Test edge cases: perfect score (guidance hidden), all non-Stroop errors
6. Run `uv run pytest -v` and `cd frontend && pnpm test`

---

## Key Messaging Content

### Education (shown to all users with mistakes)
> "When you see a color word printed in a different ink color, your brain must process two conflicting pieces of information at once: the meaning of the word and the color of the ink. This conflict is called Stroop interference, and it happens because reading is automatic—it takes extra mental effort to ignore the word and focus on the ink color."

### High Stroop Pattern Feedback
> "Most of your mistakes were influenced by the Stroop effect. This means the word meanings strongly interfered with your ability to identify the ink colors. This is completely normal—in fact, this is exactly what this exercise is designed to help train!"

### High Stroop Practice Tips
> "Start with fewer colors (3-4) and work your way up. Slow down—give your brain time to process the color, not the word. A few minutes of daily practice is more effective than one long session."

---

## Files to Modify

1. `shared/ui_text.json` — 12 new keys
2. `frontend/puzzle.html` — CSS, HTML, JS additions

## Standards Applied

- **localization/ui-text-structure** — snake_case keys, 4-language translations, {placeholder} syntax
- **frontend/single-file-architecture** — All changes in puzzle.html
- **accessibility/touch-and-fonts** — Readable fonts, elderly-friendly typography
