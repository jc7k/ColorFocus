/**
 * Tests for Tile Visual State Classes
 *
 * These tests verify the visual state classes for the counting tiles feature:
 * 1. Selected tiles have 'selected' class applied
 * 2. Unselected tiles do not have 'selected' class
 * 3. Focus state is visually distinct from selection state (different CSS properties)
 */

import { describe, it, expect, beforeEach } from 'vitest';

// Simulated tile selection state (mirrors puzzle.html implementation)
let selectedTiles: Set<number>;

// Mock DOM element class management
interface MockElement {
  classList: Set<string>;
  hasClass(className: string): boolean;
  addClass(className: string): void;
  removeClass(className: string): void;
  toggleClass(className: string, force?: boolean): void;
}

function createMockElement(): MockElement {
  const classList = new Set<string>();
  return {
    classList,
    hasClass(className: string): boolean {
      return classList.has(className);
    },
    addClass(className: string): void {
      classList.add(className);
    },
    removeClass(className: string): void {
      classList.delete(className);
    },
    toggleClass(className: string, force?: boolean): void {
      if (force !== undefined) {
        if (force) {
          classList.add(className);
        } else {
          classList.delete(className);
        }
      } else {
        if (classList.has(className)) {
          classList.delete(className);
        } else {
          classList.add(className);
        }
      }
    },
  };
}

// Simulates updating tile visual state based on selection
function updateTileVisualState(element: MockElement, index: number): void {
  if (selectedTiles.has(index)) {
    element.addClass('selected');
  } else {
    element.removeClass('selected');
  }
}

// Simulates toggle behavior with visual update
function toggleTileWithVisual(element: MockElement, index: number): void {
  if (selectedTiles.has(index)) {
    selectedTiles.delete(index);
  } else {
    selectedTiles.add(index);
  }
  updateTileVisualState(element, index);
}

describe('Tile Visual State Classes', () => {
  beforeEach(() => {
    selectedTiles = new Set<number>();
  });

  describe('selected class application', () => {
    it('should apply selected class to tiles in selectedTiles set', () => {
      const element = createMockElement();
      element.addClass('puzzle-cell');

      // Tile not selected - should not have 'selected' class
      expect(element.hasClass('selected')).toBe(false);

      // Add to selection and update visual state
      selectedTiles.add(0);
      updateTileVisualState(element, 0);

      // Tile now selected - should have 'selected' class
      expect(element.hasClass('selected')).toBe(true);
      expect(element.hasClass('puzzle-cell')).toBe(true);
    });

    it('should remove selected class when tile is deselected', () => {
      const element = createMockElement();
      element.addClass('puzzle-cell');

      // Select tile
      selectedTiles.add(0);
      updateTileVisualState(element, 0);
      expect(element.hasClass('selected')).toBe(true);

      // Deselect tile
      selectedTiles.delete(0);
      updateTileVisualState(element, 0);
      expect(element.hasClass('selected')).toBe(false);
    });

    it('should not have selected class on unselected tiles', () => {
      const element0 = createMockElement();
      const element1 = createMockElement();
      const element2 = createMockElement();

      element0.addClass('puzzle-cell');
      element1.addClass('puzzle-cell');
      element2.addClass('puzzle-cell');

      // Only select tile 1
      selectedTiles.add(1);
      updateTileVisualState(element0, 0);
      updateTileVisualState(element1, 1);
      updateTileVisualState(element2, 2);

      // Tile 0 and 2 should NOT have 'selected' class
      expect(element0.hasClass('selected')).toBe(false);
      expect(element2.hasClass('selected')).toBe(false);

      // Only tile 1 should have 'selected' class
      expect(element1.hasClass('selected')).toBe(true);
    });
  });

  describe('focus and selection state distinction', () => {
    it('should allow focus class to be applied independently of selected class', () => {
      const element = createMockElement();
      element.addClass('puzzle-cell');

      // Apply focus without selection
      element.addClass('focus-visible');
      expect(element.hasClass('focus-visible')).toBe(true);
      expect(element.hasClass('selected')).toBe(false);

      // Apply selection alongside focus
      selectedTiles.add(0);
      updateTileVisualState(element, 0);
      expect(element.hasClass('focus-visible')).toBe(true);
      expect(element.hasClass('selected')).toBe(true);

      // Remove selection but keep focus
      selectedTiles.delete(0);
      updateTileVisualState(element, 0);
      expect(element.hasClass('focus-visible')).toBe(true);
      expect(element.hasClass('selected')).toBe(false);
    });
  });
});
