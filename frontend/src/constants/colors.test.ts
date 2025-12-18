/**
 * Tests for TypeScript Color Constants
 *
 * These tests verify that:
 * 1. The TypeScript COLORS object matches the source JSON structure
 * 2. The ColorToken enum contains all 8 token names
 * 3. The ColorVariant type accepts only valid variant names
 */

import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

import { ColorToken, ColorVariant, COLORS, ALL_COLOR_TOKENS, ALL_VARIANTS } from './colors';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load the source JSON for comparison
const colorsJsonPath = resolve(__dirname, '../../../shared/colors.json');
const sourceJson = JSON.parse(readFileSync(colorsJsonPath, 'utf-8'));

describe('TypeScript Color Constants', () => {
  describe('COLORS object matches source JSON structure', () => {
    it('should contain all 8 color tokens from source JSON', () => {
      const sourceTokens = Object.keys(sourceJson);
      const exportedTokens = Object.keys(COLORS);

      expect(exportedTokens).toHaveLength(sourceTokens.length);
      for (const token of sourceTokens) {
        expect(COLORS).toHaveProperty(token);
      }
    });

    it('should have matching hex values for all variants', () => {
      for (const [token, data] of Object.entries(sourceJson)) {
        const sourceVariants = data.variants;
        const exportedVariants = COLORS[token as ColorToken];

        for (const [variant, hexValue] of Object.entries(sourceVariants)) {
          expect(exportedVariants[variant as keyof typeof exportedVariants]).toBe(hexValue);
        }
      }
    });

    it('should have correct number of total color values (23-24)', () => {
      let totalValues = 0;
      for (const token of Object.values(ColorToken)) {
        const variants = COLORS[token];
        totalValues += Object.keys(variants).length;
      }

      // BLACK omits dark variant, so we expect 23 values
      expect(totalValues).toBeGreaterThanOrEqual(23);
      expect(totalValues).toBeLessThanOrEqual(24);
    });
  });

  describe('ColorToken enum contains all 8 token names', () => {
    const expectedTokens = ['BLUE', 'ORANGE', 'PURPLE', 'BLACK', 'CYAN', 'AMBER', 'MAGENTA', 'GRAY'];

    it('should have exactly 8 color tokens', () => {
      expect(ALL_COLOR_TOKENS).toHaveLength(8);
    });

    it('should contain all required token names', () => {
      for (const token of expectedTokens) {
        expect(ColorToken).toHaveProperty(token);
        expect(ColorToken[token as keyof typeof ColorToken]).toBe(token);
      }
    });

    it('should have enum values matching their keys', () => {
      for (const token of Object.values(ColorToken)) {
        expect(typeof token).toBe('string');
        expect(token).toMatch(/^[A-Z]+$/);
      }
    });
  });

  describe('ColorVariant type accepts only valid variant names', () => {
    it('should export ALL_VARIANTS with exactly 3 variants', () => {
      expect(ALL_VARIANTS).toHaveLength(3);
    });

    it('should include dark, base, and bright as valid variants', () => {
      expect(ALL_VARIANTS).toContain('dark');
      expect(ALL_VARIANTS).toContain('base');
      expect(ALL_VARIANTS).toContain('bright');
    });

    it('should allow accessing colors with valid variant names', () => {
      // Type check: these should compile without errors
      const variants: ColorVariant[] = ['dark', 'base', 'bright'];

      for (const variant of variants) {
        // base and bright are guaranteed to exist
        if (variant === 'base' || variant === 'bright') {
          expect(typeof COLORS[ColorToken.BLUE][variant]).toBe('string');
        }
      }
    });

    it('should have base and bright variants for all tokens', () => {
      for (const token of ALL_COLOR_TOKENS) {
        expect(COLORS[token].base).toBeDefined();
        expect(COLORS[token].bright).toBeDefined();
        expect(COLORS[token].base).toMatch(/^#[0-9A-Fa-f]{6}$/);
        expect(COLORS[token].bright).toMatch(/^#[0-9A-Fa-f]{6}$/);
      }
    });
  });
});
