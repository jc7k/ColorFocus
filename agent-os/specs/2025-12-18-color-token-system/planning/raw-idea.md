# Raw Idea: Color Token System

## Feature Description (from Product Roadmap)

Implement the 8 canonical color tokens (BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY) with DARK, BASE, and BRIGHT variants, ensuring all colors are distinguishable for common forms of color blindness.

## Size Estimate
S (Small)

## Priority
Phase 1: MVP - Core Puzzle Experience (Item #1)

## Context
This is the foundational feature for the ColorFocus Stroop test application. The color token system provides the palette that will be used throughout the puzzle generation, display, and scoring functionality. Accessibility is a core requirement - all colors must be distinguishable for users with common forms of color blindness.

## Key Requirements (Initial Understanding)
- 8 canonical colors: BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY
- Each color has 3 variants: DARK, BASE, BRIGHT (24 total color values)
- Color blindness considerations: must be distinguishable for common forms (protanopia, deuteranopia, tritanopia)
- System should provide consistent color values across the application
