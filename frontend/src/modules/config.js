/**
 * Configuration constants and validation functions.
 * No dependencies - pure data and utility functions.
 */

// All color tokens in luminance order (accessible color palette)
// BLACK (10%) -> BROWN (28%) -> PURPLE (35%) -> BLUE (38%) -> GRAY (50%) -> PINK (52%) -> ORANGE (62%) -> YELLOW (84%)
export const ALL_COLOR_TOKENS = ['BLACK', 'BROWN', 'PURPLE', 'BLUE', 'GRAY', 'PINK', 'ORANGE', 'YELLOW'];

// Color subsets by count (ordered by luminance contrast for accessibility)
// Accessible tier (2): Maximum contrast - BLACK and YELLOW
// Standard tier (4): Balanced difficulty - BLACK, BLUE, ORANGE, YELLOW
// Advanced tier (8): Full palette
export const COLOR_SUBSETS = {
  2: ['BLACK', 'YELLOW'],
  3: ['BLACK', 'BLUE', 'YELLOW'],
  4: ['BLACK', 'BLUE', 'ORANGE', 'YELLOW'],
  5: ['BLACK', 'PURPLE', 'BLUE', 'ORANGE', 'YELLOW'],
  6: ['BLACK', 'PURPLE', 'BLUE', 'PINK', 'ORANGE', 'YELLOW'],
  7: ['BLACK', 'BROWN', 'PURPLE', 'BLUE', 'PINK', 'ORANGE', 'YELLOW'],
  8: ALL_COLOR_TOKENS,
};

// Valid language values for input validation
export const VALID_LANGUAGES = ['zh-TW', 'english', 'spanish', 'vietnamese'];

// Valid grid sizes (1-8)
export const VALID_GRID_SIZES = [1, 2, 3, 4, 5, 6, 7, 8];

// Valid difficulty tiers (controls Stroop interference only)
export const VALID_DIFFICULTIES = ['easy', 'medium', 'hard', 'expert'];

// Valid spacing options
export const VALID_SPACINGS = ['compact', 'normal', 'relaxed', 'spacious'];

// Difficulty presets: congruence % only (higher = easier, less Stroop interference)
export const DIFFICULTY_PRESETS = {
  easy: { congruencePercent: 75 },
  medium: { congruencePercent: 50 },
  hard: { congruencePercent: 25 },
  expert: { congruencePercent: 0 }
};

// Map old difficulty values to new ones for localStorage migration
export const DIFFICULTY_MIGRATION = {
  accessible: 'easy',
  standard: 'medium',
  advanced: 'expert',
  custom: 'medium'
};

// Spacing presets: gap in pixels
export const SPACING_VALUES = {
  compact: 1,
  normal: 2,
  relaxed: 6,
  spacious: 12
};

// ===========================================
// VALIDATION FUNCTIONS
// ===========================================

/**
 * Sanitize text content to prevent XSS (escapes HTML entities)
 */
export function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Validate and sanitize numeric input
 */
export function sanitizeNumber(value, min, max, defaultValue) {
  const num = parseFloat(value);
  if (isNaN(num)) return defaultValue;
  return Math.max(min, Math.min(max, num));
}

/**
 * Validate language selection
 */
export function validateLanguage(lang) {
  return VALID_LANGUAGES.includes(lang) ? lang : 'zh-TW';
}

/**
 * Validate grid size selection
 */
export function validateGridSize(size) {
  const num = parseInt(size, 10);
  return VALID_GRID_SIZES.includes(num) ? num : 4;
}

/**
 * Validate difficulty selection (with migration from old values)
 */
export function validateDifficulty(difficulty) {
  if (VALID_DIFFICULTIES.includes(difficulty)) return difficulty;
  // Migrate old difficulty values to new ones
  if (DIFFICULTY_MIGRATION[difficulty]) return DIFFICULTY_MIGRATION[difficulty];
  return 'easy'; // New default
}

/**
 * Validate spacing selection
 */
export function validateSpacing(spacing) {
  return VALID_SPACINGS.includes(spacing) ? spacing : 'normal';
}

/**
 * Validate sound enabled setting from localStorage
 */
export function validateSoundEnabled(value) {
  return value === 'true';
}
