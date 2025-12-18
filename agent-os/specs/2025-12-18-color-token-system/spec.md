# Specification: Color Token System

## Goal
Implement the foundational color system for ColorFocus with 8 canonical color tokens, each having 3 brightness variants (24 total values), optimized for color-blind accessibility and shared between frontend and backend via a single source of truth.

## User Stories
- As a developer, I want a centralized color token system so that all UI components use consistent, accessible colors across the application.
- As a user with color blindness, I want colors that are distinguishable so that I can complete puzzles without confusion caused by my vision condition.

## Specific Requirements

**Single Source of Truth JSON File**
- Create `/shared/colors.json` as the authoritative color definition file
- Structure: object keyed by color token (BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY)
- Each token contains `variants` object with `dark`, `base`, and `bright` hex values
- BLACK token may omit `dark` variant (only `base` and `bright`) per PRD precedent
- File must be valid JSON and importable by both TypeScript and Python build processes

**Color-Blind-Safe Hex Value Selection**
- Select hex values distinguishable across deuteranopia, protanopia, and tritanopia
- Use PRD section 14 color values as starting reference (e.g., BLUE base: #2E86DE, ORANGE base: #E67E22)
- Validate selections against color-blind simulation tools before finalizing
- Prioritize luminance separation between colors to aid differentiation
- Ensure all colors meet WCAG AAA contrast ratio (7:1) against white background

**HSL-Based Brightness Variant Calculation**
- BASE hex is the reference point for each color token
- DARK variant: reduce HSL lightness by approximately 15-20% from BASE
- BRIGHT variant: increase HSL lightness by approximately 15-20% from BASE
- Hue must remain constant across all variants of a given token
- Document the HSL values alongside hex in the source JSON for reference

**TypeScript Constants Module**
- Create `/frontend/src/constants/colors.ts` that imports from shared JSON
- Export typed constants: `ColorToken` enum and `ColorVariant` type
- Export `COLORS` object providing programmatic access to all 24 hex values
- Type signature: `Record<ColorToken, Record<ColorVariant, string>>`
- Include JSDoc comments for IDE autocomplete support

**Python Constants Module**
- Create `/backend/app/constants/colors.py` that reads from shared JSON
- Define `ColorToken` and `ColorVariant` as string enums
- Export `COLORS` dictionary matching TypeScript structure
- Load JSON at module import time (not runtime file reads per request)
- Use Python 3.11+ StrEnum for type safety

**Tailwind CSS Configuration Extension**
- Extend `tailwind.config.js` theme.colors with all 24 color values
- Naming pattern: `{color}-{variant}` (e.g., `blue-base`, `orange-bright`, `purple-dark`)
- Generate config dynamically by importing the shared JSON during build
- Ensure CSS purging does not remove dynamically generated color classes

**Color Token Validation Tests**
- Write one test verifying TypeScript and Python constants match the source JSON
- Write one test verifying all 24 color values are valid hex format (#RRGGBB)
- Tests should fail build if source of truth drifts from generated constants

**Project Structure Setup**
- Create `/shared/` directory at project root for cross-platform constants
- Create `/frontend/src/constants/` directory for TypeScript constants
- Create `/backend/app/constants/` directory for Python constants
- Ensure build scripts can resolve the shared JSON path correctly

## Visual Design
No visual assets provided.

## Existing Code to Leverage

**PRD Color Token Registry (Section 14)**
- Contains validated hex values for BLUE, ORANGE, PURPLE, BLACK with all variants
- Use these exact values as the starting point for the 4 documented colors
- Extend the pattern to define CYAN, AMBER, MAGENTA, GRAY variants
- PRD structure can serve as template for the JSON schema

**PRD Section 5.2 Canonical Color Tokens Table**
- Provides base hex values for all 8 colors (BLUE: #2E86DE, ORANGE: #E67E22, etc.)
- Confirms the 8 required token names and their semantic meanings
- Use these base values and apply HSL lightness adjustments for dark/bright variants

## Out of Scope
- Chinese single-character labels (separate roadmap item, will be added in future spec)
- Visual testing utilities or color swatch preview components
- Color-blindness simulation preview mode for developers
- Gradient support for any color tokens
- Opacity/alpha variants of colors
- CSS custom properties (CSS variables) beyond Tailwind classes
- Animation or transition helpers for color changes
- Dark mode or alternative background color support
- Achromatopsia (complete color blindness) support
- Runtime brightness toggle UI (will be separate spec)
