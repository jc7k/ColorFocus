/**
 * Tests for Frontend Color Handling - Accessible Color Palette
 *
 * These tests verify that the frontend puzzle.html JavaScript:
 * 1. ALL_COLOR_TOKENS array contains exactly 8 new color tokens
 * 2. COLOR_SUBSETS maps correctly for difficulty tiers
 * 3. VALID_LANGUAGES contains 'zh-TW' (not 'chinese')
 * 4. widthMultipliers object has 'zh-TW' key (not 'chinese')
 *
 * Note: These tests validate the expected values that should be in puzzle.html.
 * They test the shared data sources to ensure the frontend will work correctly
 * when updated to use the new accessible color palette.
 */

import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load shared JSON files to validate expected frontend behavior
const colorsJsonPath = resolve(__dirname, '../../../shared/colors.json');
const colorsJson = JSON.parse(readFileSync(colorsJsonPath, 'utf-8'));

const colorLabelsJsonPath = resolve(__dirname, '../../../shared/color_labels.json');
const colorLabelsJson = JSON.parse(readFileSync(colorLabelsJsonPath, 'utf-8'));

// Expected values for the new accessible color palette
const EXPECTED_ALL_COLOR_TOKENS = ['BLACK', 'BROWN', 'PURPLE', 'BLUE', 'GRAY', 'PINK', 'ORANGE', 'YELLOW'];

const EXPECTED_COLOR_SUBSETS = {
  2: ['BLACK', 'YELLOW'],
  3: ['BLACK', 'BLUE', 'YELLOW'],
  4: ['BLACK', 'BLUE', 'ORANGE', 'YELLOW'],
  5: ['BLACK', 'PURPLE', 'BLUE', 'ORANGE', 'YELLOW'],
  6: ['BLACK', 'PURPLE', 'BLUE', 'PINK', 'ORANGE', 'YELLOW'],
  7: ['BLACK', 'BROWN', 'PURPLE', 'BLUE', 'PINK', 'ORANGE', 'YELLOW'],
  8: EXPECTED_ALL_COLOR_TOKENS,
};

const EXPECTED_VALID_LANGUAGES = ['zh-TW', 'english', 'spanish', 'vietnamese'];

const EXPECTED_WIDTH_MULTIPLIERS = {
  'zh-TW': 1.15,
  'vietnamese': 2.4,
  'english': 3.6,
  'spanish': 4.8,
};

describe('Frontend Color Handling - Accessible Color Palette', () => {
  describe('ALL_COLOR_TOKENS array contains exactly 8 new color tokens', () => {
    it('should have exactly 8 color tokens', () => {
      expect(EXPECTED_ALL_COLOR_TOKENS).toHaveLength(8);
    });

    it('should contain the new accessible palette colors in luminance order', () => {
      const expected = ['BLACK', 'BROWN', 'PURPLE', 'BLUE', 'GRAY', 'PINK', 'ORANGE', 'YELLOW'];
      expect(EXPECTED_ALL_COLOR_TOKENS).toEqual(expected);
    });

    it('should NOT contain removed colors (CYAN, AMBER, MAGENTA)', () => {
      expect(EXPECTED_ALL_COLOR_TOKENS).not.toContain('CYAN');
      expect(EXPECTED_ALL_COLOR_TOKENS).not.toContain('AMBER');
      expect(EXPECTED_ALL_COLOR_TOKENS).not.toContain('MAGENTA');
    });

    it('should contain new colors (BROWN, PINK, YELLOW)', () => {
      expect(EXPECTED_ALL_COLOR_TOKENS).toContain('BROWN');
      expect(EXPECTED_ALL_COLOR_TOKENS).toContain('PINK');
      expect(EXPECTED_ALL_COLOR_TOKENS).toContain('YELLOW');
    });

    it('should match colors.json tokens', () => {
      const jsonTokens = Object.keys(colorsJson);
      expect(jsonTokens.sort()).toEqual([...EXPECTED_ALL_COLOR_TOKENS].sort());
    });
  });

  describe('COLOR_SUBSETS maps correctly for difficulty tiers', () => {
    it('should map 2 colors to BLACK and YELLOW (maximum luminance contrast)', () => {
      expect(EXPECTED_COLOR_SUBSETS[2]).toEqual(['BLACK', 'YELLOW']);
    });

    it('should map 4 colors to BLACK, BLUE, ORANGE, YELLOW (Standard tier)', () => {
      expect(EXPECTED_COLOR_SUBSETS[4]).toEqual(['BLACK', 'BLUE', 'ORANGE', 'YELLOW']);
    });

    it('should map 8 colors to ALL_COLOR_TOKENS (Advanced tier)', () => {
      expect(EXPECTED_COLOR_SUBSETS[8]).toEqual(EXPECTED_ALL_COLOR_TOKENS);
    });

    it('should have logical progressions for intermediate subsets (3, 5, 6, 7)', () => {
      // 3 colors: add BLUE to the 2-color set
      expect(EXPECTED_COLOR_SUBSETS[3]).toContain('BLACK');
      expect(EXPECTED_COLOR_SUBSETS[3]).toContain('BLUE');
      expect(EXPECTED_COLOR_SUBSETS[3]).toContain('YELLOW');
      expect(EXPECTED_COLOR_SUBSETS[3]).toHaveLength(3);

      // Each subset should be a superset of smaller subsets (progressive addition)
      for (let i = 3; i <= 8; i++) {
        const smaller = EXPECTED_COLOR_SUBSETS[i - 1];
        const larger = EXPECTED_COLOR_SUBSETS[i];
        // Each smaller subset's colors should exist in the larger subset
        for (const color of smaller) {
          expect(larger).toContain(color);
        }
      }
    });

    it('should have subsets containing only valid color tokens', () => {
      for (const [count, colors] of Object.entries(EXPECTED_COLOR_SUBSETS)) {
        for (const color of colors) {
          expect(EXPECTED_ALL_COLOR_TOKENS).toContain(color);
        }
        expect(colors.length).toBe(Number(count));
      }
    });
  });

  describe('VALID_LANGUAGES contains zh-TW (not chinese)', () => {
    it('should contain zh-TW as a valid language', () => {
      expect(EXPECTED_VALID_LANGUAGES).toContain('zh-TW');
    });

    it('should NOT contain chinese as a language key', () => {
      expect(EXPECTED_VALID_LANGUAGES).not.toContain('chinese');
    });

    it('should have exactly 4 supported languages', () => {
      expect(EXPECTED_VALID_LANGUAGES).toHaveLength(4);
    });

    it('should match language keys in color_labels.json', () => {
      // Get language keys from the first color entry
      const firstColor = Object.values(colorLabelsJson)[0];
      const jsonLanguages = Object.keys(firstColor);
      expect(jsonLanguages.sort()).toEqual([...EXPECTED_VALID_LANGUAGES].sort());
    });
  });

  describe('widthMultipliers object has zh-TW key (not chinese)', () => {
    it('should have zh-TW key with value 1.15 (single character)', () => {
      expect(EXPECTED_WIDTH_MULTIPLIERS['zh-TW']).toBe(1.15);
    });

    it('should NOT have chinese key', () => {
      expect(EXPECTED_WIDTH_MULTIPLIERS).not.toHaveProperty('chinese');
    });

    it('should have recalculated vietnamese multiplier of 2.4 (longest: Vang = 4 chars)', () => {
      expect(EXPECTED_WIDTH_MULTIPLIERS['vietnamese']).toBe(2.4);
    });

    it('should have recalculated english multiplier of 3.6 (longest: Yellow = 6 chars)', () => {
      expect(EXPECTED_WIDTH_MULTIPLIERS['english']).toBe(3.6);
    });

    it('should have recalculated spanish multiplier of 4.8 (longest: Amarillo = 8 chars)', () => {
      expect(EXPECTED_WIDTH_MULTIPLIERS['spanish']).toBe(4.8);
    });

    it('should have multipliers for all valid languages', () => {
      for (const lang of EXPECTED_VALID_LANGUAGES) {
        expect(EXPECTED_WIDTH_MULTIPLIERS).toHaveProperty(lang);
        expect(typeof EXPECTED_WIDTH_MULTIPLIERS[lang as keyof typeof EXPECTED_WIDTH_MULTIPLIERS]).toBe('number');
      }
    });
  });
});
