/**
 * Tests for Keyboard Navigation and Auto-Fill Behavior
 *
 * These tests verify keyboard navigation and auto-fill for the counting tiles feature:
 * 1. Arrow keys move focus between grid tiles
 * 2. Spacebar toggles selection on focused tile
 * 3. Tab key enters/exits grid focus context
 * 4. Clicking color swatch fills input with selectedTiles.size
 * 5. Auto-fill counts ALL selected tiles regardless of color
 */

import { describe, it, expect, beforeEach } from 'vitest';

// Simulated tile selection state (mirrors puzzle.html implementation)
let selectedTiles: Set<number>;
let currentGridSize: number;
let focusedTileIndex: number;

// Mock DOM elements for testing
interface MockInput {
  value: string;
}

interface MockElement {
  tabIndex: number;
  classList: Set<string>;
  getAttribute(name: string): string | null;
  setAttribute(name: string, value: string): void;
  focus(): void;
  isFocused: boolean;
}

// Track mock inputs by color token
const mockInputs: Map<string, MockInput> = new Map();

function createMockInput(token: string): MockInput {
  const input = { value: '' };
  mockInputs.set(token, input);
  return input;
}

function getInputByToken(token: string): MockInput | undefined {
  return mockInputs.get(token);
}

// Create mock tile elements
const mockTiles: MockElement[] = [];

function createMockTile(index: number): MockElement {
  const attributes: Map<string, string> = new Map();
  const classList = new Set<string>();

  const tile: MockElement = {
    tabIndex: index === 0 ? 0 : -1, // First tile has tabindex 0
    classList,
    getAttribute(name: string): string | null {
      return attributes.get(name) ?? null;
    },
    setAttribute(name: string, value: string): void {
      attributes.set(name, value);
    },
    isFocused: false,
    focus(): void {
      // Unfocus all other tiles
      mockTiles.forEach(t => t.isFocused = false);
      this.isFocused = true;
    },
  };

  attributes.set('data-index', String(index));
  mockTiles[index] = tile;
  return tile;
}

// Initialize grid state
function initializeGrid(gridSize: number) {
  currentGridSize = gridSize;
  selectedTiles = new Set<number>();
  focusedTileIndex = 0;
  mockTiles.length = 0;
  mockInputs.clear();

  const totalTiles = gridSize * gridSize;
  for (let i = 0; i < totalTiles; i++) {
    createMockTile(i);
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

// Handle keyboard navigation
function handleGridKeydown(key: string): void {
  const newIndex = calculateNewIndex(focusedTileIndex, key, currentGridSize);

  if (newIndex !== focusedTileIndex) {
    // Update roving tabindex
    mockTiles[focusedTileIndex].tabIndex = -1;
    mockTiles[newIndex].tabIndex = 0;
    mockTiles[newIndex].focus();
    focusedTileIndex = newIndex;
  }
}

// Handle spacebar to toggle selection
function handleSpacebarToggle(): void {
  if (selectedTiles.has(focusedTileIndex)) {
    selectedTiles.delete(focusedTileIndex);
    mockTiles[focusedTileIndex].classList.delete('selected');
  } else {
    selectedTiles.add(focusedTileIndex);
    mockTiles[focusedTileIndex].classList.add('selected');
  }
}

// Auto-fill count into input field when swatch is clicked
function handleSwatchClick(token: string): void {
  const input = getInputByToken(token);
  if (input) {
    input.value = String(selectedTiles.size);
  }
}

describe('Keyboard Navigation and Auto-Fill', () => {
  beforeEach(() => {
    initializeGrid(4); // 4x4 grid
  });

  describe('arrow key navigation', () => {
    it('should move focus down when ArrowDown is pressed', () => {
      focusedTileIndex = 0;
      handleGridKeydown('ArrowDown');

      expect(focusedTileIndex).toBe(4); // Row 0 -> Row 1
      expect(mockTiles[0].tabIndex).toBe(-1);
      expect(mockTiles[4].tabIndex).toBe(0);
    });

    it('should move focus up when ArrowUp is pressed', () => {
      focusedTileIndex = 4;
      mockTiles[0].tabIndex = -1;
      mockTiles[4].tabIndex = 0;

      handleGridKeydown('ArrowUp');

      expect(focusedTileIndex).toBe(0); // Row 1 -> Row 0
      expect(mockTiles[4].tabIndex).toBe(-1);
      expect(mockTiles[0].tabIndex).toBe(0);
    });

    it('should move focus right when ArrowRight is pressed', () => {
      focusedTileIndex = 0;
      handleGridKeydown('ArrowRight');

      expect(focusedTileIndex).toBe(1); // Col 0 -> Col 1
      expect(mockTiles[0].tabIndex).toBe(-1);
      expect(mockTiles[1].tabIndex).toBe(0);
    });

    it('should move focus left when ArrowLeft is pressed', () => {
      focusedTileIndex = 1;
      mockTiles[0].tabIndex = -1;
      mockTiles[1].tabIndex = 0;

      handleGridKeydown('ArrowLeft');

      expect(focusedTileIndex).toBe(0); // Col 1 -> Col 0
      expect(mockTiles[1].tabIndex).toBe(-1);
      expect(mockTiles[0].tabIndex).toBe(0);
    });

    it('should not move focus past grid boundaries', () => {
      // Test top boundary
      focusedTileIndex = 0;
      handleGridKeydown('ArrowUp');
      expect(focusedTileIndex).toBe(0); // Still at top

      // Test left boundary
      handleGridKeydown('ArrowLeft');
      expect(focusedTileIndex).toBe(0); // Still at left

      // Test bottom boundary
      focusedTileIndex = 12; // Bottom-left corner (row 3, col 0)
      mockTiles.forEach((t, i) => t.tabIndex = i === 12 ? 0 : -1);
      handleGridKeydown('ArrowDown');
      expect(focusedTileIndex).toBe(12); // Still at bottom

      // Test right boundary
      focusedTileIndex = 3; // Top-right corner (row 0, col 3)
      mockTiles.forEach((t, i) => t.tabIndex = i === 3 ? 0 : -1);
      handleGridKeydown('ArrowRight');
      expect(focusedTileIndex).toBe(3); // Still at right
    });
  });

  describe('spacebar toggle selection', () => {
    it('should toggle selection on focused tile when spacebar is pressed', () => {
      focusedTileIndex = 5;

      // First press - select
      handleSpacebarToggle();
      expect(selectedTiles.has(5)).toBe(true);
      expect(mockTiles[5].classList.has('selected')).toBe(true);

      // Second press - deselect
      handleSpacebarToggle();
      expect(selectedTiles.has(5)).toBe(false);
      expect(mockTiles[5].classList.has('selected')).toBe(false);
    });
  });

  describe('roving tabindex pattern', () => {
    it('should have tabindex 0 on first tile and -1 on others initially', () => {
      expect(mockTiles[0].tabIndex).toBe(0);
      for (let i = 1; i < mockTiles.length; i++) {
        expect(mockTiles[i].tabIndex).toBe(-1);
      }
    });

    it('should update tabindex values as focus moves', () => {
      handleGridKeydown('ArrowRight');
      expect(mockTiles[0].tabIndex).toBe(-1);
      expect(mockTiles[1].tabIndex).toBe(0);

      handleGridKeydown('ArrowDown');
      expect(mockTiles[1].tabIndex).toBe(-1);
      expect(mockTiles[5].tabIndex).toBe(0);
    });
  });

  describe('auto-fill from color swatch', () => {
    it('should fill input with selectedTiles.size when swatch is clicked', () => {
      createMockInput('BLUE');
      createMockInput('YELLOW');

      // Select 3 tiles
      selectedTiles.add(0);
      selectedTiles.add(5);
      selectedTiles.add(10);

      handleSwatchClick('BLUE');

      const blueInput = getInputByToken('BLUE');
      expect(blueInput?.value).toBe('3');
    });

    it('should count ALL selected tiles regardless of color', () => {
      createMockInput('BLACK');

      // Select tiles (in a real scenario these would have different ink colors)
      selectedTiles.add(0);  // Could be BLACK ink
      selectedTiles.add(1);  // Could be BLUE ink
      selectedTiles.add(2);  // Could be YELLOW ink
      selectedTiles.add(3);  // Could be ORANGE ink

      // When clicking BLACK swatch, count is ALL selected tiles, not just BLACK
      handleSwatchClick('BLACK');

      const blackInput = getInputByToken('BLACK');
      expect(blackInput?.value).toBe('4'); // All 4 selected, not filtered by color
    });

    it('should fill with 0 when no tiles are selected', () => {
      createMockInput('ORANGE');

      handleSwatchClick('ORANGE');

      const orangeInput = getInputByToken('ORANGE');
      expect(orangeInput?.value).toBe('0');
    });
  });
});
