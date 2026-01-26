/**
 * UI utilities module.
 * Handles UI text, modals, and DOM utilities.
 */

import { uiTextJson, colorLabelsJson, colorsJson } from './data.js';
import { DIFFICULTY_PRESETS, SPACING_VALUES } from './config.js';
import * as state from './state.js';

// ===========================================
// UI TEXT FUNCTIONS
// ===========================================

/**
 * Get UI text for the current language
 */
export function getUIText(key) {
  if (uiTextJson[key] && uiTextJson[key][state.currentLanguage]) {
    return uiTextJson[key][state.currentLanguage];
  }
  // Fallback to English if key or language not found
  if (uiTextJson[key] && uiTextJson[key]['english']) {
    return uiTextJson[key]['english'];
  }
  return key; // Return key itself as last resort
}

/**
 * Get language descriptor for task instructions
 */
export function getLanguageDescriptor() {
  const descriptorKey = `language_descriptor_${state.currentLanguage}`;
  return getUIText(descriptorKey);
}

/**
 * Update all UI text elements based on current language
 */
export function updateAllUIText() {
  // Update page title dynamically
  document.title = getUIText('page_title');

  // Update elements with data-i18n attribute
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const text = getUIText(key);
    if (text && text !== key) {
      el.textContent = text;
    }
  });

  // Update elements with data-i18n-placeholder attribute
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    const text = getUIText(key);
    if (text && text !== key) {
      el.placeholder = text;
    }
  });

  // Update metadata labels
  const metadataSeed = document.querySelector('.metadata-item:first-child span:first-child');
  if (metadataSeed) {
    metadataSeed.textContent = getUIText('metadata_seed');
  }

  // Update subtitle with language-specific task instructions
  const subtitle = document.getElementById('subtitle');
  if (subtitle) {
    const task = getUIText('task_instruction');
    const langDescriptor = getLanguageDescriptor();
    subtitle.textContent = task.replace('{language}', langDescriptor);
  }

  // Update reveal/hide button text based on current state
  const revealBtn = document.getElementById('revealBtn');
  if (revealBtn) {
    revealBtn.textContent = state.answerKeyRevealed
      ? getUIText('hide_btn')
      : getUIText('reveal_btn');
  }
}

// ===========================================
// MODAL FUNCTIONS
// ===========================================

/**
 * Open a modal by ID
 */
export function openModal(modalId) {
  const modal = document.getElementById(modalId);
  const backdrop = document.getElementById('modalBackdrop');
  if (!modal || !backdrop) return;

  // Store previously focused element for restoration
  state.setPreviouslyFocusedElement(document.activeElement);

  // Sync modal controls with current state before opening
  if (modalId === 'settingsModal') {
    syncModalControlsFromState();
  }

  // Show modal and backdrop
  backdrop.classList.add('visible');
  modal.classList.add('visible');
  state.setCurrentModal(modal);

  // Focus first focusable element in modal
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  if (focusableElements.length > 0) {
    focusableElements[0].focus();
  }

  // Add escape key listener
  document.addEventListener('keydown', handleModalEscape);

  // Prevent body scroll
  document.body.style.overflow = 'hidden';
}

/**
 * Close current modal
 */
export function closeModal() {
  if (!state.currentModal) return;

  const backdrop = document.getElementById('modalBackdrop');

  // If settings modal, apply changes
  if (state.currentModal.id === 'settingsModal') {
    applyModalSettings();
  }

  // Hide modal and backdrop
  backdrop.classList.remove('visible');
  state.currentModal.classList.remove('visible');

  // Restore focus
  if (state.previouslyFocusedElement) {
    state.previouslyFocusedElement.focus();
  }

  // Remove escape key listener
  document.removeEventListener('keydown', handleModalEscape);

  // Restore body scroll
  document.body.style.overflow = '';

  state.setCurrentModal(null);
}

/**
 * Handle escape key for modal
 */
export function handleModalEscape(e) {
  if (e.key === 'Escape') {
    closeModal();
  }
}

/**
 * Handle backdrop click
 */
export function handleBackdropClick(e) {
  if (e.target.id === 'modalBackdrop') {
    closeModal();
  }
}

/**
 * Sync modal controls to current app state
 */
export function syncModalControlsFromState() {
  document.getElementById('modalLanguage').value = state.currentLanguage;
  document.getElementById('modalSpacing').value = state.currentSpacing;
  document.getElementById('modalSoundToggle').checked = state.soundEnabled;
  document.getElementById('modalDifficulty').value = state.currentDifficulty;
  document.getElementById('modalGridSize').value = state.currentGridSize;
  document.getElementById('modalColorCount').value = document.getElementById('colorCount').value;
  document.getElementById('modalCongruence').value = document.getElementById('congruence').value;
  document.getElementById('modalSeed').value = document.getElementById('seed').value;
}

/**
 * Apply modal settings to the app
 * Note: This function needs access to generatePuzzle, which creates a circular dependency.
 * The generatePuzzle function will be passed in from index.js
 */
let generatePuzzleCallback = null;
export function setGeneratePuzzleCallback(fn) {
  generatePuzzleCallback = fn;
}

export function applyModalSettings() {
  const newLanguage = document.getElementById('modalLanguage').value;
  const newSpacing = document.getElementById('modalSpacing').value;
  const newSound = document.getElementById('modalSoundToggle').checked;
  const newDifficulty = document.getElementById('modalDifficulty').value;
  const newGridSize = parseInt(document.getElementById('modalGridSize').value, 10);
  const newColorCount = document.getElementById('modalColorCount').value;
  const newCongruence = document.getElementById('modalCongruence').value;
  const newSeed = document.getElementById('modalSeed').value;

  let needsRegenerate = false;

  // Update language
  if (newLanguage !== state.currentLanguage) {
    state.setCurrentLanguage(newLanguage);
    document.getElementById('language').value = newLanguage;
    updateAllUIText();
    // Puzzle display will be re-rendered by generatePuzzle if needed
    needsRegenerate = true;
  }

  // Update spacing
  if (newSpacing !== state.currentSpacing) {
    state.setCurrentSpacing(newSpacing);
    document.getElementById('spacing').value = newSpacing;
    needsRegenerate = true;
  }

  // Update sound
  if (newSound !== state.soundEnabled) {
    state.setSoundEnabled(newSound);
    document.getElementById('soundToggle').checked = newSound;
  }

  // Update difficulty
  if (newDifficulty !== state.currentDifficulty) {
    state.setCurrentDifficulty(newDifficulty);
    document.getElementById('difficulty').value = newDifficulty;
    applyDifficultyPreset(state.currentDifficulty);
    needsRegenerate = true;
  }

  // Update grid size
  if (newGridSize !== state.currentGridSize) {
    state.setCurrentGridSize(newGridSize);
    document.getElementById('gridSize').value = newGridSize;
    updateColorDropdownOptions();
    needsRegenerate = true;
  }

  // Update color count
  if (newColorCount !== document.getElementById('colorCount').value) {
    document.getElementById('colorCount').value = newColorCount;
    needsRegenerate = true;
  }

  // Update seed
  if (newSeed !== document.getElementById('seed').value) {
    document.getElementById('seed').value = newSeed;
    needsRegenerate = true;
  }

  // Regenerate puzzle if settings changed
  if (needsRegenerate && generatePuzzleCallback) {
    generatePuzzleCallback();
  }
}

/**
 * Update modal color dropdown options based on grid size
 */
export function updateModalColorDropdownOptions() {
  const colorSelect = document.getElementById('modalColorCount');
  const gridSize = parseInt(document.getElementById('modalGridSize').value, 10);
  const maxColors = Math.min(8, gridSize);
  const currentColorValue = parseInt(colorSelect.value, 10);

  // Clear existing options
  colorSelect.innerHTML = '';

  // Add options from 1 to maxColors
  const minColors = Math.min(2, maxColors);
  for (let i = minColors; i <= maxColors; i++) {
    const option = document.createElement('option');
    option.value = i;
    option.textContent = i;
    if (i === Math.min(currentColorValue, maxColors)) {
      option.selected = true;
    }
    colorSelect.appendChild(option);
  }

  // If current selection exceeds new max, clamp it
  if (currentColorValue > maxColors) {
    colorSelect.value = maxColors;
  }
}

// ===========================================
// DIFFICULTY & GRID FUNCTIONS
// ===========================================

/**
 * Apply difficulty preset
 */
export function applyDifficultyPreset(difficulty) {
  const preset = DIFFICULTY_PRESETS[difficulty];
  if (preset) {
    document.getElementById('congruence').value = preset.congruencePercent;
  }
}

/**
 * Update color dropdown options based on grid size
 */
export function updateColorDropdownOptions() {
  const colorSelect = document.getElementById('colorCount');
  const maxColors = Math.min(8, state.currentGridSize);
  const currentColorValue = parseInt(colorSelect.value, 10);

  // Clear existing options
  colorSelect.innerHTML = '';

  // Add options from 2 to maxColors (minimum 2 colors for Stroop effect)
  const minColors = Math.min(2, maxColors);
  for (let i = minColors; i <= maxColors; i++) {
    const option = document.createElement('option');
    option.value = i;
    option.textContent = i;
    if (i === Math.min(currentColorValue, maxColors)) {
      option.selected = true;
    }
    colorSelect.appendChild(option);
  }

  // If current selection exceeds new max, clamp it
  if (currentColorValue > maxColors) {
    colorSelect.value = maxColors;
  }
}

/**
 * Update grid CSS for current grid size and spacing
 */
export function updateGridCSS() {
  const grid = document.getElementById('puzzleGrid');
  const gap = SPACING_VALUES[state.currentSpacing] || 2;
  grid.style.gridTemplateColumns = `repeat(${state.currentGridSize}, 1fr)`;
  grid.style.gap = `${gap}px`;
}
