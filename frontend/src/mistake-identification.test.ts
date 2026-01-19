/**
 * Tests for Mistake Identification Feature - Core Logic
 *
 * These tests verify the core state management and algorithms for the mistake identification feature:
 * 1. Discrepancy detection (user count vs correct count)
 * 2. Identification mode state transitions (enter, exit, color cycling)
 * 3. Tile selection storage during identification flow
 * 4. Stroop effect detection for adjacent tiles
 */

import { describe, it, expect, beforeEach } from 'vitest';

// ===========================================
// SIMULATED STATE AND TYPES
// ===========================================

interface DiscrepancyData {
  userCount: number;
  correctCount: number;
  difference: number;
}

interface IdentificationStep {
  currentColor: string | null;
  queueIndex: number;
}

interface MistakeAnalysisItem {
  correct: boolean;
  incorrect: boolean;
  stroopInfluenced: boolean;
}

interface PuzzleCell {
  word: string;
  inkColor: string;
}

// State variables mirroring puzzle.html implementation
let identificationMode: boolean;
let identificationStep: IdentificationStep;
let discrepancyData: Map<string, DiscrepancyData>;
let colorQueue: string[];
let identificationResults: Map<string, Set<number>>;
let mistakeAnalysis: Map<number, MistakeAnalysisItem>;
let selectedTiles: Set<number>;
let currentGridSize: number;
let currentPuzzle: PuzzleCell[];
let correctAnswers: Record<string, number>;

// ===========================================
// CORE FUNCTIONS
// ===========================================

/**
 * Initialize identification state (called at start and on reset)
 */
function initializeIdentificationState(): void {
  identificationMode = false;
  identificationStep = { currentColor: null, queueIndex: -1 };
  discrepancyData = new Map();
  colorQueue = [];
  identificationResults = new Map();
  mistakeAnalysis = new Map();
}

/**
 * Calculate discrepancies between user answers and correct answers
 * @param userAnswers - Map of color tokens to user-entered counts
 * @param correctAnswersObj - Map of color tokens to correct counts
 * @returns Array of color tokens that have discrepancies (for the color queue)
 */
function calculateDiscrepancies(
  userAnswers: Record<string, number>,
  correctAnswersObj: Record<string, number>
): string[] {
  discrepancyData.clear();
  const colorsWithDiscrepancies: string[] = [];

  // Process all colors that appear in either user answers or correct answers
  const allColors = new Set([
    ...Object.keys(userAnswers),
    ...Object.keys(correctAnswersObj)
  ]);

  allColors.forEach(token => {
    const userCount = userAnswers[token] ?? 0;
    const correctCount = correctAnswersObj[token] ?? 0;
    const difference = userCount - correctCount;

    // Store discrepancy data for all colors
    discrepancyData.set(token, {
      userCount,
      correctCount,
      difference
    });

    // Only add to queue if there's a discrepancy (non-zero difference)
    if (difference !== 0) {
      colorsWithDiscrepancies.push(token);
    }
  });

  return colorsWithDiscrepancies;
}

/**
 * Enter identification mode with the calculated discrepancies
 * @param discrepancyColors - Array of color tokens with discrepancies
 */
function enterIdentificationMode(discrepancyColors: string[]): void {
  if (discrepancyColors.length === 0) {
    return; // No discrepancies, don't enter identification mode
  }

  identificationMode = true;
  colorQueue = [...discrepancyColors];
  identificationStep = {
    currentColor: colorQueue[0],
    queueIndex: 0
  };

  // Initialize empty sets for each color in the queue
  colorQueue.forEach(color => {
    identificationResults.set(color, new Set());
  });
}

/**
 * Advance to the next color in the identification queue
 * Stores current selections and moves to next color
 * @returns true if advanced to next color, false if queue is complete
 */
function advanceToNextColor(): boolean {
  if (!identificationMode || identificationStep.queueIndex < 0) {
    return false;
  }

  // Store current selections for the current color
  const currentColor = identificationStep.currentColor;
  if (currentColor) {
    identificationResults.set(currentColor, new Set(selectedTiles));
  }

  // Clear selections for next color
  selectedTiles.clear();

  // Advance to next color
  const nextIndex = identificationStep.queueIndex + 1;
  if (nextIndex >= colorQueue.length) {
    // Queue complete
    identificationStep = { currentColor: null, queueIndex: -1 };
    return false;
  }

  identificationStep = {
    currentColor: colorQueue[nextIndex],
    queueIndex: nextIndex
  };
  return true;
}

/**
 * Exit identification mode and reset state
 */
function exitIdentificationMode(): void {
  identificationMode = false;
  identificationStep = { currentColor: null, queueIndex: -1 };
  colorQueue = [];
  identificationResults.clear();
  mistakeAnalysis.clear();
  selectedTiles.clear();
}

/**
 * Reset all identification state (called on new puzzle generation)
 * This extends the existing clearAllSelections behavior
 */
function resetIdentificationState(): void {
  initializeIdentificationState();
  selectedTiles.clear();
}

/**
 * Get orthogonally adjacent tile indices for a given tile
 * @param tileIndex - The index of the tile to find neighbors for
 * @param gridSize - The size of the grid (NxN)
 * @returns Array of valid adjacent tile indices (up, down, left, right)
 */
function getAdjacentTileIndices(tileIndex: number, gridSize: number): number[] {
  const row = Math.floor(tileIndex / gridSize);
  const col = tileIndex % gridSize;
  const adjacent: number[] = [];

  // Up
  if (row > 0) {
    adjacent.push(tileIndex - gridSize);
  }
  // Down
  if (row < gridSize - 1) {
    adjacent.push(tileIndex + gridSize);
  }
  // Left
  if (col > 0) {
    adjacent.push(tileIndex - 1);
  }
  // Right
  if (col < gridSize - 1) {
    adjacent.push(tileIndex + 1);
  }

  return adjacent;
}

/**
 * Analyze if Stroop interference likely occurred for a tile
 * @param tileIndex - Index of the tile to analyze
 * @param perceivedColor - The color the user thought the tile was
 * @param puzzle - The current puzzle array
 * @param gridSize - The grid size
 * @returns true if any adjacent tile's word text matches the perceived color
 */
function analyzeStroopInfluence(
  tileIndex: number,
  perceivedColor: string,
  puzzle: PuzzleCell[],
  gridSize: number
): boolean {
  const adjacentIndices = getAdjacentTileIndices(tileIndex, gridSize);

  // Check if any adjacent tile's word matches the user's perceived color
  for (const adjIndex of adjacentIndices) {
    if (adjIndex >= 0 && adjIndex < puzzle.length) {
      const adjacentTile = puzzle[adjIndex];
      if (adjacentTile.word === perceivedColor) {
        return true;
      }
    }
  }

  return false;
}

// ===========================================
// TEST SETUP
// ===========================================

function setupTestState(): void {
  initializeIdentificationState();
  selectedTiles = new Set();
  currentGridSize = 4;

  // Create a 4x4 test puzzle with known values
  // Grid layout (4x4, indices 0-15):
  //  0  1  2  3
  //  4  5  6  7
  //  8  9 10 11
  // 12 13 14 15
  currentPuzzle = [
    { word: 'BLUE', inkColor: 'BLACK' },    // 0
    { word: 'YELLOW', inkColor: 'BLUE' },   // 1
    { word: 'BLACK', inkColor: 'YELLOW' },  // 2
    { word: 'ORANGE', inkColor: 'ORANGE' }, // 3 - congruent
    { word: 'BLACK', inkColor: 'BLUE' },    // 4
    { word: 'BLUE', inkColor: 'YELLOW' },   // 5 - word is BLUE
    { word: 'YELLOW', inkColor: 'BLACK' },  // 6
    { word: 'ORANGE', inkColor: 'BLUE' },   // 7
    { word: 'YELLOW', inkColor: 'ORANGE' }, // 8
    { word: 'BLUE', inkColor: 'BLACK' },    // 9 - word is BLUE (adjacent to 5)
    { word: 'BLACK', inkColor: 'YELLOW' },  // 10
    { word: 'ORANGE', inkColor: 'ORANGE' }, // 11 - congruent
    { word: 'BLUE', inkColor: 'YELLOW' },   // 12
    { word: 'YELLOW', inkColor: 'BLUE' },   // 13
    { word: 'BLACK', inkColor: 'ORANGE' },  // 14
    { word: 'ORANGE', inkColor: 'BLACK' },  // 15
  ];

  // Correct counts based on ink colors in the puzzle:
  // BLACK: 4 (indices: 0, 6, 9, 15)
  // BLUE: 4 (indices: 1, 4, 7, 13)
  // YELLOW: 4 (indices: 2, 5, 10, 12)
  // ORANGE: 4 (indices: 3, 8, 11, 14)
  correctAnswers = {
    BLACK: 4,
    BLUE: 4,
    YELLOW: 4,
    ORANGE: 4
  };
}

// ===========================================
// TESTS
// ===========================================

describe('Mistake Identification - Core Logic', () => {
  beforeEach(() => {
    setupTestState();
  });

  describe('Discrepancy Detection', () => {
    it('should detect when user count differs from correct count', () => {
      const userAnswers = {
        BLACK: 3,   // Under-counted by 1
        BLUE: 5,    // Over-counted by 1
        YELLOW: 4,  // Correct
        ORANGE: 4   // Correct
      };

      const discrepancies = calculateDiscrepancies(userAnswers, correctAnswers);

      expect(discrepancies).toContain('BLACK');
      expect(discrepancies).toContain('BLUE');
      expect(discrepancies).not.toContain('YELLOW');
      expect(discrepancies).not.toContain('ORANGE');
      expect(discrepancies.length).toBe(2);

      // Verify discrepancy data is stored correctly
      expect(discrepancyData.get('BLACK')?.difference).toBe(-1);
      expect(discrepancyData.get('BLUE')?.difference).toBe(1);
      expect(discrepancyData.get('YELLOW')?.difference).toBe(0);
    });

    it('should return empty array when all counts are correct', () => {
      const userAnswers = {
        BLACK: 4,
        BLUE: 4,
        YELLOW: 4,
        ORANGE: 4
      };

      const discrepancies = calculateDiscrepancies(userAnswers, correctAnswers);

      expect(discrepancies.length).toBe(0);
    });

    it('should handle missing user answers as zero', () => {
      const userAnswers = {
        BLACK: 4,
        BLUE: 4
        // YELLOW and ORANGE not provided
      };

      const discrepancies = calculateDiscrepancies(userAnswers, correctAnswers);

      // YELLOW and ORANGE should show as under-counted (0 vs 4)
      expect(discrepancies).toContain('YELLOW');
      expect(discrepancies).toContain('ORANGE');
      expect(discrepancyData.get('YELLOW')?.userCount).toBe(0);
      expect(discrepancyData.get('YELLOW')?.difference).toBe(-4);
    });
  });

  describe('Identification Mode State Transitions', () => {
    it('should enter identification mode with correct initial state', () => {
      const userAnswers = { BLACK: 3, BLUE: 5, YELLOW: 4, ORANGE: 4 };
      const discrepancies = calculateDiscrepancies(userAnswers, correctAnswers);

      enterIdentificationMode(discrepancies);

      expect(identificationMode).toBe(true);
      expect(colorQueue).toEqual(['BLACK', 'BLUE']);
      expect(identificationStep.currentColor).toBe('BLACK');
      expect(identificationStep.queueIndex).toBe(0);
    });

    it('should not enter identification mode when no discrepancies exist', () => {
      enterIdentificationMode([]);

      expect(identificationMode).toBe(false);
      expect(colorQueue.length).toBe(0);
    });

    it('should advance through color queue correctly', () => {
      enterIdentificationMode(['BLACK', 'BLUE', 'YELLOW']);

      // Select some tiles for BLACK
      selectedTiles.add(0);
      selectedTiles.add(6);

      // Advance to BLUE
      const hasMore = advanceToNextColor();

      expect(hasMore).toBe(true);
      expect(identificationStep.currentColor).toBe('BLUE');
      expect(identificationStep.queueIndex).toBe(1);
      expect(identificationResults.get('BLACK')?.size).toBe(2);
      expect(selectedTiles.size).toBe(0); // Cleared for next color
    });

    it('should return false when advancing past last color', () => {
      enterIdentificationMode(['BLACK']);
      selectedTiles.add(0);

      const hasMore = advanceToNextColor();

      expect(hasMore).toBe(false);
      expect(identificationStep.currentColor).toBe(null);
      expect(identificationStep.queueIndex).toBe(-1);
    });

    it('should exit identification mode and clear all state', () => {
      enterIdentificationMode(['BLACK', 'BLUE']);
      selectedTiles.add(0);
      selectedTiles.add(1);
      advanceToNextColor();

      exitIdentificationMode();

      expect(identificationMode).toBe(false);
      expect(colorQueue.length).toBe(0);
      expect(identificationResults.size).toBe(0);
      expect(selectedTiles.size).toBe(0);
    });
  });

  describe('Tile Selection Storage', () => {
    it('should store tile selections per color in identification results', () => {
      enterIdentificationMode(['BLACK', 'BLUE']);

      // Select tiles for BLACK
      selectedTiles.add(0);
      selectedTiles.add(6);
      selectedTiles.add(9);
      advanceToNextColor();

      // Select tiles for BLUE
      selectedTiles.add(1);
      selectedTiles.add(4);
      advanceToNextColor();

      // Verify stored results
      const blackResults = identificationResults.get('BLACK');
      const blueResults = identificationResults.get('BLUE');

      expect(blackResults?.has(0)).toBe(true);
      expect(blackResults?.has(6)).toBe(true);
      expect(blackResults?.has(9)).toBe(true);
      expect(blackResults?.size).toBe(3);

      expect(blueResults?.has(1)).toBe(true);
      expect(blueResults?.has(4)).toBe(true);
      expect(blueResults?.size).toBe(2);
    });
  });

  describe('Stroop Effect Detection', () => {
    it('should detect Stroop influence when adjacent tile word matches perceived color', () => {
      // Tile 6 (inkColor: BLACK), adjacent to tile 5 which has word "BLUE"
      // If user thought tile 6 was BLUE (when it's actually BLACK),
      // and tile 5's word is "BLUE", that's Stroop interference
      const isStroopInfluenced = analyzeStroopInfluence(
        6,      // tile index
        'BLUE', // user thought it was BLUE
        currentPuzzle,
        currentGridSize
      );

      expect(isStroopInfluenced).toBe(true);
    });

    it('should not detect Stroop influence when no adjacent word matches', () => {
      // Tile 0 is at corner, adjacent to tiles 1 (word: YELLOW) and 4 (word: BLACK)
      // If user thought it was ORANGE, neither adjacent word matches
      const isStroopInfluenced = analyzeStroopInfluence(
        0,
        'ORANGE',
        currentPuzzle,
        currentGridSize
      );

      expect(isStroopInfluenced).toBe(false);
    });

    it('should correctly identify adjacent tiles for corner positions', () => {
      // Top-left corner (index 0) should only have 2 adjacent tiles
      const adjacentTo0 = getAdjacentTileIndices(0, 4);
      expect(adjacentTo0).toContain(1);  // right
      expect(adjacentTo0).toContain(4);  // down
      expect(adjacentTo0.length).toBe(2);

      // Bottom-right corner (index 15) should only have 2 adjacent tiles
      const adjacentTo15 = getAdjacentTileIndices(15, 4);
      expect(adjacentTo15).toContain(14); // left
      expect(adjacentTo15).toContain(11); // up
      expect(adjacentTo15.length).toBe(2);
    });

    it('should correctly identify adjacent tiles for center positions', () => {
      // Center tile (index 5) should have 4 adjacent tiles
      const adjacentTo5 = getAdjacentTileIndices(5, 4);
      expect(adjacentTo5).toContain(1);  // up
      expect(adjacentTo5).toContain(9);  // down
      expect(adjacentTo5).toContain(4);  // left
      expect(adjacentTo5).toContain(6);  // right
      expect(adjacentTo5.length).toBe(4);
    });
  });

  describe('State Reset', () => {
    it('should clear all identification state on reset', () => {
      // Setup some state
      enterIdentificationMode(['BLACK', 'BLUE']);
      selectedTiles.add(0);
      advanceToNextColor();
      selectedTiles.add(1);

      // Reset
      resetIdentificationState();

      expect(identificationMode).toBe(false);
      expect(identificationStep.currentColor).toBe(null);
      expect(colorQueue.length).toBe(0);
      expect(discrepancyData.size).toBe(0);
      expect(identificationResults.size).toBe(0);
      expect(mistakeAnalysis.size).toBe(0);
      expect(selectedTiles.size).toBe(0);
    });
  });
});
