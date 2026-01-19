/**
 * Tests for Mistake Identification Feature - UI Components
 *
 * These tests verify the UI layer for the mistake identification feature:
 * 1. "Identify Mistakes" button visibility (shows only when discrepancies exist)
 * 2. Identification prompt display (correct color swatch, localized label)
 * 3. "Done" button advances to next color or completes flow
 * 4. Exit button returns to normal puzzle view
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

// State variables mirroring puzzle.html implementation
let identificationMode: boolean;
let identificationStep: IdentificationStep;
let discrepancyData: Map<string, DiscrepancyData>;
let colorQueue: string[];
let identificationResults: Map<string, Set<number>>;
let selectedTiles: Set<number>;
let hasChecked: boolean;
let currentLanguage: string;

// Mock color data
const colorsJson: Record<string, string> = {
  BLACK: '#0D0D0D',
  BLUE: '#0062E6',
  YELLOW: '#D9B000',
  ORANGE: '#CC5200',
};

const colorLabelsJson: Record<string, Record<string, string>> = {
  BLACK: { english: 'Black', 'zh-TW': '黑', spanish: 'Negro', vietnamese: 'Den' },
  BLUE: { english: 'Blue', 'zh-TW': '藍', spanish: 'Azul', vietnamese: 'Xanh duong' },
  YELLOW: { english: 'Yellow', 'zh-TW': '黃', spanish: 'Amarillo', vietnamese: 'Vang' },
  ORANGE: { english: 'Orange', 'zh-TW': '橙', spanish: 'Naranja', vietnamese: 'Cam' },
};

// Mock UI text data
const uiTextJson: Record<string, Record<string, string>> = {
  identify_mistakes_btn: {
    english: 'Identify Mistakes',
    'zh-TW': '識別錯誤',
    spanish: 'Identificar Errores',
    vietnamese: 'Xac dinh loi',
  },
  identification_prompt: {
    english: 'Select the tiles you thought were {color}',
    'zh-TW': '選擇您認為是{color}的方塊',
    spanish: 'Selecciona las celdas que pensaste que eran {color}',
    vietnamese: 'Chon cac o ban nghi la {color}',
  },
  identification_done_btn: {
    english: 'Done',
    'zh-TW': '完成',
    spanish: 'Listo',
    vietnamese: 'Xong',
  },
  identification_cancel_btn: {
    english: 'Cancel',
    'zh-TW': '取消',
    spanish: 'Cancelar',
    vietnamese: 'Huy',
  },
  identification_next_color: {
    english: 'Next: {color}',
    'zh-TW': '下一個：{color}',
    spanish: 'Siguiente: {color}',
    vietnamese: 'Tiep theo: {color}',
  },
};

// ===========================================
// CORE FUNCTIONS (from puzzle.html)
// ===========================================

function initializeIdentificationState(): void {
  identificationMode = false;
  identificationStep = { currentColor: null, queueIndex: -1 };
  discrepancyData = new Map();
  colorQueue = [];
  identificationResults = new Map();
}

function calculateDiscrepancies(
  userAnswers: Record<string, number>,
  correctAnswers: Record<string, number>
): string[] {
  discrepancyData.clear();
  const colorsWithDiscrepancies: string[] = [];

  const allColors = new Set([
    ...Object.keys(userAnswers),
    ...Object.keys(correctAnswers),
  ]);

  allColors.forEach((token) => {
    const userCount = userAnswers[token] ?? 0;
    const correctCount = correctAnswers[token] ?? 0;
    const difference = userCount - correctCount;

    discrepancyData.set(token, {
      userCount,
      correctCount,
      difference,
    });

    if (difference !== 0) {
      colorsWithDiscrepancies.push(token);
    }
  });

  return colorsWithDiscrepancies;
}

function enterIdentificationMode(discrepancyColors: string[]): void {
  if (discrepancyColors.length === 0) {
    return;
  }

  identificationMode = true;
  colorQueue = [...discrepancyColors];
  identificationStep = {
    currentColor: colorQueue[0],
    queueIndex: 0,
  };

  colorQueue.forEach((color) => {
    identificationResults.set(color, new Set());
  });
}

function advanceToNextColor(): boolean {
  if (!identificationMode || identificationStep.queueIndex < 0) {
    return false;
  }

  const currentColor = identificationStep.currentColor;
  if (currentColor) {
    identificationResults.set(currentColor, new Set(selectedTiles));
  }

  selectedTiles.clear();

  const nextIndex = identificationStep.queueIndex + 1;
  if (nextIndex >= colorQueue.length) {
    identificationStep = { currentColor: null, queueIndex: -1 };
    return false;
  }

  identificationStep = {
    currentColor: colorQueue[nextIndex],
    queueIndex: nextIndex,
  };
  return true;
}

function exitIdentificationMode(): void {
  identificationMode = false;
  identificationStep = { currentColor: null, queueIndex: -1 };
  colorQueue = [];
  identificationResults.clear();
  selectedTiles.clear();
}

// ===========================================
// UI FUNCTIONS
// ===========================================

/**
 * Get UI text for the current language
 */
function getUIText(key: string): string {
  if (uiTextJson[key] && uiTextJson[key][currentLanguage]) {
    return uiTextJson[key][currentLanguage];
  }
  if (uiTextJson[key] && uiTextJson[key]['english']) {
    return uiTextJson[key]['english'];
  }
  return key;
}

/**
 * Determine if the "Identify Mistakes" button should be visible
 * Button shows only when hasChecked is true AND discrepancies exist
 */
function shouldShowIdentifyMistakesButton(): boolean {
  if (!hasChecked) {
    return false;
  }

  // Check if there are any discrepancies
  for (const [, data] of discrepancyData) {
    if (data.difference !== 0) {
      return true;
    }
  }

  return false;
}

/**
 * Get the identification prompt text for the current color
 * Formats the prompt with the localized color label
 */
function getIdentificationPromptText(): string {
  if (!identificationMode || !identificationStep.currentColor) {
    return '';
  }

  const colorToken = identificationStep.currentColor;
  const colorLabel = colorLabelsJson[colorToken]?.[currentLanguage] ?? colorToken;
  const promptTemplate = getUIText('identification_prompt');

  return promptTemplate.replace('{color}', colorLabel);
}

/**
 * Get the color swatch hex value for the current identification color
 */
function getIdentificationColorSwatch(): string {
  if (!identificationMode || !identificationStep.currentColor) {
    return '';
  }

  return colorsJson[identificationStep.currentColor] ?? '';
}

/**
 * Get the "Next" indicator text showing the next color in queue
 * Returns empty string if no more colors after current
 */
function getNextColorIndicator(): string {
  if (!identificationMode || identificationStep.queueIndex < 0) {
    return '';
  }

  const nextIndex = identificationStep.queueIndex + 1;
  if (nextIndex >= colorQueue.length) {
    return ''; // No more colors
  }

  const nextColor = colorQueue[nextIndex];
  const colorLabel = colorLabelsJson[nextColor]?.[currentLanguage] ?? nextColor;
  const template = getUIText('identification_next_color');

  return template.replace('{color}', colorLabel);
}

/**
 * Handle "Done" button click in identification mode
 * Returns true if flow continues, false if flow is complete
 */
function handleDoneClick(): boolean {
  if (!identificationMode) {
    return false;
  }

  return advanceToNextColor();
}

/**
 * Handle "Cancel" button click in identification mode
 * Exits identification mode and restores normal view
 */
function handleCancelClick(): void {
  exitIdentificationMode();
}

/**
 * Check if identification prompt panel should be visible
 */
function isIdentificationPromptVisible(): boolean {
  return identificationMode && identificationStep.currentColor !== null;
}

// ===========================================
// TEST SETUP
// ===========================================

function setupUITestState(): void {
  initializeIdentificationState();
  selectedTiles = new Set();
  hasChecked = false;
  currentLanguage = 'english';
}

// ===========================================
// TESTS
// ===========================================

describe('Mistake Identification - UI Components', () => {
  beforeEach(() => {
    setupUITestState();
  });

  describe('Identify Mistakes Button Visibility', () => {
    it('should not show button when answers have not been checked', () => {
      hasChecked = false;

      expect(shouldShowIdentifyMistakesButton()).toBe(false);
    });

    it('should not show button when all answers are correct', () => {
      hasChecked = true;
      const correctAnswers = { BLACK: 4, BLUE: 4 };
      calculateDiscrepancies({ BLACK: 4, BLUE: 4 }, correctAnswers);

      expect(shouldShowIdentifyMistakesButton()).toBe(false);
    });

    it('should show button when hasChecked is true AND discrepancies exist', () => {
      hasChecked = true;
      const correctAnswers = { BLACK: 4, BLUE: 4 };
      calculateDiscrepancies({ BLACK: 3, BLUE: 5 }, correctAnswers);

      expect(shouldShowIdentifyMistakesButton()).toBe(true);
    });

    it('should hide button when user over-counts one color and under-counts another', () => {
      hasChecked = true;
      const correctAnswers = { BLACK: 4, BLUE: 4 };
      // User counted BLACK as 5 and BLUE as 3
      calculateDiscrepancies({ BLACK: 5, BLUE: 3 }, correctAnswers);

      // Button should still show because there ARE discrepancies
      expect(shouldShowIdentifyMistakesButton()).toBe(true);
    });
  });

  describe('Identification Prompt Display', () => {
    it('should display correct prompt text with localized color label', () => {
      const correctAnswers = { BLACK: 4, BLUE: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3, BLUE: 5 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      const promptText = getIdentificationPromptText();

      expect(promptText).toBe('Select the tiles you thought were Black');
    });

    it('should return correct color swatch hex value', () => {
      const correctAnswers = { BLACK: 4, BLUE: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3, BLUE: 5 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      const swatchColor = getIdentificationColorSwatch();

      expect(swatchColor).toBe('#0D0D0D'); // BLACK hex
    });

    it('should display prompt in current language (Chinese)', () => {
      currentLanguage = 'zh-TW';
      const correctAnswers = { BLACK: 4, BLUE: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3, BLUE: 5 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      const promptText = getIdentificationPromptText();

      expect(promptText).toBe('選擇您認為是黑的方塊');
    });

    it('should show next color indicator when more colors remain', () => {
      const correctAnswers = { BLACK: 4, BLUE: 4, YELLOW: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3, BLUE: 5, YELLOW: 3 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      const nextIndicator = getNextColorIndicator();

      expect(nextIndicator).toBe('Next: Blue');
    });

    it('should return empty next indicator when on last color', () => {
      const correctAnswers = { BLACK: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      const nextIndicator = getNextColorIndicator();

      expect(nextIndicator).toBe('');
    });
  });

  describe('Done Button Functionality', () => {
    it('should advance to next color when clicked', () => {
      const correctAnswers = { BLACK: 4, BLUE: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3, BLUE: 5 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      expect(identificationStep.currentColor).toBe('BLACK');

      selectedTiles.add(0);
      selectedTiles.add(6);
      const hasMore = handleDoneClick();

      expect(hasMore).toBe(true);
      expect(identificationStep.currentColor).toBe('BLUE');
      expect(identificationResults.get('BLACK')?.size).toBe(2);
    });

    it('should return false when completing final color', () => {
      const correctAnswers = { BLACK: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      selectedTiles.add(0);
      const hasMore = handleDoneClick();

      expect(hasMore).toBe(false);
      expect(identificationStep.currentColor).toBe(null);
    });

    it('should store tile selections before advancing', () => {
      const correctAnswers = { BLACK: 4, BLUE: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3, BLUE: 5 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      // Select tiles for BLACK
      selectedTiles.add(0);
      selectedTiles.add(6);
      selectedTiles.add(9);
      handleDoneClick();

      const blackSelections = identificationResults.get('BLACK');
      expect(blackSelections?.has(0)).toBe(true);
      expect(blackSelections?.has(6)).toBe(true);
      expect(blackSelections?.has(9)).toBe(true);
    });
  });

  describe('Cancel Button Functionality', () => {
    it('should exit identification mode when clicked', () => {
      const correctAnswers = { BLACK: 4, BLUE: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3, BLUE: 5 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      expect(identificationMode).toBe(true);

      handleCancelClick();

      expect(identificationMode).toBe(false);
      expect(identificationStep.currentColor).toBe(null);
      expect(colorQueue.length).toBe(0);
    });

    it('should clear all state including selected tiles', () => {
      const correctAnswers = { BLACK: 4, BLUE: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3, BLUE: 5 }, correctAnswers);
      enterIdentificationMode(discrepancies);
      selectedTiles.add(0);
      selectedTiles.add(1);

      handleCancelClick();

      expect(selectedTiles.size).toBe(0);
      expect(identificationResults.size).toBe(0);
    });

    it('should return to normal view state', () => {
      const correctAnswers = { BLACK: 4, BLUE: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3, BLUE: 5 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      handleCancelClick();

      expect(isIdentificationPromptVisible()).toBe(false);
    });
  });

  describe('Identification Mode Toggle', () => {
    it('should show identification prompt when in identification mode', () => {
      const correctAnswers = { BLACK: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      expect(isIdentificationPromptVisible()).toBe(true);
    });

    it('should hide identification prompt when not in identification mode', () => {
      expect(isIdentificationPromptVisible()).toBe(false);
    });

    it('should hide prompt after flow completes', () => {
      const correctAnswers = { BLACK: 4 };
      const discrepancies = calculateDiscrepancies({ BLACK: 3 }, correctAnswers);
      enterIdentificationMode(discrepancies);

      handleDoneClick(); // Complete the single color

      // After completing, queueIndex should be -1 and currentColor null
      expect(isIdentificationPromptVisible()).toBe(false);
    });
  });
});
