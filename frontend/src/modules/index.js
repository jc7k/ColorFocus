/**
 * Main entry point for ColorFocus puzzle application.
 * Wires up all modules and initializes the application.
 */

// Import all modules
import * as state from './state.js';
import { colorsJson, colorLabelsJson, uiTextJson } from './data.js';
import {
  ALL_COLOR_TOKENS,
  COLOR_SUBSETS,
  DIFFICULTY_PRESETS,
  SPACING_VALUES,
  escapeHtml,
  sanitizeNumber,
  validateLanguage,
  validateGridSize,
  validateDifficulty,
  validateSpacing
} from './config.js';
import {
  getUIText,
  updateAllUIText,
  openModal,
  closeModal,
  handleModalEscape,
  handleBackdropClick,
  applyDifficultyPreset,
  updateColorDropdownOptions,
  updateModalColorDropdownOptions,
  updateGridCSS,
  setGeneratePuzzleCallback
} from './ui.js';
import {
  signInWithGoogle,
  signOut,
  initAuthListener,
  checkExistingSession,
  savePuzzleHistory
} from './auth.js';
import {
  toggleTileSelection,
  clearAllSelections,
  handleGridKeydown
} from './tiles.js';
import {
  generatePuzzle,
  renderPuzzleDisplay,
  applyPuzzleFontSize,
  updateMetadata,
  initResizeHandlers
} from './puzzle.js';
import {
  renderAnswerInputs,
  renderAnswerKey,
  checkAnswers,
  clearAnswers,
  toggleAnswerKey,
  randomSeed,
  hideStroopWarningPanel,
  setMistakeCallbacks
} from './answers.js';
import {
  calculateDiscrepancies,
  updateIdentifyMistakesButtonVisibility,
  startIdentificationMode,
  handleIdentificationDone,
  handleIdentificationCancel,
  handleGlobalKeydown,
  closeSummaryPanel
} from './mistakes.js';

// ===========================================
// MODULE CALLBACK WIRING
// ===========================================

// Create a wrapped generatePuzzle that includes answer callbacks
function generatePuzzleWithCallbacks() {
  generatePuzzle({
    renderAnswerInputs,
    renderAnswerKey
  });
}

// Set the generatePuzzle callback for UI module
setGeneratePuzzleCallback(generatePuzzleWithCallbacks);

// Set mistake callbacks for answers module
setMistakeCallbacks(calculateDiscrepancies, updateIdentifyMistakesButtonVisibility);

// ===========================================
// EVENT LISTENER WIRING
// ===========================================

function initEventListeners() {
  // Main control buttons
  document.getElementById('generateBtn').addEventListener('click', generatePuzzleWithCallbacks);
  document.getElementById('randomBtn').addEventListener('click', () => randomSeed(generatePuzzleWithCallbacks));
  document.getElementById('checkBtn').addEventListener('click', checkAnswers);
  document.getElementById('clearBtn').addEventListener('click', clearAnswers);
  document.getElementById('revealBtn').addEventListener('click', toggleAnswerKey);
  document.getElementById('clearSelectionsBtn').addEventListener('click', clearAllSelections);

  // Identification mode event listeners
  document.getElementById('identifyMistakesBtn').addEventListener('click', startIdentificationMode);
  document.getElementById('identificationDoneBtn').addEventListener('click', handleIdentificationDone);
  document.getElementById('identificationCancelBtn').addEventListener('click', handleIdentificationCancel);
  document.getElementById('closeSummaryBtn').addEventListener('click', closeSummaryPanel);

  // Stroop warning panel dismiss button
  document.getElementById('dismissWarningBtn').addEventListener('click', hideStroopWarningPanel);

  // Global keyboard handler for identification mode
  document.addEventListener('keydown', handleGlobalKeydown);

  // Modal event listeners
  document.getElementById('settingsBtn').addEventListener('click', () => openModal('settingsModal'));
  document.getElementById('aboutBtn').addEventListener('click', () => openModal('aboutModal'));
  document.getElementById('settingsModalClose').addEventListener('click', closeModal);
  document.getElementById('aboutModalClose').addEventListener('click', closeModal);
  document.getElementById('modalBackdrop').addEventListener('click', handleBackdropClick);

  // Modal settings controls
  document.getElementById('modalGridSize').addEventListener('change', updateModalColorDropdownOptions);

  // Auth event listeners
  document.getElementById('loginBtn').addEventListener('click', signInWithGoogle);
  document.getElementById('logoutBtn').addEventListener('click', signOut);
}

// ===========================================
// APPLICATION INITIALIZATION
// ===========================================

function initApp() {
  // Initialize resize handlers for font sizing
  initResizeHandlers();

  // Wire up event listeners
  initEventListeners();

  // Apply difficulty preset
  applyDifficultyPreset(state.currentDifficulty);

  // Initialize color dropdown options
  updateColorDropdownOptions();

  // Initialize UI text with current language
  updateAllUIText();

  // Initialize auth
  initAuthListener();
  checkExistingSession();

  // Initial puzzle generation
  generatePuzzleWithCallbacks();
}

// Start the application
initApp();

// ===========================================
// EXPORTS FOR DEBUGGING (optional)
// ===========================================
// These can be accessed via window.ColorFocus for debugging if needed
export {
  state,
  colorsJson,
  colorLabelsJson,
  uiTextJson,
  generatePuzzleWithCallbacks as generatePuzzle
};
