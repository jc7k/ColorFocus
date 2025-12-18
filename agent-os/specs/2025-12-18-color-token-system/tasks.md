# Task Breakdown: Color Token System

## Overview
Total Tasks: 4 Task Groups with 19 Sub-tasks

This spec implements the foundational color system for ColorFocus with 8 canonical color tokens (BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY), each having 3 brightness variants (24 total values), optimized for color-blind accessibility and shared between frontend and backend via a single source of truth.

## Task List

### Shared Constants Layer

#### Task Group 1: Color Token Source of Truth
**Dependencies:** None

- [x] 1.0 Complete shared color token definitions
  - [x] 1.1 Write 3-4 focused tests for color token validation
    - Test that colors.json is valid JSON and has correct structure
    - Test that all 24 color values are valid hex format (#RRGGBB)
    - Test that all 8 color tokens have required variants (dark, base, bright; BLACK may omit dark)
    - Test that hex values meet minimum luminance separation thresholds
  - [x] 1.2 Create project directory structure
    - Create `/shared/` directory at project root for cross-platform constants
    - Create `/frontend/src/constants/` directory for TypeScript constants
    - Create `/backend/app/constants/` directory for Python constants
  - [x] 1.3 Research and select color-blind-safe hex values
    - Use PRD Section 5.2 and Section 14 as starting reference for base values
    - Validate hex values are distinguishable across deuteranopia, protanopia, and tritanopia
    - Ensure all colors meet WCAG AAA contrast ratio (7:1) against white background
    - Prioritize luminance separation between colors to aid differentiation
    - Document research findings and validation methodology
  - [x] 1.4 Calculate HSL-based brightness variants
    - Convert base hex values to HSL format
    - Calculate DARK variant: reduce lightness by 15-20% from BASE
    - Calculate BRIGHT variant: increase lightness by 15-20% from BASE
    - Ensure hue remains constant across all variants of each token
    - Document HSL values alongside hex for reference
  - [x] 1.5 Create `/shared/colors.json` source of truth file
    - Structure: object keyed by color token (BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY)
    - Each token contains `variants` object with `dark`, `base`, and `bright` hex values
    - BLACK token may omit `dark` variant (only `base` and `bright`) per PRD precedent
    - Include HSL reference values as comments or metadata
    - Ensure file is valid JSON importable by both TypeScript and Python
  - [x] 1.6 Ensure color token tests pass
    - Run ONLY the 3-4 tests written in 1.1
    - Verify JSON structure is valid
    - Verify all hex values are properly formatted
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 3-4 tests written in 1.1 pass
- `/shared/colors.json` contains all 8 color tokens with 24 total hex values (23 if BLACK omits dark)
- All hex values validated for color-blind accessibility
- All colors meet WCAG AAA contrast requirements
- File is valid JSON and follows documented structure

### Frontend Constants Layer

#### Task Group 2: TypeScript Constants Module
**Dependencies:** Task Group 1

- [x] 2.0 Complete TypeScript color constants
  - [x] 2.1 Write 2-3 focused tests for TypeScript constants
    - Test that TypeScript COLORS object matches source JSON structure
    - Test that ColorToken enum contains all 8 token names
    - Test that ColorVariant type accepts only valid variant names
  - [x] 2.2 Create `/frontend/src/constants/colors.ts` module
    - Import from shared JSON (configure build to resolve path)
    - Export `ColorToken` enum: BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY
    - Export `ColorVariant` type: 'dark' | 'base' | 'bright'
    - Export `COLORS` object: `Record<ColorToken, Record<ColorVariant, string>>`
    - Include JSDoc comments for IDE autocomplete support
  - [x] 2.3 Extend Tailwind CSS configuration
    - Extend `tailwind.config.js` theme.colors with all 24 color values
    - Naming pattern: `{color}-{variant}` (e.g., `blue-base`, `orange-bright`, `purple-dark`)
    - Import shared JSON dynamically during build
    - Configure safelist or content patterns to prevent CSS purging of color classes
  - [x] 2.4 Ensure TypeScript constants tests pass
    - Run ONLY the 2-3 tests written in 2.1
    - Verify constants match source JSON
    - Verify Tailwind config generates expected color classes
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-3 tests written in 2.1 pass
- TypeScript constants correctly typed and exported
- Tailwind CSS extended with all 24 color utility classes
- Color classes available for use in components (e.g., `text-blue-base`, `bg-orange-bright`)
- JSDoc comments provide IDE autocomplete hints

### Backend Constants Layer

#### Task Group 3: Python Constants Module
**Dependencies:** Task Group 1

- [x] 3.0 Complete Python color constants
  - [x] 3.1 Write 2-3 focused tests for Python constants
    - Test that Python COLORS dictionary matches source JSON structure
    - Test that ColorToken StrEnum contains all 8 token names
    - Test that ColorVariant StrEnum contains all 3 variant names
  - [x] 3.2 Create `/backend/app/constants/colors.py` module
    - Define `ColorToken` as Python 3.11+ StrEnum with all 8 tokens
    - Define `ColorVariant` as StrEnum with: DARK, BASE, BRIGHT
    - Load shared JSON at module import time (not runtime file reads per request)
    - Export `COLORS` dictionary matching TypeScript structure
    - Use `uv` for any dependency management if needed
  - [x] 3.3 Configure JSON path resolution for backend
    - Ensure backend build/import can resolve `/shared/colors.json` path
    - Add necessary path configuration to pyproject.toml if needed
    - Document path resolution approach for future maintainers
  - [x] 3.4 Ensure Python constants tests pass
    - Run ONLY the 2-3 tests written in 3.1
    - Use `uv run pytest` to execute tests
    - Verify constants match source JSON
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-3 tests written in 3.1 pass
- Python StrEnums correctly defined for ColorToken and ColorVariant
- COLORS dictionary structure matches TypeScript equivalent
- JSON loaded at import time, not per-request
- Path resolution documented and working

### Testing Layer

#### Task Group 4: Cross-Platform Validation and Test Review
**Dependencies:** Task Groups 1-3

- [x] 4.0 Review existing tests and validate cross-platform consistency
  - [x] 4.1 Review tests from Task Groups 1-3
    - Review the 3-4 tests written for shared constants (Task 1.1)
    - Review the 2-3 tests written for TypeScript constants (Task 2.1)
    - Review the 2-3 tests written for Python constants (Task 3.1)
    - Total existing tests: approximately 7-10 tests
  - [x] 4.2 Write cross-platform synchronization test
    - Add 1-2 tests verifying TypeScript and Python constants both match the source JSON
    - Test should fail build if source of truth drifts from either platform's constants
    - Focus on critical synchronization, not exhaustive property comparison
  - [x] 4.3 Run all feature-specific tests
    - Run ONLY tests related to Color Token System (tests from 1.1, 2.1, 3.1, and 4.2)
    - Expected total: approximately 8-12 tests
    - Verify cross-platform consistency
    - Do NOT run the entire application test suite
    - Verify all critical workflows pass

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 8-12 tests total)
- TypeScript and Python constants verified to match source JSON
- Build will fail if constants drift from source of truth
- Cross-platform synchronization confirmed working

## Execution Order

Recommended implementation sequence:
1. **Shared Constants Layer** (Task Group 1) - Foundation: Create directory structure, research colors, define source of truth JSON
2. **Frontend Constants Layer** (Task Group 2) - Can start immediately after Task Group 1: TypeScript constants and Tailwind integration
3. **Backend Constants Layer** (Task Group 3) - Can run in parallel with Task Group 2: Python constants module
4. **Testing Layer** (Task Group 4) - Final validation: Cross-platform synchronization tests

**Parallelization Notes:**
- Task Groups 2 and 3 can be executed in parallel after Task Group 1 completes
- Both depend only on the shared JSON from Task Group 1
- Task Group 4 must wait for all previous groups to complete

## File Structure Summary

After completion, the following files should exist:

```
/shared/
  colors.json              # Single source of truth (Task 1.5)

/frontend/
  src/
    constants/
      colors.ts            # TypeScript constants (Task 2.2)
  tailwind.config.js       # Extended with colors (Task 2.3)

/backend/
  app/
    constants/
      colors.py            # Python constants (Task 3.2)
```

## Color Token Reference

For implementation reference, the 8 canonical color tokens with their variants:

| Token   | Dark | Base | Bright |
|---------|------|------|--------|
| BLUE    | Yes  | Yes  | Yes    |
| ORANGE  | Yes  | Yes  | Yes    |
| PURPLE  | Yes  | Yes  | Yes    |
| BLACK   | No*  | Yes  | Yes    |
| CYAN    | Yes  | Yes  | Yes    |
| AMBER   | Yes  | Yes  | Yes    |
| MAGENTA | Yes  | Yes  | Yes    |
| GRAY    | Yes  | Yes  | Yes    |

*BLACK may omit dark variant per PRD precedent (23-24 total values)
