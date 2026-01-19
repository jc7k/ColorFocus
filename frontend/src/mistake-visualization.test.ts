/**
 * Tests for Mistake Identification Feature - Visualization and Summary
 *
 * These tests verify the visualization layer for the mistake identification feature:
 * 1. Correct tile identification styling (correctly identified tiles)
 * 2. Incorrect tile identification styling (user thought wrong color)
 * 3. Stroop influence indicator styling
 * 4. Summary panel displays correct counts
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

interface TileAnalysisResult {
  tileIndex: number;
  isCorrect: boolean;
  isIncorrect: boolean;
  isStroopInfluenced: boolean;
  perceivedColor: string;
  actualColor: string;
}

interface SummaryData {
  totalMistakes: number;
  stroopInfluencedCount: number;
  nonStroopMistakes: number;
  puzzleMetadata: {
    seed: number;
    gridSize: number;
    language: string;
    difficulty: string;
  };
}

interface PuzzleCell {
  word: string;
  inkColor: string;
}

// State variables
let identificationMode: boolean;
let identificationStep: IdentificationStep;
let discrepancyData: Map<string, DiscrepancyData>;
let colorQueue: string[];
let identificationResults: Map<string, Set<number>>;
let mistakeAnalysis: Map<number, TileAnalysisResult>;
let currentGridSize: number;
let currentPuzzle: PuzzleCell[];
let correctAnswers: Record<string, number>;

// ===========================================
// CORE FUNCTIONS (from puzzle.html)
// ===========================================

function initializeIdentificationState(): void {
  identificationMode = false;
  identificationStep = { currentColor: null, queueIndex: -1 };
  discrepancyData = new Map();
  colorQueue = [];
  identificationResults = new Map();
  mistakeAnalysis = new Map();
}

function getAdjacentTileIndices(tileIndex: number, gridSize: number): number[] {
  const row = Math.floor(tileIndex / gridSize);
  const col = tileIndex % gridSize;
  const adjacent: number[] = [];

  if (row > 0) adjacent.push(tileIndex - gridSize);
  if (row < gridSize - 1) adjacent.push(tileIndex + gridSize);
  if (col > 0) adjacent.push(tileIndex - 1);
  if (col < gridSize - 1) adjacent.push(tileIndex + 1);

  return adjacent;
}

function analyzeStroopInfluence(
  tileIndex: number,
  perceivedColor: string,
  puzzle: PuzzleCell[],
  gridSize: number
): boolean {
  const adjacentIndices = getAdjacentTileIndices(tileIndex, gridSize);

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
// VISUALIZATION FUNCTIONS
// ===========================================

/**
 * Analyze identification results and mark tiles with appropriate classes
 * For each tile in identificationResults, check if the tile's actual inkColor
 * matches the color the user selected it for.
 * @returns Map of tile indices to their analysis results
 */
function analyzeIdentificationResults(
  results: Map<string, Set<number>>,
  puzzle: PuzzleCell[],
  gridSize: number
): Map<number, TileAnalysisResult> {
  const analysis = new Map<number, TileAnalysisResult>();

  // Process each color and its selected tiles
  results.forEach((selectedTiles, perceivedColor) => {
    selectedTiles.forEach((tileIndex) => {
      if (tileIndex >= 0 && tileIndex < puzzle.length) {
        const tile = puzzle[tileIndex];
        const actualColor = tile.inkColor;
        const isCorrect = actualColor === perceivedColor;
        const isIncorrect = !isCorrect;

        // Check for Stroop influence on incorrect tiles
        const isStroopInfluenced = isIncorrect
          ? analyzeStroopInfluence(tileIndex, perceivedColor, puzzle, gridSize)
          : false;

        analysis.set(tileIndex, {
          tileIndex,
          isCorrect,
          isIncorrect,
          isStroopInfluenced,
          perceivedColor,
          actualColor,
        });
      }
    });
  });

  return analysis;
}

/**
 * Get CSS classes for a tile based on its analysis result
 * @returns Array of CSS class names to apply
 */
function getTileMarkingClasses(analysis: TileAnalysisResult | undefined): string[] {
  if (!analysis) return [];

  const classes: string[] = [];

  if (analysis.isCorrect) {
    classes.push('tile-correct-id');
  }

  if (analysis.isIncorrect) {
    classes.push('tile-incorrect-id');
  }

  if (analysis.isStroopInfluenced) {
    classes.push('tile-stroop-influenced');
  }

  return classes;
}

/**
 * Calculate summary data from mistake analysis
 */
function calculateSummaryData(
  analysis: Map<number, TileAnalysisResult>,
  metadata: { seed: number; gridSize: number; language: string; difficulty: string }
): SummaryData {
  let totalMistakes = 0;
  let stroopInfluencedCount = 0;

  analysis.forEach((result) => {
    if (result.isIncorrect) {
      totalMistakes++;
      if (result.isStroopInfluenced) {
        stroopInfluencedCount++;
      }
    }
  });

  return {
    totalMistakes,
    stroopInfluencedCount,
    nonStroopMistakes: totalMistakes - stroopInfluencedCount,
    puzzleMetadata: metadata,
  };
}

/**
 * Get legend items for mistake indicators
 */
function getLegendItems(): Array<{ className: string; labelKey: string }> {
  return [
    { className: 'tile-correct-id', labelKey: 'legend_correct' },
    { className: 'tile-incorrect-id', labelKey: 'legend_incorrect' },
    { className: 'tile-stroop-influenced', labelKey: 'legend_stroop' },
  ];
}

// ===========================================
// TEST SETUP
// ===========================================

function setupVisualizationTestState(): void {
  initializeIdentificationState();
  currentGridSize = 4;

  // Create a 4x4 test puzzle with known values
  // Grid layout (4x4, indices 0-15):
  //  0  1  2  3
  //  4  5  6  7
  //  8  9 10 11
  // 12 13 14 15
  //
  // For Stroop testing, we need carefully placed words:
  // - Tile 5 has word "BLUE", so tile 6 (adjacent) can be Stroop-influenced if user thinks BLUE
  // - Tile 2 has word "BLACK", so tile 1 (adjacent) would be Stroop if user thinks BLACK
  // - Tile 3 has word "ORANGE", so no adjacent tiles have misleading words for other colors
  currentPuzzle = [
    { word: 'BLUE', inkColor: 'BLACK' },    // 0 - ink BLACK
    { word: 'YELLOW', inkColor: 'BLUE' },   // 1 - ink BLUE
    { word: 'BLACK', inkColor: 'YELLOW' },  // 2 - word BLACK
    { word: 'ORANGE', inkColor: 'ORANGE' }, // 3 - congruent
    { word: 'ORANGE', inkColor: 'BLUE' },   // 4 - word ORANGE (no black nearby for stroop test)
    { word: 'BLUE', inkColor: 'YELLOW' },   // 5 - word BLUE
    { word: 'YELLOW', inkColor: 'BLACK' },  // 6 - ink BLACK, adjacent to tile 5 (word BLUE)
    { word: 'ORANGE', inkColor: 'BLUE' },   // 7
    { word: 'YELLOW', inkColor: 'ORANGE' }, // 8
    { word: 'BLUE', inkColor: 'BLACK' },    // 9 - word BLUE
    { word: 'YELLOW', inkColor: 'YELLOW' }, // 10 - word YELLOW
    { word: 'ORANGE', inkColor: 'ORANGE' }, // 11 - congruent
    { word: 'BLUE', inkColor: 'YELLOW' },   // 12
    { word: 'YELLOW', inkColor: 'BLUE' },   // 13
    { word: 'BLACK', inkColor: 'ORANGE' },  // 14
    { word: 'ORANGE', inkColor: 'BLACK' },  // 15
  ];

  correctAnswers = {
    BLACK: 4, // indices: 0, 6, 9, 15
    BLUE: 4,  // indices: 1, 4, 7, 13
    YELLOW: 4, // indices: 2, 5, 10, 12
    ORANGE: 4, // indices: 3, 8, 11, 14
  };
}

// ===========================================
// TESTS
// ===========================================

describe('Mistake Visualization and Summary', () => {
  beforeEach(() => {
    setupVisualizationTestState();
  });

  describe('Correct Tile Identification Styling', () => {
    it('should mark correctly identified tiles with tile-correct-id class', () => {
      // User correctly identifies that tile 0 is BLACK (it is BLACK)
      const results = new Map<string, Set<number>>();
      results.set('BLACK', new Set([0])); // Tile 0 ink is BLACK - correct!

      const analysis = analyzeIdentificationResults(results, currentPuzzle, currentGridSize);
      const tile0Result = analysis.get(0);

      expect(tile0Result).toBeDefined();
      expect(tile0Result?.isCorrect).toBe(true);
      expect(tile0Result?.isIncorrect).toBe(false);

      const classes = getTileMarkingClasses(tile0Result);
      expect(classes).toContain('tile-correct-id');
      expect(classes).not.toContain('tile-incorrect-id');
    });

    it('should correctly identify multiple tiles for same color', () => {
      // User identifies tiles 0, 6, 9, 15 as BLACK (all are actually BLACK)
      const results = new Map<string, Set<number>>();
      results.set('BLACK', new Set([0, 6, 9, 15]));

      const analysis = analyzeIdentificationResults(results, currentPuzzle, currentGridSize);

      expect(analysis.get(0)?.isCorrect).toBe(true);
      expect(analysis.get(6)?.isCorrect).toBe(true);
      expect(analysis.get(9)?.isCorrect).toBe(true);
      expect(analysis.get(15)?.isCorrect).toBe(true);
    });
  });

  describe('Incorrect Tile Identification Styling', () => {
    it('should mark incorrectly identified tiles with tile-incorrect-id class', () => {
      // User thinks tile 5 is BLACK, but it's actually YELLOW
      const results = new Map<string, Set<number>>();
      results.set('BLACK', new Set([5])); // Tile 5 ink is YELLOW - incorrect!

      const analysis = analyzeIdentificationResults(results, currentPuzzle, currentGridSize);
      const tile5Result = analysis.get(5);

      expect(tile5Result).toBeDefined();
      expect(tile5Result?.isCorrect).toBe(false);
      expect(tile5Result?.isIncorrect).toBe(true);

      const classes = getTileMarkingClasses(tile5Result);
      expect(classes).toContain('tile-incorrect-id');
      expect(classes).not.toContain('tile-correct-id');
    });

    it('should track perceived and actual colors for incorrect tiles', () => {
      // User thinks tile 1 is BLACK, but it's actually BLUE
      const results = new Map<string, Set<number>>();
      results.set('BLACK', new Set([1]));

      const analysis = analyzeIdentificationResults(results, currentPuzzle, currentGridSize);
      const tile1Result = analysis.get(1);

      expect(tile1Result?.perceivedColor).toBe('BLACK');
      expect(tile1Result?.actualColor).toBe('BLUE');
    });
  });

  describe('Stroop Influence Indicator Styling', () => {
    it('should add tile-stroop-influenced class when adjacent tile word matches perceived color', () => {
      // User thinks tile 6 is BLUE, but it's actually BLACK
      // Tile 5 (adjacent to tile 6) has word "BLUE" - this is Stroop interference
      const results = new Map<string, Set<number>>();
      results.set('BLUE', new Set([6])); // Tile 6 ink is BLACK, but user thinks BLUE

      const analysis = analyzeIdentificationResults(results, currentPuzzle, currentGridSize);
      const tile6Result = analysis.get(6);

      expect(tile6Result?.isIncorrect).toBe(true);
      expect(tile6Result?.isStroopInfluenced).toBe(true);

      const classes = getTileMarkingClasses(tile6Result);
      expect(classes).toContain('tile-incorrect-id');
      expect(classes).toContain('tile-stroop-influenced');
    });

    it('should not add stroop class when no adjacent word matches perceived color', () => {
      // User thinks tile 3 is BLACK, but it's ORANGE
      // Adjacent tiles are 2 (word BLACK) and 7 (word ORANGE) - wait, tile 2 has BLACK
      // Let's use a better test: tile 8 - adjacent to 4 (ORANGE), 9 (BLUE), 12 (BLUE)
      // User thinks tile 8 is BLACK, no adjacent word is BLACK
      const results = new Map<string, Set<number>>();
      results.set('BLACK', new Set([8])); // Tile 8 ink is ORANGE, user thinks BLACK

      const analysis = analyzeIdentificationResults(results, currentPuzzle, currentGridSize);
      const tile8Result = analysis.get(8);

      expect(tile8Result?.isIncorrect).toBe(true);
      expect(tile8Result?.isStroopInfluenced).toBe(false);

      const classes = getTileMarkingClasses(tile8Result);
      expect(classes).toContain('tile-incorrect-id');
      expect(classes).not.toContain('tile-stroop-influenced');
    });

    it('should not add stroop class to correctly identified tiles', () => {
      // User correctly identifies tile 0 as BLACK
      // Even though tile 0 has word "BLUE", the identification was correct
      const results = new Map<string, Set<number>>();
      results.set('BLACK', new Set([0]));

      const analysis = analyzeIdentificationResults(results, currentPuzzle, currentGridSize);
      const tile0Result = analysis.get(0);

      expect(tile0Result?.isCorrect).toBe(true);
      expect(tile0Result?.isStroopInfluenced).toBe(false);
    });
  });

  describe('Summary Panel Displays Correct Counts', () => {
    it('should calculate total mistakes correctly', () => {
      // User makes 2 mistakes: tiles 1 and 5 are identified as BLACK (but they're BLUE and YELLOW)
      // Tile 0 is BLACK (correct), tile 6 is BLACK (correct)
      const results = new Map<string, Set<number>>();
      results.set('BLACK', new Set([0, 1, 5, 6]));
      // Tile 0: ink BLACK - correct
      // Tile 1: ink BLUE - incorrect
      // Tile 5: ink YELLOW - incorrect
      // Tile 6: ink BLACK - correct

      const analysis = analyzeIdentificationResults(results, currentPuzzle, currentGridSize);
      const summary = calculateSummaryData(analysis, {
        seed: 42,
        gridSize: 4,
        language: 'english',
        difficulty: 'standard',
      });

      expect(summary.totalMistakes).toBe(2);
    });

    it('should calculate stroop-influenced count correctly', () => {
      // Tile 6: user thinks BLUE, actual BLACK, adjacent to tile 5 (word BLUE) - Stroop!
      // Tile 8: user thinks BLACK, actual ORANGE, no adjacent word BLACK - not Stroop
      const results = new Map<string, Set<number>>();
      results.set('BLUE', new Set([6]));   // Stroop-influenced mistake (adjacent tile 5 word is BLUE)
      results.set('BLACK', new Set([8]));  // Regular mistake (no adjacent BLACK word)

      const analysis = analyzeIdentificationResults(results, currentPuzzle, currentGridSize);
      const summary = calculateSummaryData(analysis, {
        seed: 42,
        gridSize: 4,
        language: 'english',
        difficulty: 'standard',
      });

      expect(summary.totalMistakes).toBe(2);
      expect(summary.stroopInfluencedCount).toBe(1);
      expect(summary.nonStroopMistakes).toBe(1);
    });

    it('should include puzzle metadata for reproducibility', () => {
      const results = new Map<string, Set<number>>();
      const analysis = analyzeIdentificationResults(results, currentPuzzle, currentGridSize);

      const metadata = { seed: 12345, gridSize: 8, language: 'spanish', difficulty: 'advanced' };
      const summary = calculateSummaryData(analysis, metadata);

      expect(summary.puzzleMetadata.seed).toBe(12345);
      expect(summary.puzzleMetadata.gridSize).toBe(8);
      expect(summary.puzzleMetadata.language).toBe('spanish');
      expect(summary.puzzleMetadata.difficulty).toBe('advanced');
    });

    it('should return zero counts when no mistakes made', () => {
      // All correct identifications
      const results = new Map<string, Set<number>>();
      results.set('BLACK', new Set([0, 6, 9, 15])); // All actually BLACK

      const analysis = analyzeIdentificationResults(results, currentPuzzle, currentGridSize);
      const summary = calculateSummaryData(analysis, {
        seed: 42,
        gridSize: 4,
        language: 'english',
        difficulty: 'standard',
      });

      expect(summary.totalMistakes).toBe(0);
      expect(summary.stroopInfluencedCount).toBe(0);
      expect(summary.nonStroopMistakes).toBe(0);
    });
  });

  describe('Legend Component', () => {
    it('should return all three legend items', () => {
      const legendItems = getLegendItems();

      expect(legendItems.length).toBe(3);
      expect(legendItems.find((item) => item.className === 'tile-correct-id')).toBeDefined();
      expect(legendItems.find((item) => item.className === 'tile-incorrect-id')).toBeDefined();
      expect(legendItems.find((item) => item.className === 'tile-stroop-influenced')).toBeDefined();
    });

    it('should include localization keys for each legend item', () => {
      const legendItems = getLegendItems();

      expect(legendItems[0].labelKey).toBe('legend_correct');
      expect(legendItems[1].labelKey).toBe('legend_incorrect');
      expect(legendItems[2].labelKey).toBe('legend_stroop');
    });
  });
});
