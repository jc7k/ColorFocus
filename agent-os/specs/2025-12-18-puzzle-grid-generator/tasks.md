# Task Breakdown: Puzzle Grid Generator

## Overview
Total Tasks: 18

This feature implements a deterministic algorithm that generates 8x8 word jungle grids with color words rendered in different ink colors, creating Stroop interference patterns for cognitive training exercises.

## Task List

### Data Models & Constants

#### Task Group 1: Color Labels and Data Structures
**Dependencies:** None (builds on existing ColorToken enum)

- [x] 1.0 Complete color labels and data structures
  - [x] 1.1 Write 3-5 focused tests for color labels and puzzle data structures
    - Test that all 8 ColorToken values have Chinese labels defined
    - Test that PuzzleCell dataclass contains word and inkColor fields
    - Test that PuzzleGrid dataclass contains grid, metadata (seed, dimensions, congruence_percentage)
    - Test JSON serialization of puzzle structures
  - [x] 1.2 Add Chinese color labels to shared data
    - Add labels mapping to `shared/colors.json` or create `shared/color_labels.json`
    - Labels per PRD: BLUE=藍, ORANGE=橙, PURPLE=紫, BLACK=黑, CYAN=青, AMBER=金, MAGENTA=品, GRAY=灰
    - Include English labels as secondary option: BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY
  - [x] 1.3 Create color labels Python module
    - Path: `backend/app/constants/color_labels.py`
    - Define `ColorLabel` dictionary mapping ColorToken to labels by language
    - Support Language enum (CHINESE, ENGLISH) with CHINESE as default
    - Follow pattern from existing `colors.py` module
  - [x] 1.4 Create puzzle data structures
    - Path: `backend/app/models/puzzle.py`
    - Define `PuzzleCell` dataclass with `word: ColorToken` and `ink_color: ColorToken` fields
    - Define `PuzzleMetadata` dataclass with `seed: int`, `rows: int`, `cols: int`, `congruence_percentage: float`
    - Define `PuzzleGrid` dataclass with `cells: list[list[PuzzleCell]]` and `metadata: PuzzleMetadata`
    - Ensure all structures are JSON-serializable
  - [x] 1.5 Ensure data structure tests pass
    - Run ONLY the 3-5 tests written in 1.1
    - Verify color labels are accessible
    - Verify data structures serialize correctly

**Acceptance Criteria:**
- The 3-5 tests written in 1.1 pass
- Chinese labels defined for all 8 ColorToken values
- English labels available as fallback
- PuzzleCell, PuzzleMetadata, and PuzzleGrid are properly structured
- All structures can be serialized to JSON

### Service Layer

#### Task Group 2: Puzzle Generation Algorithm
**Dependencies:** Task Group 1

- [x] 2.0 Complete puzzle generation service
  - [x] 2.1 Write 5-8 focused tests for puzzle generation
    - Test that generate() returns an 8x8 grid (64 cells total)
    - Test that same seed produces identical grids (reproducibility)
    - Test that different seeds produce different grids
    - Test that ink color distribution is roughly equal (each color appears ~8 times, within tolerance)
    - Test that congruence percentage parameter affects word-ink matching
    - Test that default congruence is low (mostly incongruent for Stroop effect)
    - Test that auto-generated seed is included in metadata when none provided
  - [x] 2.2 Create puzzle generator service class
    - Path: `backend/app/services/puzzle_generator.py`
    - Create `PuzzleGenerator` class
    - Constructor accepts optional `seed: int | None` and `congruence_percentage: float = 0.125`
    - Use Python `random` module with explicit seeding
    - Store seed value (auto-generate if none provided)
  - [x] 2.3 Implement ink color distribution algorithm
    - Distribute 64 cells across 8 colors (8 cells per color)
    - Allow minor natural variation but prevent heavy skewing
    - Validate no color appears significantly more or less than target
  - [x] 2.4 Implement word assignment with congruence control
    - For each cell, decide if word should match ink color based on congruence_percentage
    - If incongruent, select a different ColorToken for the word
    - Ensure word distribution also remains reasonably balanced
  - [x] 2.5 Implement spatial randomization
    - Shuffle cell positions after ink/word assignment
    - Convert 1D shuffled list to 2D grid structure (8x8)
  - [x] 2.6 Implement generate() method
    - Orchestrate: ink distribution -> word assignment -> shuffle -> build grid
    - Return `PuzzleGrid` with cells and metadata
    - Include seed, dimensions (8, 8), and congruence_percentage in metadata
  - [x] 2.7 Add language configuration support
    - Accept optional `language` parameter (default: CHINESE)
    - Labels used for display purposes, but ColorToken values remain canonical
  - [x] 2.8 Ensure puzzle generation tests pass
    - Run ONLY the 5-8 tests written in 2.1
    - Verify deterministic generation with seeds
    - Verify distribution constraints are met

**Acceptance Criteria:**
- The 5-8 tests written in 2.1 pass
- Generator produces valid 8x8 grids
- Same seed always produces identical output
- Ink colors are distributed roughly equally
- Congruence percentage controls word-ink matching
- Output structure matches PuzzleGrid dataclass

### Validation & Distribution

#### Task Group 3: Distribution Validation and Output Formatting
**Dependencies:** Task Group 2

- [x] 3.0 Complete validation and output formatting
  - [x] 3.1 Write 3-5 focused tests for validation and formatting
    - Test that validator rejects grids with heavily skewed color distribution
    - Test that validator accepts grids within acceptable tolerance
    - Test JSON output format matches expected structure
    - Test that to_dict() produces JSON-serializable output
  - [x] 3.2 Implement distribution validator
    - Path: Add to `backend/app/services/puzzle_generator.py` or create separate validator
    - Validate ink color distribution is within acceptable bounds
    - Define tolerance (e.g., each color should appear 6-10 times out of 64)
    - Return validation result with details
  - [x] 3.3 Add retry logic for distribution failures
    - If generated grid fails validation, regenerate with new seed derived from original
    - Limit retries to prevent infinite loops (max 3 attempts)
    - Log warning if retry needed
  - [x] 3.4 Implement to_dict() serialization method
    - Add `to_dict()` method to PuzzleGrid
    - Output format: `{ "grid": [[{word, inkColor}...]], "metadata": {seed, rows, cols, congruence_percentage} }`
    - Ensure ColorToken values are serialized as strings
  - [x] 3.5 Ensure validation tests pass
    - Run ONLY the 3-5 tests written in 3.1
    - Verify validation catches distribution issues
    - Verify JSON output is correct

**Acceptance Criteria:**
- The 3-5 tests written in 3.1 pass
- Validator correctly identifies skewed distributions
- Retry logic prevents returning invalid grids
- JSON output is clean and matches expected format

### Testing

#### Task Group 4: Test Review and Gap Analysis
**Dependencies:** Task Groups 1-3

- [x] 4.0 Review existing tests and fill critical gaps only
  - [x] 4.1 Review tests from Task Groups 1-3
    - Review the 3-5 tests written for data structures (Task 1.1)
    - Review the 5-8 tests written for puzzle generation (Task 2.1)
    - Review the 3-5 tests written for validation/formatting (Task 3.1)
    - Total existing tests: approximately 11-18 tests
  - [x] 4.2 Analyze test coverage gaps for puzzle generator feature only
    - Identify critical user workflows that lack test coverage
    - Focus ONLY on gaps related to this spec's feature requirements
    - Do NOT assess entire application test coverage
    - Prioritize end-to-end generation workflows
  - [x] 4.3 Write up to 5 additional strategic tests maximum
    - Add maximum of 5 new tests to fill identified critical gaps
    - Consider: edge case seeds (0, negative, very large)
    - Consider: extreme congruence values (0.0 = all incongruent, 1.0 = all congruent)
    - Consider: integration test for full generation flow
    - Do NOT write comprehensive coverage for all scenarios
  - [x] 4.4 Run feature-specific tests only
    - Run ONLY tests related to puzzle generator (tests from 1.1, 2.1, 3.1, and 4.3)
    - Expected total: approximately 16-23 tests maximum
    - Do NOT run the entire application test suite
    - Verify critical workflows pass

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 16-23 tests total)
- Critical user workflows for puzzle generation are covered
- No more than 5 additional tests added when filling gaps
- Testing focused exclusively on this spec's feature requirements

## Execution Order

Recommended implementation sequence:
1. **Data Models & Constants (Task Group 1)** - Foundation for the generator
2. **Service Layer (Task Group 2)** - Core algorithm implementation
3. **Validation & Distribution (Task Group 3)** - Quality assurance for output
4. **Test Review & Gap Analysis (Task Group 4)** - Final verification

## Technical Notes

### File Locations
- Color labels: `backend/app/constants/color_labels.py`
- Data structures: `backend/app/models/puzzle.py`
- Generator service: `backend/app/services/puzzle_generator.py`
- Tests: `tests/test_puzzle_generator.py`

### Dependencies
- Uses existing `ColorToken` enum from `backend/app/constants/colors.py`
- Uses Python standard library `random` module for seeding
- Uses `dataclasses` for type-safe data structures
- No new external dependencies required

### Key Algorithms
1. **Ink Distribution**: Create list of 64 ink colors (8 of each), then shuffle
2. **Word Assignment**: For each cell, use congruence_percentage to decide if word = ink_color
3. **Spatial Randomization**: Shuffle flat list, then reshape to 8x8 grid

### Out of Scope (per spec)
- REST API endpoint (separate future task)
- Answer key generation
- Difficulty tier presets
- Grid size configuration beyond 8x8
- Spatial constraints (adjacent identical colors)
- Animation data or timing information
