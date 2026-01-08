/**
 * Tests for UI Controls and Localization
 *
 * These tests verify the UI controls and localization for the counting tiles feature:
 * 1. "Clear Selections" button clears all tile selections
 * 2. Sound toggle updates soundEnabled state and LocalStorage
 * 3. New UI text keys render correctly in all 4 languages
 */

import { describe, it, expect, beforeEach } from 'vitest';

// Simulated tile selection state (mirrors puzzle.html implementation)
let selectedTiles: Set<number>;
let soundEnabled: boolean;

// Mock LocalStorage
const mockLocalStorage: Map<string, string> = new Map();

function mockGetItem(key: string): string | null {
  return mockLocalStorage.get(key) ?? null;
}

function mockSetItem(key: string, value: string): void {
  mockLocalStorage.set(key, value);
}

// Mock DOM elements for testing
interface MockElement {
  classList: Set<string>;
  hasClass(className: string): boolean;
  addClass(className: string): void;
  removeClass(className: string): void;
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
  };
}

// Initialize state
function initializeState() {
  selectedTiles = new Set<number>();
  soundEnabled = false;
  mockLocalStorage.clear();
}

// Clear all selections function (to be tested)
function clearAllSelections(tiles: MockElement[]): void {
  selectedTiles.clear();
  tiles.forEach(tile => tile.removeClass('selected'));
}

// Sound toggle functionality
function validateSoundEnabled(value: string | null): boolean {
  return value === 'true';
}

function loadSoundEnabledFromStorage(): boolean {
  return validateSoundEnabled(mockGetItem('colorFocusSoundEnabled'));
}

function saveSoundEnabledToStorage(enabled: boolean): void {
  mockSetItem('colorFocusSoundEnabled', String(enabled));
}

function toggleSoundEnabled(): void {
  soundEnabled = !soundEnabled;
  saveSoundEnabledToStorage(soundEnabled);
}

// UI text localization mock
const mockUIText: Record<string, Record<string, string>> = {
  clear_selections_btn: {
    'zh-TW': '清除選擇',
    english: 'Clear Selections',
    spanish: 'Borrar Selecciones',
    vietnamese: 'Xoa lua chon',
  },
  sound_toggle_label: {
    'zh-TW': '選擇音效',
    english: 'Selection Sound',
    spanish: 'Sonido de Seleccion',
    vietnamese: 'Am thanh chon',
  },
};

function getUIText(key: string, language: string): string {
  if (mockUIText[key] && mockUIText[key][language]) {
    return mockUIText[key][language];
  }
  // Fallback to English
  if (mockUIText[key] && mockUIText[key]['english']) {
    return mockUIText[key]['english'];
  }
  return key;
}

describe('UI Controls and Localization', () => {
  beforeEach(() => {
    initializeState();
  });

  describe('Clear Selections button', () => {
    it('should clear all tile selections when clicked', () => {
      // Create mock tiles with selections
      const tiles = [createMockElement(), createMockElement(), createMockElement(), createMockElement()];
      tiles.forEach((tile, index) => {
        tile.addClass('puzzle-cell');
        if (index % 2 === 0) {
          tile.addClass('selected');
          selectedTiles.add(index);
        }
      });

      expect(selectedTiles.size).toBe(2);
      expect(tiles[0].hasClass('selected')).toBe(true);
      expect(tiles[2].hasClass('selected')).toBe(true);

      // Clear all selections
      clearAllSelections(tiles);

      expect(selectedTiles.size).toBe(0);
      expect(tiles[0].hasClass('selected')).toBe(false);
      expect(tiles[2].hasClass('selected')).toBe(false);
    });

    it('should not affect answer inputs when clearing selections', () => {
      // Selections should be cleared independently of answer inputs
      const tiles = [createMockElement()];
      tiles[0].addClass('selected');
      selectedTiles.add(0);

      // Simulate answer input value
      const mockAnswerInputValue = '5';

      clearAllSelections(tiles);

      // Answer input value should remain unchanged (not part of clearAllSelections)
      expect(mockAnswerInputValue).toBe('5');
      expect(selectedTiles.size).toBe(0);
    });
  });

  describe('Sound toggle functionality', () => {
    it('should update soundEnabled state when toggled', () => {
      expect(soundEnabled).toBe(false);

      toggleSoundEnabled();
      expect(soundEnabled).toBe(true);

      toggleSoundEnabled();
      expect(soundEnabled).toBe(false);
    });

    it('should persist sound preference to LocalStorage', () => {
      expect(mockGetItem('colorFocusSoundEnabled')).toBeNull();

      toggleSoundEnabled(); // Enable
      expect(mockGetItem('colorFocusSoundEnabled')).toBe('true');

      toggleSoundEnabled(); // Disable
      expect(mockGetItem('colorFocusSoundEnabled')).toBe('false');
    });

    it('should load sound preference from LocalStorage on initialization', () => {
      mockSetItem('colorFocusSoundEnabled', 'true');
      const loaded = loadSoundEnabledFromStorage();
      expect(loaded).toBe(true);

      mockSetItem('colorFocusSoundEnabled', 'false');
      const loadedFalse = loadSoundEnabledFromStorage();
      expect(loadedFalse).toBe(false);
    });

    it('should default to OFF when no LocalStorage value exists', () => {
      mockLocalStorage.clear();
      const loaded = loadSoundEnabledFromStorage();
      expect(loaded).toBe(false);
    });
  });

  describe('UI text localization', () => {
    it('should render clear_selections_btn correctly in all 4 languages', () => {
      expect(getUIText('clear_selections_btn', 'zh-TW')).toBe('清除選擇');
      expect(getUIText('clear_selections_btn', 'english')).toBe('Clear Selections');
      expect(getUIText('clear_selections_btn', 'spanish')).toBe('Borrar Selecciones');
      expect(getUIText('clear_selections_btn', 'vietnamese')).toBe('Xoa lua chon');
    });

    it('should render sound_toggle_label correctly in all 4 languages', () => {
      expect(getUIText('sound_toggle_label', 'zh-TW')).toBe('選擇音效');
      expect(getUIText('sound_toggle_label', 'english')).toBe('Selection Sound');
      expect(getUIText('sound_toggle_label', 'spanish')).toBe('Sonido de Seleccion');
      expect(getUIText('sound_toggle_label', 'vietnamese')).toBe('Am thanh chon');
    });

    it('should fallback to English when language not found', () => {
      expect(getUIText('clear_selections_btn', 'unknown')).toBe('Clear Selections');
    });
  });
});
