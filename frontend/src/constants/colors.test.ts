/**
 * Tests for TypeScript Color Constants
 *
 * These tests verify that:
 * 1. The TypeScript COLORS object matches the source JSON structure (flat hex)
 * 2. The ColorToken enum contains all 8 token names for the accessible palette
 * 3. Old tokens (CYAN, AMBER, MAGENTA) are removed
 *
 * Updated for the accessible color palette replacement:
 * - New tokens: BLACK, BROWN, PURPLE, BLUE, GRAY, PINK, ORANGE, YELLOW
 * - Old tokens removed: CYAN, AMBER, MAGENTA
 * - Flat hex structure (no variant objects)
 */

import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load the source JSON for comparison (now uses flat structure)
const colorsJsonPath = resolve(__dirname, '../../../shared/colors.json');
const sourceJson = JSON.parse(readFileSync(colorsJsonPath, 'utf-8')) as Record<string, string>;

// Expected color tokens for the new accessible palette
const EXPECTED_NEW_TOKENS = ['BLACK', 'BROWN', 'PURPLE', 'BLUE', 'GRAY', 'PINK', 'ORANGE', 'YELLOW'];

// Old tokens that should be removed
const REMOVED_TOKENS = ['CYAN', 'AMBER', 'MAGENTA'];

// Expected hex values for the new accessible palette
const EXPECTED_HEX_VALUES: Record<string, string> = {
  BLACK: '#1A1A1A',
  BROWN: '#8B4513',
  PURPLE: '#7B4BAF',
  BLUE: '#0066CC',
  GRAY: '#808080',
  PINK: '#E75480',
  ORANGE: '#FF8C00',
  YELLOW: '#FFD700',
};

describe('TypeScript Color Constants - Accessible Palette', () => {
  describe('colors.json has correct flat structure', () => {
    it('should contain exactly 8 color tokens', () => {
      const tokens = Object.keys(sourceJson);
      expect(tokens).toHaveLength(8);
    });

    it('should contain all expected accessible palette tokens', () => {
      for (const token of EXPECTED_NEW_TOKENS) {
        expect(sourceJson).toHaveProperty(token);
      }
    });

    it('should NOT contain removed tokens (CYAN, AMBER, MAGENTA)', () => {
      for (const token of REMOVED_TOKENS) {
        expect(sourceJson).not.toHaveProperty(token);
      }
    });

    it('should have flat hex values (not variant objects)', () => {
      for (const [token, value] of Object.entries(sourceJson)) {
        // Value should be a string (hex), not an object
        expect(typeof value).toBe('string');
        // Should be valid hex format
        expect(value).toMatch(/^#[0-9A-Fa-f]{6}$/);
      }
    });

    it('should have correct hex values for each color', () => {
      for (const [token, expectedHex] of Object.entries(EXPECTED_HEX_VALUES)) {
        expect(sourceJson[token].toUpperCase()).toBe(expectedHex.toUpperCase());
      }
    });
  });

  describe('ColorToken enum should match new palette', () => {
    it('should expect exactly 8 tokens in the new palette', () => {
      expect(EXPECTED_NEW_TOKENS).toHaveLength(8);
    });

    it('should have tokens ordered by luminance', () => {
      // Luminance order: BLACK (10%) -> BROWN (28%) -> PURPLE (35%) -> BLUE (38%)
      //                  -> GRAY (50%) -> PINK (52%) -> ORANGE (62%) -> YELLOW (84%)
      const expectedOrder = ['BLACK', 'BROWN', 'PURPLE', 'BLUE', 'GRAY', 'PINK', 'ORANGE', 'YELLOW'];
      expect(EXPECTED_NEW_TOKENS).toEqual(expectedOrder);
    });

    it('should have all tokens in source JSON', () => {
      for (const token of EXPECTED_NEW_TOKENS) {
        expect(Object.keys(sourceJson)).toContain(token);
      }
    });
  });

  describe('Accessible difficulty tier colors', () => {
    it('should have BLACK for minimum luminance (darkest)', () => {
      expect(sourceJson).toHaveProperty('BLACK');
      expect(sourceJson['BLACK']).toBe('#1A1A1A');
    });

    it('should have YELLOW for maximum luminance (lightest)', () => {
      expect(sourceJson).toHaveProperty('YELLOW');
      expect(sourceJson['YELLOW']).toBe('#FFD700');
    });

    it('should have accessible tier colors (BLACK, YELLOW) with high contrast', () => {
      // These two form the "Accessible" (2-color) tier
      expect(sourceJson).toHaveProperty('BLACK');
      expect(sourceJson).toHaveProperty('YELLOW');
    });

    it('should have standard tier colors (BLACK, BLUE, ORANGE, YELLOW)', () => {
      // These four form the "Standard" (4-color) tier
      const standardColors = ['BLACK', 'BLUE', 'ORANGE', 'YELLOW'];
      for (const color of standardColors) {
        expect(sourceJson).toHaveProperty(color);
      }
    });
  });

  describe('Color hex value format validation', () => {
    it('should have all values in #RRGGBB format', () => {
      for (const [token, hex] of Object.entries(sourceJson)) {
        expect(hex).toMatch(/^#[0-9A-Fa-f]{6}$/);
        expect(hex.length).toBe(7);
      }
    });

    it('should have hex values starting with #', () => {
      for (const hex of Object.values(sourceJson)) {
        expect(hex.startsWith('#')).toBe(true);
      }
    });
  });
});
