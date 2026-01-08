/**
 * Tests for Tile Selection Logic
 *
 * These tests verify the core selection state management for the counting tiles feature:
 * 1. selectedTiles Set initializes empty
 * 2. Clicking a tile adds its index to selectedTiles
 * 3. Clicking a selected tile removes it from selectedTiles (toggle behavior)
 * 4. selectedTiles.clear() empties all selections
 * 5. generatePuzzle() clears all selections
 */

import { describe, it, expect, beforeEach } from 'vitest';

// Simulated tile selection state and functions (mirrors puzzle.html implementation)
let selectedTiles: Set<number>;
let soundEnabled: boolean;

// Mock puzzle data for testing
let currentPuzzle: { word: string; inkColor: string }[] | null;

function validateSoundEnabled(value: string | null): boolean {
  return value === 'true';
}

function initializeSelectionState() {
  selectedTiles = new Set<number>();
  soundEnabled = validateSoundEnabled(null); // Default to false
}

function toggleTileSelection(index: number): void {
  if (selectedTiles.has(index)) {
    selectedTiles.delete(index);
  } else {
    selectedTiles.add(index);
  }
}

function clearAllSelections(): void {
  selectedTiles.clear();
}

// Simulates the selection clearing that occurs in generatePuzzle()
function generatePuzzleSelectionReset(): void {
  selectedTiles.clear();
}

describe('Tile Selection Logic', () => {
  beforeEach(() => {
    initializeSelectionState();
    currentPuzzle = [
      { word: 'BLUE', inkColor: 'BLACK' },
      { word: 'YELLOW', inkColor: 'BLUE' },
      { word: 'BLACK', inkColor: 'YELLOW' },
      { word: 'ORANGE', inkColor: 'ORANGE' },
    ];
  });

  describe('selectedTiles Set initialization', () => {
    it('should initialize selectedTiles as an empty Set', () => {
      expect(selectedTiles).toBeInstanceOf(Set);
      expect(selectedTiles.size).toBe(0);
    });

    it('should initialize soundEnabled as false by default', () => {
      expect(soundEnabled).toBe(false);
    });
  });

  describe('tile selection toggle behavior', () => {
    it('should add tile index to selectedTiles when clicking unselected tile', () => {
      expect(selectedTiles.has(0)).toBe(false);
      toggleTileSelection(0);
      expect(selectedTiles.has(0)).toBe(true);
      expect(selectedTiles.size).toBe(1);
    });

    it('should remove tile index from selectedTiles when clicking selected tile', () => {
      toggleTileSelection(0);
      expect(selectedTiles.has(0)).toBe(true);
      toggleTileSelection(0);
      expect(selectedTiles.has(0)).toBe(false);
      expect(selectedTiles.size).toBe(0);
    });

    it('should support selecting multiple tiles', () => {
      toggleTileSelection(0);
      toggleTileSelection(2);
      toggleTileSelection(3);
      expect(selectedTiles.size).toBe(3);
      expect(selectedTiles.has(0)).toBe(true);
      expect(selectedTiles.has(1)).toBe(false);
      expect(selectedTiles.has(2)).toBe(true);
      expect(selectedTiles.has(3)).toBe(true);
    });
  });

  describe('clearing selections', () => {
    it('should empty all selections when selectedTiles.clear() is called', () => {
      toggleTileSelection(0);
      toggleTileSelection(1);
      toggleTileSelection(2);
      expect(selectedTiles.size).toBe(3);

      selectedTiles.clear();
      expect(selectedTiles.size).toBe(0);
      expect(selectedTiles.has(0)).toBe(false);
      expect(selectedTiles.has(1)).toBe(false);
      expect(selectedTiles.has(2)).toBe(false);
    });

    it('should clear all selections when generatePuzzle() is called', () => {
      toggleTileSelection(0);
      toggleTileSelection(1);
      expect(selectedTiles.size).toBe(2);

      generatePuzzleSelectionReset();
      expect(selectedTiles.size).toBe(0);
    });
  });

  describe('soundEnabled validation', () => {
    it('should return false for null localStorage value', () => {
      expect(validateSoundEnabled(null)).toBe(false);
    });

    it('should return true only for "true" string', () => {
      expect(validateSoundEnabled('true')).toBe(true);
      expect(validateSoundEnabled('false')).toBe(false);
      expect(validateSoundEnabled('')).toBe(false);
      expect(validateSoundEnabled('1')).toBe(false);
    });
  });
});
