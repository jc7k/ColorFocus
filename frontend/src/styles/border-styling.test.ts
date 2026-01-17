/**
 * Tests for CSS Styling - Apple-esque Design
 *
 * These tests verify that the frontend puzzle.html CSS follows the
 * Apple-esque design with subtle shadows and soft styling:
 * 1. .puzzle-cell uses subtle shadows instead of bold borders
 * 2. .color-swatch has soft border styling
 * 3. Design system uses CSS custom properties
 *
 * Note: These tests parse the CSS from puzzle.html to verify styling rules.
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

// Check if CSS contains a declaration with a specific property
function hasDeclaration(ruleContent: string | null, property: string, value?: string): boolean {
  if (!ruleContent) return false;
  const normalizedContent = ruleContent.replace(/\s+/g, ' ').toLowerCase();
  if (value) {
    return normalizedContent.includes(`${property.toLowerCase()}: ${value.toLowerCase()}`);
  }
  return normalizedContent.includes(`${property.toLowerCase()}:`);
}

// Check if CSS uses CSS custom properties (var())
function usesCustomProperty(ruleContent: string | null, varName?: string): boolean {
  if (!ruleContent) return false;
  if (varName) {
    return ruleContent.includes(`var(--${varName})`);
  }
  return ruleContent.includes('var(--');
}

const css = extractCSSFromHTML(puzzleHtml);

describe('CSS Styling - Apple-esque Design', () => {
  describe('.puzzle-cell uses subtle shadow styling', () => {
    it('should have a .puzzle-cell CSS rule', () => {
      const ruleContent = getCSSRuleContent(css, '.puzzle-cell');
      expect(ruleContent).not.toBeNull();
    });

    it('should use border: none for soft appearance', () => {
      const ruleContent = getCSSRuleContent(css, '.puzzle-cell');
      expect(hasDeclaration(ruleContent, 'border', 'none')).toBe(true);
    });

    it('should use box-shadow for subtle depth', () => {
      const ruleContent = getCSSRuleContent(css, '.puzzle-cell');
      expect(hasDeclaration(ruleContent, 'box-shadow')).toBe(true);
    });
  });

  describe('.color-swatch has styled appearance', () => {
    it('should have a .color-swatch CSS rule', () => {
      const ruleContent = getCSSRuleContent(css, '.color-swatch');
      expect(ruleContent).not.toBeNull();
    });

    it('should have border styling', () => {
      const ruleContent = getCSSRuleContent(css, '.color-swatch');
      // Should have some form of border (can be 1px or use CSS variable)
      expect(hasDeclaration(ruleContent, 'border')).toBe(true);
    });
  });

  describe('Design system uses CSS custom properties', () => {
    it('should define design tokens in :root', () => {
      const rootContent = getCSSRuleContent(css, ':root');
      expect(rootContent).not.toBeNull();
    });

    it('should define color tokens', () => {
      const rootContent = getCSSRuleContent(css, ':root');
      expect(rootContent).toContain('--color-');
    });

    it('should define spacing tokens', () => {
      const rootContent = getCSSRuleContent(css, ':root');
      expect(rootContent).toContain('--space-');
    });

    it('should define radius tokens', () => {
      const rootContent = getCSSRuleContent(css, ':root');
      expect(rootContent).toContain('--radius-');
    });

    it('should define shadow tokens', () => {
      const rootContent = getCSSRuleContent(css, ':root');
      expect(rootContent).toContain('--shadow-');
    });
  });
});
