/**
 * Integration Tests for Counting Tiles Feature
 *
 * These tests verify end-to-end workflows and edge cases for the counting tiles feature:
 * 1. Complete workflow: select tiles -> tap swatch -> verify count
 * 2. Edge cases: all tiles selected, selection sequence with deselection
 * 3. Integration: clear selections and generatePuzzle effects on auto-fill
 */

import { describe, it, expect, beforeEach } from 'vitest';

// Simulated state and functions mirroring puzzle.html implementation
let selectedTiles: Set<number>;
let currentGridSize: number;
let focusedTileIndex: number;

// Mock input values by token
const inputValues: Map<string, string> = new Map();

// Initialize grid and state
function initializeGrid(gridSize: number): void {
  currentGridSize = gridSize;
  selectedTiles = new Set<number>();
  focusedTileIndex = 0;
  inputValues.clear();
  // Initialize answer inputs for all color tokens
  ['BLUE', 'ORANGE', 'PURPLE', 'BLACK', 'CYAN', 'AMBER', 'MAGENTA', 'GRAY'].forEach(token => {
    inputValues.set(token, '');
  });
}

// Toggle tile selection
function toggleTileSelection(index: number): void {
  if (selectedTiles.has(index)) {
    selectedTiles.delete(index);
  } else {
    selectedTiles.add(index);
  }
}

// Calculate new index based on arrow key direction
function calculateNewIndex(currentIndex: number, key: string, gridSize: number): number {
  const row = Math.floor(currentIndex / gridSize);
  const col = currentIndex % gridSize;

  switch (key) {
    case 'ArrowUp':
      return row > 0 ? currentIndex - gridSize : currentIndex;
    case 'ArrowDown':
      return row < gridSize - 1 ? currentIndex + gridSize : currentIndex;
    case 'ArrowLeft':
      return col > 0 ? currentIndex - 1 : currentIndex;
    case 'ArrowRight':
      return col < gridSize - 1 ? currentIndex + 1 : currentIndex;
    default:
      return currentIndex;
  }
}

// Navigate with arrow keys
function navigateToTile(key: string): void {
  const newIndex = calculateNewIndex(focusedTileIndex, key, currentGridSize);
  focusedTileIndex = newIndex;
}

// Toggle selection on focused tile (spacebar)
function toggleFocusedTile(): void {
  toggleTileSelection(focusedTileIndex);
}

// Auto-fill: click swatch to fill input with selected count
function handleSwatchClick(token: string): void {
  inputValues.set(token, String(selectedTiles.size));
}

// Clear all selections
function clearAllSelections(): void {
  selectedTiles.clear();
}

// Simulate generatePuzzle() behavior - clears selections
function generatePuzzle(): void {
  selectedTiles.clear();
  focusedTileIndex = 0;
}

describe('Counting Tiles Integration Tests', () => {
  describe('End-to-end workflow', () => {
    it('should correctly auto-fill count after selecting tiles via click and keyboard', () => {
      initializeGrid(4); // 4x4 grid = 16 tiles

      // User clicks to select tiles 0, 5, 10
      toggleTileSelection(0);
      toggleTileSelection(5);
      toggleTileSelection(10);

      // User navigates with keyboard and selects more
      focusedTileIndex = 0;
      navigateToTile('ArrowRight'); // focus on tile 1
      toggleFocusedTile(); // select tile 1 (index 1)

      navigateToTile('ArrowDown'); // focus on tile 5 (already selected)
      // User doesn't toggle - tile 5 remains selected

      navigateToTile('ArrowRight'); // focus on tile 6
      toggleFocusedTile(); // select tile 6

      // Now we have 5 tiles selected: 0, 1, 5, 6, 10
      expect(selectedTiles.size).toBe(5);

      // User clicks BLUE swatch to auto-fill
      handleSwatchClick('BLUE');
      expect(inputValues.get('BLUE')).toBe('5');

      // User clicks another swatch - same count should fill
      handleSwatchClick('ORANGE');
      expect(inputValues.get('ORANGE')).toBe('5');
    });

    it('should correctly handle selection/deselection sequence before auto-fill', () => {
      initializeGrid(3); // 3x3 grid = 9 tiles

      // User selects tiles
      toggleTileSelection(0);
      toggleTileSelection(1);
      toggleTileSelection(2);
      toggleTileSelection(3);
      expect(selectedTiles.size).toBe(4);

      // User realizes they made a mistake and deselects some
      toggleTileSelection(1); // deselect
      toggleTileSelection(3); // deselect
      expect(selectedTiles.size).toBe(2);

      // User selects one more
      toggleTileSelection(4);
      expect(selectedTiles.size).toBe(3);

      // Auto-fill should reflect final count of 3
      handleSwatchClick('PURPLE');
      expect(inputValues.get('PURPLE')).toBe('3');
    });
  });

  describe('Edge cases', () => {
    it('should auto-fill correct count when all tiles are selected', () => {
      initializeGrid(3); // 3x3 grid = 9 tiles

      // Select all 9 tiles
      for (let i = 0; i < 9; i++) {
        toggleTileSelection(i);
      }

      expect(selectedTiles.size).toBe(9);

      // Auto-fill should show 9
      handleSwatchClick('BLACK');
      expect(inputValues.get('BLACK')).toBe('9');
    });

    it('should auto-fill 0 after clearing all selections', () => {
      initializeGrid(4); // 4x4 grid

      // Select some tiles
      toggleTileSelection(0);
      toggleTileSelection(5);
      toggleTileSelection(10);
      expect(selectedTiles.size).toBe(3);

      // User clicks Clear Selections button
      clearAllSelections();
      expect(selectedTiles.size).toBe(0);

      // Auto-fill should now produce 0
      handleSwatchClick('CYAN');
      expect(inputValues.get('CYAN')).toBe('0');
    });

    it('should auto-fill 0 after generatePuzzle() clears selections', () => {
      initializeGrid(4); // 4x4 grid

      // Select some tiles
      toggleTileSelection(0);
      toggleTileSelection(1);
      toggleTileSelection(2);
      expect(selectedTiles.size).toBe(3);

      // User generates a new puzzle (simulates clicking Generate button)
      generatePuzzle();
      expect(selectedTiles.size).toBe(0);

      // Auto-fill should now produce 0
      handleSwatchClick('AMBER');
      expect(inputValues.get('AMBER')).toBe('0');
    });

    it('should maintain correct count when switching between different grid sizes', () => {
      // Start with 3x3 grid
      initializeGrid(3);
      toggleTileSelection(0);
      toggleTileSelection(1);
      expect(selectedTiles.size).toBe(2);

      handleSwatchClick('MAGENTA');
      expect(inputValues.get('MAGENTA')).toBe('2');

      // User generates new puzzle with larger grid (4x4)
      // generatePuzzle clears selections
      generatePuzzle();
      currentGridSize = 4;

      // Select new tiles on the new grid
      toggleTileSelection(0);
      toggleTileSelection(5);
      toggleTileSelection(10);
      toggleTileSelection(15);
      expect(selectedTiles.size).toBe(4);

      handleSwatchClick('GRAY');
      expect(inputValues.get('GRAY')).toBe('4');
    });
  });
});
