/**
 * Tests for CSS Border Styling - Accessible Color Palette
 *
 * These tests verify that the frontend puzzle.html CSS:
 * 1. .puzzle-cell has 2px solid #1A1A1A border
 * 2. .color-swatch (answer input) has 2px solid #1A1A1A border
 * 3. .answer-key-item .color-swatch has 2px solid #1A1A1A border
 *
 * Note: These tests parse the CSS from puzzle.html to verify border rules.
 */

import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load puzzle.html to parse CSS (path: frontend/src/styles -> frontend/puzzle.html)
const puzzleHtmlPath = resolve(__dirname, '../../puzzle.html');
const puzzleHtml = readFileSync(puzzleHtmlPath, 'utf-8');

// Extract CSS from <style> tag
function extractCSSFromHTML(html: string): string {
  const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
  return styleMatch ? styleMatch[1] : '';
}

// Parse a CSS rule block for a specific selector
// Returns the content between { and } for the first matching selector
function getCSSRuleContent(css: string, selector: string): string | null {
  // Handle complex selectors by escaping special chars for regex
  const escapedSelector = selector.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  // Match the selector followed by optional whitespace and opening brace
  const regex = new RegExp(`${escapedSelector}\\s*\\{([^}]+)\\}`, 'g');
  const match = regex.exec(css);
  return match ? match[1].trim() : null;
}

// Check if a CSS rule block contains a specific border declaration
function hasBorderDeclaration(ruleContent: string | null, expectedBorder: string): boolean {
  if (!ruleContent) return false;
  // Normalize whitespace and check for border declaration
  const normalizedContent = ruleContent.replace(/\s+/g, ' ').toLowerCase();
  const normalizedExpected = expectedBorder.toLowerCase().replace(/\s+/g, ' ');
  return normalizedContent.includes(`border: ${normalizedExpected}`);
}

const css = extractCSSFromHTML(puzzleHtml);
const EXPECTED_BORDER = '2px solid #1A1A1A';

describe('CSS Border Styling - Accessible Color Palette', () => {
  describe('.puzzle-cell has 2px solid #1A1A1A border', () => {
    it('should have a .puzzle-cell CSS rule', () => {
      const ruleContent = getCSSRuleContent(css, '.puzzle-cell');
      expect(ruleContent).not.toBeNull();
    });

    it('should have border: 2px solid #1A1A1A in .puzzle-cell rule', () => {
      const ruleContent = getCSSRuleContent(css, '.puzzle-cell');
      expect(hasBorderDeclaration(ruleContent, EXPECTED_BORDER)).toBe(true);
    });
  });

  describe('.color-swatch (answer input) has 2px solid #1A1A1A border', () => {
    it('should have a .color-swatch CSS rule', () => {
      const ruleContent = getCSSRuleContent(css, '.color-swatch');
      expect(ruleContent).not.toBeNull();
    });

    it('should have border: 2px solid #1A1A1A in .color-swatch rule', () => {
      const ruleContent = getCSSRuleContent(css, '.color-swatch');
      expect(hasBorderDeclaration(ruleContent, EXPECTED_BORDER)).toBe(true);
    });
  });

  describe('.answer-key-item .color-swatch has 2px solid #1A1A1A border', () => {
    it('should have border applied to answer key swatches', () => {
      // The border can be applied either via:
      // 1. A specific .answer-key-item .color-swatch rule
      // 2. The general .color-swatch rule (which covers all swatches)
      // Since .color-swatch already has the border, answer-key swatches inherit it
      const generalSwatchRule = getCSSRuleContent(css, '.color-swatch');
      const specificSwatchRule = getCSSRuleContent(css, '.answer-key-item .color-swatch');

      // Either the general rule has border (which applies to all swatches)
      // OR there's a specific rule for answer-key-item swatches
      const hasBorderInGeneral = hasBorderDeclaration(generalSwatchRule, EXPECTED_BORDER);
      const hasBorderInSpecific = specificSwatchRule
        ? hasBorderDeclaration(specificSwatchRule, EXPECTED_BORDER)
        : false;

      expect(hasBorderInGeneral || hasBorderInSpecific).toBe(true);
    });
  });
});
