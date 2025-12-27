/**
 * Color Token System for ColorFocus
 *
 * This module provides the canonical color tokens for the ColorFocus application.
 * All colors are imported from the shared source of truth (colors.json) to ensure
 * consistency between frontend and backend.
 *
 * Updated for the accessible color palette replacement:
 * - New tokens: BLACK, BROWN, PURPLE, BLUE, GRAY, PINK, ORANGE, YELLOW
 * - Old tokens removed: CYAN, AMBER, MAGENTA
 * - Flat hex structure (no variant objects)
 *
 * @module colors
 */

import colorsData from '../../../shared/colors.json';

/**
 * Canonical color token identifiers for the accessible color palette.
 * These 8 tokens represent the complete color palette for ColorFocus puzzles,
 * ordered by luminance from darkest to lightest.
 *
 * Luminance order (10% to 84%):
 *   BLACK (10%) -> BROWN (28%) -> PURPLE (35%) -> BLUE (38%) ->
 *   GRAY (50%) -> PINK (52%) -> ORANGE (62%) -> YELLOW (84%)
 *
 * @enum {string}
 * @example
 * ```typescript
 * const selectedColor = ColorToken.BLUE;
 * const hexValue = COLORS[selectedColor];
 * ```
 */
export enum ColorToken {
  /** Black - Darkest color, 10% luminance */
  BLACK = 'BLACK',
  /** Brown - Earth tone, 28% luminance */
  BROWN = 'BROWN',
  /** Purple - Cool accent, 35% luminance */
  PURPLE = 'PURPLE',
  /** Blue - Primary cool color, 38% luminance */
  BLUE = 'BLUE',
  /** Gray - Neutral midpoint, 50% luminance */
  GRAY = 'GRAY',
  /** Pink - Warm accent, 52% luminance */
  PINK = 'PINK',
  /** Orange - High visibility warm color, 62% luminance */
  ORANGE = 'ORANGE',
  /** Yellow - Lightest color, 84% luminance */
  YELLOW = 'YELLOW',
}

/**
 * Type for the raw colors data imported from JSON (flat hex values).
 */
type ColorsJson = Record<string, string>;

/**
 * Master color registry providing programmatic access to all 8 hex color values.
 *
 * Structure: `COLORS[ColorToken]` returns the hex color string directly.
 *
 * @example
 * ```typescript
 * // Get a specific color value
 * const blue = COLORS[ColorToken.BLUE];      // '#0066CC'
 * const yellow = COLORS[ColorToken.YELLOW];  // '#FFD700'
 * ```
 *
 * @constant
 */
export const COLORS: Record<ColorToken, string> = (() => {
  const colors = colorsData as ColorsJson;
  const result: Record<string, string> = {};

  for (const token of Object.values(ColorToken)) {
    const hexValue = colors[token];
    if (hexValue) {
      result[token] = hexValue;
    }
  }

  return result as Record<ColorToken, string>;
})();

/**
 * Array of all color token names for iteration.
 *
 * @example
 * ```typescript
 * ALL_COLOR_TOKENS.forEach(token => {
 *   console.log(`${token}: ${COLORS[token]}`);
 * });
 * ```
 *
 * @constant
 */
export const ALL_COLOR_TOKENS: readonly ColorToken[] = Object.values(ColorToken);

/**
 * Get the hex color value for a specific token.
 *
 * @param token - The color token
 * @returns The hex color value
 *
 * @example
 * ```typescript
 * const color = getColor(ColorToken.BLUE); // '#0066CC'
 * ```
 */
export function getColor(token: ColorToken): string {
  return COLORS[token];
}
