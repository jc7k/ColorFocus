/**
 * Application state management.
 * Centralizes all state variables for the puzzle application.
 */

import {
  validateLanguage,
  validateGridSize,
  validateDifficulty,
  validateSpacing,
  validateSoundEnabled
} from './config.js';

// ===========================================
// CORE PUZZLE STATE
// ===========================================
export let currentPuzzle = null;
export let correctAnswers = {};
export let activeColors = [];
export let hasChecked = false;
export let answerKeyRevealed = false;

// ===========================================
// USER PREFERENCES (from localStorage)
// ===========================================
export let currentLanguage = validateLanguage(localStorage.getItem('colorFocusLanguage') || 'zh-TW');
export let currentGridSize = validateGridSize(localStorage.getItem('colorFocusGridSize') || 4);
export let currentDifficulty = validateDifficulty(localStorage.getItem('colorFocusDifficulty') || 'easy');
export let currentSpacing = validateSpacing(localStorage.getItem('colorFocusSpacing') || 'normal');
export let soundEnabled = validateSoundEnabled(localStorage.getItem('colorFocusSoundEnabled'));

// ===========================================
// TILE SELECTION STATE
// ===========================================
export let selectedTiles = new Set();
export let focusedTileIndex = 0;
export let audioContext = null;

// ===========================================
// STROOP INTERFERENCE DETECTION STATE
// ===========================================
// Track which tiles are assigned to which color (colorToken -> Set<tileIndex>)
export let assignedTiles = new Map();
// Track tiles that were incorrectly assigned (tileIndex -> {assignedColor, actualColor, wordShown})
export let stroopErrors = new Map();

// ===========================================
// MISTAKE IDENTIFICATION STATE
// ===========================================
// Whether identification mode is active
export let identificationMode = false;
// Current step in identification flow
export let identificationStep = { currentColor: null, queueIndex: -1 };
// Map of color tokens to discrepancy data
export let discrepancyData = new Map();
// Array of colors with discrepancies to process in order
export let colorQueue = [];
// Map of color tokens to Set of selected tile indices
export let identificationResults = new Map();
// Tile-level analysis results
export let mistakeAnalysis = new Map();

// ===========================================
// PUZZLE METADATA STATE
// ===========================================
export let currentSeed = 42;
export let currentColorCount = 4;
export let currentCongruentCount = 0;

// ===========================================
// MODAL STATE
// ===========================================
export let currentModal = null;
export let previouslyFocusedElement = null;

// ===========================================
// AUTH STATE
// ===========================================
export let currentUser = null;

// ===========================================
// STATE SETTERS
// ===========================================

export function setCurrentPuzzle(puzzle) { currentPuzzle = puzzle; }
export function setCorrectAnswers(answers) { correctAnswers = answers; }
export function setActiveColors(colors) { activeColors = colors; }
export function setHasChecked(checked) { hasChecked = checked; }
export function setAnswerKeyRevealed(revealed) { answerKeyRevealed = revealed; }
export function setCurrentLanguage(lang) {
  currentLanguage = lang;
  localStorage.setItem('colorFocusLanguage', lang);
}
export function setCurrentGridSize(size) {
  currentGridSize = size;
  localStorage.setItem('colorFocusGridSize', size);
}
export function setCurrentDifficulty(difficulty) {
  currentDifficulty = difficulty;
  localStorage.setItem('colorFocusDifficulty', difficulty);
}
export function setCurrentSpacing(spacing) {
  currentSpacing = spacing;
  localStorage.setItem('colorFocusSpacing', spacing);
}
export function setSoundEnabled(enabled) {
  soundEnabled = enabled;
  localStorage.setItem('colorFocusSoundEnabled', String(enabled));
}
export function setFocusedTileIndex(index) { focusedTileIndex = index; }
export function setAudioContext(ctx) { audioContext = ctx; }
export function setIdentificationMode(mode) { identificationMode = mode; }
export function setIdentificationStep(step) { identificationStep = step; }
export function setColorQueue(queue) { colorQueue = queue; }
export function setCurrentSeed(seed) { currentSeed = seed; }
export function setCurrentColorCount(count) { currentColorCount = count; }
export function setCurrentCongruentCount(count) { currentCongruentCount = count; }
export function setCurrentModal(modal) { currentModal = modal; }
export function setPreviouslyFocusedElement(el) { previouslyFocusedElement = el; }
export function setCurrentUser(user) { currentUser = user; }

// ===========================================
// STATE RESET FUNCTIONS
// ===========================================

export function resetAssignmentState() {
  assignedTiles.clear();
  stroopErrors.clear();
}

export function resetIdentificationState() {
  identificationMode = false;
  identificationStep = { currentColor: null, queueIndex: -1 };
  discrepancyData.clear();
  colorQueue = [];
  identificationResults.clear();
  mistakeAnalysis.clear();
}
