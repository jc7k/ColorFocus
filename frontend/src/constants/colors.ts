/**
 * Color Token System for ColorFocus
 *
 * This module provides the canonical color tokens for the ColorFocus application.
 * All colors are imported from the shared source of truth (colors.json) to ensure
 * consistency between frontend and backend.
 *
 * @module colors
 */

import colorsData from '../../../shared/colors.json';

/**
 * Canonical color token identifiers.
 * These 8 tokens represent the complete color palette for ColorFocus puzzles.
 *
 * @enum {string}
 * @example
 * ```typescript
 * const selectedColor = ColorToken.BLUE;
 * const hexValue = COLORS[selectedColor].base;
 * ```
 */
export enum ColorToken {
  /** Blue - Primary color for standard puzzles */
  BLUE = 'BLUE',
  /** Orange - High visibility warm color */
  ORANGE = 'ORANGE',
  /** Purple - Secondary color for variety */
  PURPLE = 'PURPLE',
  /** Black - Neutral anchor color (no dark variant) */
  BLACK = 'BLACK',
  /** Cyan - Cool color distinct from blue */
  CYAN = 'CYAN',
  /** Amber - Warm golden color */
  AMBER = 'AMBER',
  /** Magenta - Warm-cool bridge color */
  MAGENTA = 'MAGENTA',
  /** Gray - Neutral color for contrast */
  GRAY = 'GRAY',
}

/**
 * Brightness variant identifiers for color tokens.
 * Each color token (except BLACK) has three variants for accessibility.
 *
 * - `dark`: Reduced lightness for high-contrast needs
 * - `base`: Default brightness level
 * - `bright`: Increased lightness for low-vision accessibility
 *
 * @typedef {'dark' | 'base' | 'bright'} ColorVariant
 */
export type ColorVariant = 'dark' | 'base' | 'bright';

/**
 * Type definition for the variants object of a color token.
 * Maps variant names to hex color values.
 */
type ColorVariants = Partial<Record<ColorVariant, string>>;

/**
 * Raw color data structure as loaded from JSON.
 */
interface ColorData {
  variants: ColorVariants;
  hsl_reference?: Record<string, string>;
}

/**
 * Type for the raw colors data imported from JSON.
 */
type ColorsJson = Record<string, ColorData>;

/**
 * Processed color variants with guaranteed hex values.
 * Used for the public COLORS object.
 */
interface ProcessedColorVariants {
  dark?: string;
  base: string;
  bright: string;
}

/**
 * Master color registry providing programmatic access to all 24 hex color values.
 *
 * Structure: `COLORS[ColorToken][ColorVariant]`
 *
 * @example
 * ```typescript
 * // Get a specific color value
 * const blueBase = COLORS[ColorToken.BLUE].base;      // '#2E86DE'
 * const orangeBright = COLORS[ColorToken.ORANGE].bright; // '#FFB366'
 *
 * // Use with Tailwind classes
 * const className = `text-${ColorToken.BLUE.toLowerCase()}-base`;
 * ```
 *
 * @constant
 */
export const COLORS: Record<ColorToken, ProcessedColorVariants> = (() => {
  const colors = colorsData as ColorsJson;
  const result: Record<string, ProcessedColorVariants> = {};

  for (const token of Object.values(ColorToken)) {
    const colorData = colors[token];
    if (colorData && colorData.variants) {
      result[token] = {
        base: colorData.variants.base!,
        bright: colorData.variants.bright!,
        ...(colorData.variants.dark && { dark: colorData.variants.dark }),
      };
    }
  }

  return result as Record<ColorToken, ProcessedColorVariants>;
})();

/**
 * Array of all color token names for iteration.
 *
 * @example
 * ```typescript
 * ALL_COLOR_TOKENS.forEach(token => {
 *   console.log(`${token}: ${COLORS[token].base}`);
 * });
 * ```
 *
 * @constant
 */
export const ALL_COLOR_TOKENS: readonly ColorToken[] = Object.values(ColorToken);

/**
 * Array of all variant names for iteration.
 *
 * @constant
 */
export const ALL_VARIANTS: readonly ColorVariant[] = ['dark', 'base', 'bright'];

/**
 * Get the hex color value for a specific token and variant combination.
 *
 * @param token - The color token
 * @param variant - The brightness variant (defaults to 'base')
 * @returns The hex color value, or undefined if the variant doesn't exist
 *
 * @example
 * ```typescript
 * const color = getColor(ColorToken.BLUE, 'bright'); // '#6BB6FF'
 * const defaultColor = getColor(ColorToken.ORANGE); // '#E67E22' (base)
 * ```
 */
export function getColor(token: ColorToken, variant: ColorVariant = 'base'): string | undefined {
  return COLORS[token][variant];
}
