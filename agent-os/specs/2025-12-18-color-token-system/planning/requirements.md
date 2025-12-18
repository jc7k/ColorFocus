# Spec Requirements: Color Token System

## Initial Description

Implement the 8 canonical color tokens (BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY) with DARK, BASE, and BRIGHT variants (24 total color values), ensuring all colors are distinguishable for common forms of color blindness. This is the foundational color system for the entire ColorFocus puzzle application.

## Requirements Discussion

### First Round Questions

**Q1:** I assume each color token will have exactly 3 brightness variants (DARK, BASE, BRIGHT) using HSL adjustments where BASE is the reference point, DARK has lower lightness, and BRIGHT has higher lightness. Is that correct, or would you prefer a different approach to generating variants (e.g., saturation shifts, or manually curated values for each variant)?
**Answer:** Yes to defaults - HSL brightness variant approach is acceptable.

**Q2:** For the color-blind accessibility requirement, I'm planning to ensure the 8 base colors are distinguishable across deuteranopia (red-green, most common), protanopia (red-green), and tritanopia (blue-yellow). Should we also consider achromatopsia (complete color blindness), or are the three common types sufficient? Also, are you aware of any specific color palette research or references we should use as a starting point?
**Answer:** Yes to defaults - Support deuteranopia, protanopia, and tritanopia. Research and select appropriate color-blind-safe hex values.

**Q3:** I assume the color tokens will be implemented as TypeScript constants in the frontend AND Python constants in the backend (as noted in the tech stack), with the hex/HSL values defined once and shared or synchronized between both. Should we prioritize a single source of truth (e.g., JSON file that both systems read), or are duplicated definitions acceptable with tests to ensure they match?
**Answer:** Yes to defaults - Use a single source of truth approach to prevent drift between frontend and backend.

**Q4:** Regarding Tailwind CSS integration, I assume we'll extend the Tailwind config to add custom color classes for all 24 color values (e.g., `text-blue-base`, `bg-orange-bright`, etc.). Is that the naming convention you'd prefer, or should we use a different pattern?
**Answer:** Yes to defaults - Use the proposed naming convention pattern.

**Q5:** The Chinese single-character labels are mentioned as a separate roadmap item (Item 8). Should the Color Token System include placeholders or data structures for these labels now, or should we keep this spec focused purely on colors and add labels later?
**Answer:** Not explicitly answered - assume focus purely on colors; Chinese labels will be added in separate spec (roadmap item 8).

**Q6:** For puzzle rendering, should the colors work on both light and dark backgrounds, or will puzzles always be displayed on a consistent background color (e.g., white/off-white)? This affects whether we need to validate contrast for multiple background scenarios.
**Answer:** Not explicitly answered - assume consistent light/white background based on accessibility-first design for older adults (product mission).

**Q7:** Should this spec include any visual testing utilities, such as a color swatch preview component that shows all 24 colors side-by-side, or a simulated color-blindness preview mode for developers? Or should those be separate specs?
**Answer:** Keep implementation minimal - no visual testing utilities in this spec.

**Q8:** Is there anything specific you want to EXCLUDE from this color token system? For example: gradient support, opacity variants, CSS custom properties (CSS variables), or animation/transition helpers?
**Answer:** Not explicitly answered - assume minimal implementation excludes these advanced features.

### Existing Code to Reference

No similar existing features identified for reference. This is a new project with no prior codebase.

### Follow-up Questions

**Follow-up 1:** For the 8 colors (BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY), should I proceed with researching and selecting color-blind-safe hex values that work for deuteranopia, protanopia, and tritanopia? Or do you have specific hex values already in mind that you'd like to use as starting points?
**Answer:** Yes to defaults - Research and select color-blind-safe hex values.

**Follow-up 2:** For sharing color definitions between frontend (TypeScript) and backend (Python), I'm assuming we should use a single source of truth approach (e.g., a JSON file or generated constants) to prevent drift. Is that acceptable, or would you prefer simpler duplicated definitions with validation tests?
**Answer:** Yes to defaults - Use single source of truth approach.

**Follow-up 3:** Should this initial color token system be minimal (just the 24 color values with their hex codes and Tailwind integration), or should it also include the visual testing utilities I mentioned (color swatch preview component, simulated color-blindness preview)?
**Answer:** Keep it minimal - just the 24 color values with hex codes and Tailwind integration.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
N/A - No visual references available.

## Requirements Summary

### Functional Requirements
- Define 8 canonical color tokens: BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY
- Each color token has 3 brightness variants: DARK, BASE, BRIGHT (24 total color values)
- All 8 base colors must be visually distinguishable for users with:
  - Deuteranopia (red-green color blindness, most common)
  - Protanopia (red-green color blindness)
  - Tritanopia (blue-yellow color blindness)
- Brightness variants generated using HSL lightness adjustments from BASE value
- Color values defined as a single source of truth (e.g., JSON file) consumed by both frontend and backend
- Tailwind CSS extended with custom color classes following pattern: `{property}-{color}-{variant}` (e.g., `text-blue-base`, `bg-orange-bright`)
- TypeScript constants generated/imported from source of truth for frontend use
- Python constants generated/imported from source of truth for backend use

### Reusability Opportunities
- No existing code to reference (new project)
- This color token system will be the foundation referenced by all future specs involving color display
- Pattern established here for single source of truth should inform future shared constants

### Scope Boundaries

**In Scope:**
- 8 color tokens with 3 variants each (24 total hex values)
- Color-blind-safe color selection research and implementation
- Single source of truth file (JSON or similar)
- Tailwind CSS configuration extension
- TypeScript type definitions and constants
- Python constants module
- HSL-based brightness variant calculation

**Out of Scope:**
- Chinese single-character labels (separate roadmap item 8)
- Visual testing utilities (color swatch preview, color-blindness simulation)
- Gradient support
- Opacity variants
- CSS custom properties / CSS variables
- Animation/transition helpers
- Dark mode / multiple background support
- Achromatopsia (complete color blindness) support

### Technical Considerations
- Frontend: React 18+ with TypeScript, Tailwind CSS
- Backend: FastAPI with Python 3.11+, use `uv` for dependency management
- Color values should be defined in HSL for easier variant calculation, with hex equivalents for implementation
- Tailwind config extends theme.colors with custom color tokens
- Must align with WCAG contrast requirements (product targets WCAG AAA)
- Colors will be used on light/white backgrounds (consistent with accessibility-first design for older adults)
- No information conveyed by color alone - text labels always present (per product tech stack)
