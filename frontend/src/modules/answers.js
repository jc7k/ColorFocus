/**
 * Answer handling module.
 * Handles answer inputs, checking, and results display.
 */

import { ALL_COLOR_TOKENS, sanitizeNumber } from './config.js';
import { colorsJson, colorLabelsJson } from './data.js';
import * as state from './state.js';
import { getUIText } from './ui.js';
import { savePuzzleHistory } from './auth.js';

// ===========================================
// STROOP INTERFERENCE HELPERS
// ===========================================

/**
 * Get total count of assigned tiles across all colors
 */
export function getTotalAssignedCount() {
  let count = 0;
  state.assignedTiles.forEach(tileSet => {
    count += tileSet.size;
  });
  return count;
}

/**
 * Validate tile assignment and detect Stroop interference
 */
export function validateTileAssignment(tileIndices, assignedColor) {
  const errors = [];
  tileIndices.forEach(index => {
    const tile = state.currentPuzzle[index];
    if (tile.inkColor !== assignedColor) {
      const error = {
        tileIndex: index,
        assignedColor: assignedColor,
        actualColor: tile.inkColor,
        wordShown: tile.word,
        isStroopInfluenced: tile.word === assignedColor
      };
      errors.push(error);
      state.stroopErrors.set(index, error);
    }
  });
  return errors;
}

/**
 * Check for tiles already assigned to other colors
 */
export function checkForConflicts(tileIndices, newColor) {
  const conflicts = [];
  state.assignedTiles.forEach((tiles, colorToken) => {
    if (colorToken !== newColor) {
      tileIndices.forEach(index => {
        if (tiles.has(index)) {
          conflicts.push({ tileIndex: index, previousColor: colorToken });
        }
      });
    }
  });
  return conflicts;
}

/**
 * Handle tile reassignment conflicts
 */
export function handleConflicts(conflicts, newColor) {
  conflicts.forEach(({ tileIndex, previousColor }) => {
    const prevSet = state.assignedTiles.get(previousColor);
    if (prevSet) {
      prevSet.delete(tileIndex);
      const prevInput = document.getElementById(`answer-${previousColor}`);
      if (prevInput) {
        prevInput.value = String(prevSet.size);
      }
    }
    state.stroopErrors.delete(tileIndex);
    const cell = document.querySelector(`.puzzle-cell[data-index="${tileIndex}"]`);
    if (cell) {
      cell.classList.remove('stroop-warning');
    }
  });
}

/**
 * Show Stroop warning panel
 */
export function showStroopWarnings(errors, assignedColor) {
  const panel = document.getElementById('stroopWarningPanel');
  const titleEl = document.getElementById('stroopWarningTitle');
  const messageEl = document.getElementById('stroopWarningMessage');

  const assignedColorLabel = colorLabelsJson[assignedColor][state.currentLanguage];
  const firstError = errors[0];
  const actualColorLabel = colorLabelsJson[firstError.actualColor][state.currentLanguage];
  const wordLabel = colorLabelsJson[firstError.wordShown][state.currentLanguage];

  titleEl.textContent = getUIText('stroop_warning_title') || 'Stroop Interference Detected';
  let message = getUIText('stroop_warning_message') || "{count} tile(s) may be incorrectly assigned. The tile showing '{word}' is actually printed in {actual} ink. This is the Stroop effect!";
  message = message
    .replace('{count}', String(errors.length))
    .replace('{word}', wordLabel)
    .replace('{actual}', actualColorLabel);
  messageEl.textContent = message;

  panel.classList.add('visible');
}

/**
 * Hide Stroop warning panel
 */
export function hideStroopWarningPanel() {
  const panel = document.getElementById('stroopWarningPanel');
  panel.classList.remove('visible');
}

/**
 * Handle color swatch click for auto-fill
 */
export function handleSwatchClick(token) {
  hideStroopWarningPanel();

  if (state.selectedTiles.size === 0) {
    return;
  }

  const input = document.getElementById(`answer-${token}`);
  if (!input) return;

  if (!state.assignedTiles.has(token)) {
    state.assignedTiles.set(token, new Set());
  }

  const conflicts = checkForConflicts(state.selectedTiles, token);
  if (conflicts.length > 0) {
    handleConflicts(conflicts, token);
  }

  const errors = validateTileAssignment(state.selectedTiles, token);

  state.selectedTiles.forEach(index => {
    state.assignedTiles.get(token).add(index);
  });

  input.value = String(state.assignedTiles.get(token).size);

  // Mark tiles as assigned
  state.selectedTiles.forEach(index => {
    const cell = document.querySelector(`.puzzle-cell[data-index="${index}"]`);
    if (cell) {
      cell.classList.add('assigned');
      cell.classList.remove('selected');
      cell.setAttribute('aria-pressed', 'false');
    }
  });

  // Mark Stroop warnings
  errors.forEach(error => {
    const cell = document.querySelector(`.puzzle-cell[data-index="${error.tileIndex}"]`);
    if (cell) {
      cell.classList.add('stroop-warning');
    }
  });

  if (errors.length > 0) {
    showStroopWarnings(errors, token);
  }

  state.selectedTiles.clear();
}

// ===========================================
// ANSWER INPUT RENDERING
// ===========================================

/**
 * Render answer input fields
 */
export function renderAnswerInputs() {
  const answerGrid = document.getElementById('answerGrid');
  answerGrid.textContent = '';

  const maxInputValue = state.currentGridSize * state.currentGridSize;

  state.activeColors.forEach(token => {
    const item = document.createElement('div');
    item.className = 'answer-item';
    item.id = `answer-item-${token}`;

    // Create swatch with auto-fill click handler
    const swatch = document.createElement('div');
    swatch.className = 'color-swatch';
    swatch.style.backgroundColor = colorsJson[token];
    swatch.setAttribute('role', 'button');
    swatch.setAttribute('tabindex', '0');
    swatch.setAttribute('aria-label', 'Auto-fill with selected tile count');
    swatch.addEventListener('click', () => handleSwatchClick(token));
    swatch.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        handleSwatchClick(token);
      }
    });
    item.appendChild(swatch);

    // Create label
    const label = document.createElement('span');
    label.className = 'answer-label';
    label.textContent = colorLabelsJson[token][state.currentLanguage];
    item.appendChild(label);

    // Create input
    const input = document.createElement('input');
    input.type = 'number';
    input.className = 'answer-input';
    input.id = `answer-${token}`;
    input.min = '0';
    input.max = String(maxInputValue);
    input.placeholder = '?';
    input.readOnly = true;
    item.appendChild(input);

    // Create correct value span
    const correctSpan = document.createElement('span');
    correctSpan.className = 'correct-value';
    correctSpan.id = `correct-${token}`;
    item.appendChild(correctSpan);

    answerGrid.appendChild(item);
  });

  // Add enter key handler
  answerGrid.querySelectorAll('input').forEach(input => {
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        checkAnswers();
      }
    });
  });
}

/**
 * Render answer key
 */
export function renderAnswerKey() {
  const keyGrid = document.getElementById('answerKeyGrid');
  keyGrid.textContent = '';

  state.activeColors.forEach(token => {
    const item = document.createElement('div');
    item.className = 'answer-key-item';

    const swatch = document.createElement('div');
    swatch.className = 'color-swatch';
    swatch.style.backgroundColor = colorsJson[token];
    item.appendChild(swatch);

    const label = document.createElement('span');
    label.className = 'answer-key-label';
    label.textContent = colorLabelsJson[token][state.currentLanguage];
    item.appendChild(label);

    const count = document.createElement('span');
    count.className = 'answer-key-count';
    count.textContent = String(state.correctAnswers[token]);
    item.appendChild(count);

    keyGrid.appendChild(item);
  });
}

// ===========================================
// ANSWER CHECKING
// ===========================================

// Callback for calculating discrepancies (set from mistakes module)
let calculateDiscrepanciesCallback = null;
let updateIdentifyButtonCallback = null;

export function setMistakeCallbacks(calcDiscrepancies, updateButton) {
  calculateDiscrepanciesCallback = calcDiscrepancies;
  updateIdentifyButtonCallback = updateButton;
}

/**
 * Check answers
 */
export function checkAnswers() {
  if (!state.currentPuzzle) return;

  const totalTiles = state.currentGridSize * state.currentGridSize;
  const totalAssigned = getTotalAssignedCount();

  if (totalAssigned < totalTiles) {
    const remaining = totalTiles - totalAssigned;
    let message = getUIText('tiles_remaining') || "Please assign all tiles first. {count} tile(s) remaining.";
    message = message.replace('{count}', String(remaining));

    const panel = document.getElementById('stroopWarningPanel');
    const titleEl = document.getElementById('stroopWarningTitle');
    const messageEl = document.getElementById('stroopWarningMessage');
    titleEl.textContent = getUIText('assignment_incomplete_title') || 'Assignment Incomplete';
    messageEl.textContent = message;
    panel.classList.add('visible');
    return;
  }

  state.setHasChecked(true);
  let correctCount = 0;
  let totalOff = 0;

  const maxValue = state.currentGridSize * state.currentGridSize;
  const userAnswersObj = {};

  state.activeColors.forEach(token => {
    const input = document.getElementById(`answer-${token}`);
    const item = document.getElementById(`answer-item-${token}`);
    const correctSpan = document.getElementById(`correct-${token}`);
    const userAnswer = sanitizeNumber(input.value, 0, maxValue, 0);
    const correct = state.correctAnswers[token];

    userAnswersObj[token] = userAnswer;

    input.classList.remove('correct', 'incorrect');
    item.classList.remove('correct', 'incorrect');

    if (userAnswer === correct) {
      input.classList.add('correct');
      item.classList.add('correct');
      correctSpan.textContent = '';
      correctCount++;
    } else {
      input.classList.add('incorrect');
      item.classList.add('incorrect');
      correctSpan.textContent = correct;
      totalOff += Math.abs(userAnswer - correct);
    }
  });

  showResults(correctCount, state.activeColors.length, totalOff);

  if (state.currentUser) {
    const accuracy = Math.round((correctCount / state.activeColors.length) * 100);
    savePuzzleHistory(userAnswersObj, accuracy);
  }
}

/**
 * Show results with translated messages
 */
export function showResults(correct, total, totalOff) {
  const resultsSection = document.getElementById('resultsSection');
  const resultsSummary = document.getElementById('resultsSummary');
  const resultMessage = document.getElementById('resultMessage');

  const percentage = Math.round((correct / total) * 100);
  let scoreClass, message;

  if (correct === total) {
    scoreClass = 'perfect';
    message = getUIText('result_perfect');
  } else if (percentage >= 75) {
    scoreClass = 'good';
    message = getUIText('result_good')
      .replace('{correct}', String(correct))
      .replace('{total}', String(total));
  } else {
    scoreClass = 'needs-work';
    message = getUIText('result_needs_work')
      .replace('{correct}', String(correct))
      .replace('{total}', String(total));
  }

  resultsSummary.textContent = '';

  const stats = [
    { value: `${correct}/${total}`, label: getUIText('result_colors_correct'), hasClass: true },
    { value: `${percentage}%`, label: getUIText('result_accuracy'), hasClass: true },
    { value: String(totalOff), label: getUIText('result_total_off'), hasClass: false }
  ];

  stats.forEach(stat => {
    const div = document.createElement('div');
    div.className = stat.hasClass ? `result-stat ${scoreClass}` : 'result-stat';

    const valueDiv = document.createElement('div');
    valueDiv.className = 'value';
    valueDiv.textContent = stat.value;
    div.appendChild(valueDiv);

    const labelDiv = document.createElement('div');
    labelDiv.className = 'label';
    labelDiv.textContent = stat.label;
    div.appendChild(labelDiv);

    resultsSummary.appendChild(div);
  });

  resultMessage.className = `result-message ${scoreClass}`;
  resultMessage.textContent = message;

  resultsSection.classList.add('visible');

  // Calculate discrepancies and update button visibility
  if (calculateDiscrepanciesCallback) calculateDiscrepanciesCallback();
  if (updateIdentifyButtonCallback) updateIdentifyButtonCallback();
}

/**
 * Clear answers
 */
export function clearAnswers() {
  ALL_COLOR_TOKENS.forEach(token => {
    const input = document.getElementById(`answer-${token}`);
    const item = document.getElementById(`answer-item-${token}`);
    const correctSpan = document.getElementById(`correct-${token}`);

    if (input) {
      input.value = '';
      input.classList.remove('correct', 'incorrect');
    }
    if (item) {
      item.classList.remove('correct', 'incorrect');
    }
    if (correctSpan) {
      correctSpan.textContent = '';
    }
  });

  document.getElementById('resultsSection').classList.remove('visible');
  state.setHasChecked(false);

  // Reset assignment state
  state.resetAssignmentState();
  hideStroopWarningPanel();
  state.selectedTiles.clear();

  // Clear visual indicators
  document.querySelectorAll('.puzzle-cell').forEach(cell => {
    cell.classList.remove('assigned', 'stroop-warning');
  });

  // Hide identify mistakes button
  document.getElementById('identifyMistakesBtn').classList.remove('visible');
}

/**
 * Toggle answer key visibility
 */
export function toggleAnswerKey() {
  const content = document.getElementById('answerKeyContent');
  const btn = document.getElementById('revealBtn');
  const warning = document.getElementById('revealWarning');

  if (state.answerKeyRevealed) {
    content.classList.remove('revealed');
    btn.textContent = getUIText('reveal_btn');
    state.setAnswerKeyRevealed(false);
    warning.style.display = 'block';
  } else {
    content.classList.add('revealed');
    btn.textContent = getUIText('hide_btn');
    state.setAnswerKeyRevealed(true);
    warning.style.display = 'none';
  }
}

/**
 * Generate random seed
 */
export function randomSeed(generatePuzzleCallback) {
  document.getElementById('seed').value = Math.floor(Math.random() * 1000000);
  document.getElementById('modalSeed').value = document.getElementById('seed').value;
  if (generatePuzzleCallback) generatePuzzleCallback();
}
