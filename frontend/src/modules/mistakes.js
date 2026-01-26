/**
 * Mistake identification module.
 * Handles the mistake identification flow and visualization.
 */

import { colorsJson, colorLabelsJson } from './data.js';
import * as state from './state.js';
import { getUIText } from './ui.js';

// ===========================================
// DISCREPANCY DETECTION
// ===========================================

/**
 * Calculate discrepancies between user answers and correct answers
 * @returns Array of color tokens with discrepancies
 */
export function calculateDiscrepancies() {
  state.discrepancyData.clear();
  const colorsWithDiscrepancies = [];

  state.activeColors.forEach(token => {
    const input = document.getElementById(`answer-${token}`);
    const userCount = input ? parseInt(input.value, 10) || 0 : 0;
    const correctCount = state.correctAnswers[token] || 0;
    const difference = userCount - correctCount;

    state.discrepancyData.set(token, {
      userCount,
      correctCount,
      difference
    });

    if (difference !== 0) {
      colorsWithDiscrepancies.push(token);
    }
  });

  return colorsWithDiscrepancies;
}

/**
 * Check if discrepancies exist
 */
export function hasDiscrepancies() {
  for (const [, data] of state.discrepancyData) {
    if (data.difference !== 0) {
      return true;
    }
  }
  return false;
}

/**
 * Update the visibility of the "Identify Mistakes" button
 */
export function updateIdentifyMistakesButtonVisibility() {
  const btn = document.getElementById('identifyMistakesBtn');
  if (state.hasChecked && hasDiscrepancies()) {
    btn.classList.add('visible');
  } else {
    btn.classList.remove('visible');
  }
}

// ===========================================
// IDENTIFICATION MODE MANAGEMENT
// ===========================================

/**
 * Enter identification mode with list of colors to identify
 */
export function enterIdentificationMode(discrepancyColors) {
  state.setIdentificationMode(true);
  state.setColorQueue([...discrepancyColors]);
  state.identificationResults.clear();

  if (discrepancyColors.length > 0) {
    state.setIdentificationStep({
      currentColor: discrepancyColors[0],
      queueIndex: 0
    });
  }
}

/**
 * Exit identification mode and clear state
 */
export function exitIdentificationMode() {
  state.setIdentificationMode(false);
  state.setIdentificationStep({ currentColor: null, queueIndex: -1 });
  state.selectedTiles.clear();
  document.querySelectorAll('.puzzle-cell.selected').forEach(cell => {
    cell.classList.remove('selected');
    cell.setAttribute('aria-pressed', 'false');
  });
}

// ===========================================
// STROOP INFLUENCE ANALYSIS
// ===========================================

/**
 * Get adjacent tile indices for Stroop analysis
 */
export function getAdjacentTileIndices(tileIndex) {
  const gridSize = state.currentGridSize;
  const row = Math.floor(tileIndex / gridSize);
  const col = tileIndex % gridSize;
  const adjacent = [];

  if (row > 0) adjacent.push(tileIndex - gridSize);
  if (row < gridSize - 1) adjacent.push(tileIndex + gridSize);
  if (col > 0) adjacent.push(tileIndex - 1);
  if (col < gridSize - 1) adjacent.push(tileIndex + 1);

  return adjacent;
}

/**
 * Analyze whether a tile error was Stroop-influenced
 */
export function analyzeStroopInfluence(tileIndex, perceivedColor) {
  if (!state.currentPuzzle || tileIndex < 0 || tileIndex >= state.currentPuzzle.length) {
    return false;
  }

  const tile = state.currentPuzzle[tileIndex];

  // Check if user perceived color matches the word shown
  if (tile.word === perceivedColor) {
    return true;
  }

  // Check adjacent tiles for word text that matches perceived color
  const adjacentIndices = getAdjacentTileIndices(tileIndex);
  for (const adjIdx of adjacentIndices) {
    if (adjIdx >= 0 && adjIdx < state.currentPuzzle.length) {
      const adjTile = state.currentPuzzle[adjIdx];
      if (adjTile.word === perceivedColor) {
        return true;
      }
    }
  }

  return false;
}

/**
 * Analyze identification results and mark tiles
 */
export function analyzeIdentificationResults() {
  state.mistakeAnalysis.clear();

  state.identificationResults.forEach((selectedTileSet, perceivedColor) => {
    selectedTileSet.forEach((tileIndex) => {
      if (tileIndex >= 0 && tileIndex < state.currentPuzzle.length) {
        const tile = state.currentPuzzle[tileIndex];
        const actualColor = tile.inkColor;
        const isCorrect = actualColor === perceivedColor;
        const isIncorrect = !isCorrect;

        const isStroopInfluenced = isIncorrect
          ? analyzeStroopInfluence(tileIndex, perceivedColor)
          : false;

        state.mistakeAnalysis.set(tileIndex, {
          tileIndex,
          isCorrect,
          isIncorrect,
          isStroopInfluenced,
          perceivedColor,
          actualColor
        });
      }
    });
  });
}

// ===========================================
// VISUALIZATION
// ===========================================

/**
 * Apply visual marking classes to tiles
 */
export function applyTileMarking() {
  document.querySelectorAll('.puzzle-cell').forEach(cell => {
    cell.classList.remove('tile-correct-id', 'tile-incorrect-id', 'tile-stroop-influenced');
  });

  const cells = document.querySelectorAll('.puzzle-cell');
  state.mistakeAnalysis.forEach((result, tileIndex) => {
    if (tileIndex >= 0 && tileIndex < cells.length) {
      const cell = cells[tileIndex];
      if (result.isCorrect) {
        cell.classList.add('tile-correct-id');
      }
      if (result.isIncorrect) {
        cell.classList.add('tile-incorrect-id');
      }
      if (result.isStroopInfluenced) {
        cell.classList.add('tile-stroop-influenced');
      }
    }
  });
}

/**
 * Calculate Stroop pattern category
 */
export function calculateStroopPattern(totalMistakes, stroopCount) {
  if (totalMistakes === 0) {
    return 'non_stroop';
  }

  const stroopPercentage = (stroopCount / totalMistakes) * 100;

  if (stroopPercentage >= 70) {
    return 'high_stroop';
  } else if (stroopPercentage >= 40) {
    return 'moderate_stroop';
  } else if (stroopCount > 0) {
    return 'mixed_errors';
  } else {
    return 'non_stroop';
  }
}

/**
 * Display Stroop guidance section
 */
export function displayStroopGuidance(totalMistakes, stroopCount) {
  const guidanceSection = document.getElementById('stroopGuidanceSection');

  if (totalMistakes === 0) {
    guidanceSection.classList.remove('visible');
    return;
  }

  const pattern = calculateStroopPattern(totalMistakes, stroopCount);

  document.getElementById('guidanceEducationHeader').textContent = getUIText('guidance_education_header');
  document.getElementById('guidanceEducationText').textContent = getUIText('guidance_education_text');
  document.getElementById('guidancePatternHeader').textContent = getUIText('guidance_pattern_header');
  document.getElementById('guidancePatternText').textContent = getUIText(`guidance_pattern_${pattern}`);
  document.getElementById('guidanceTipsHeader').textContent = getUIText('guidance_tips_header');
  document.getElementById('guidanceTipsText').textContent = getUIText(`guidance_tips_${pattern}`);

  guidanceSection.classList.add('visible');
}

/**
 * Display summary panel
 */
export function displaySummary() {
  let totalMistakes = 0;
  let stroopInfluencedCount = 0;

  state.mistakeAnalysis.forEach((result) => {
    if (result.isIncorrect) {
      totalMistakes++;
      if (result.isStroopInfluenced) {
        stroopInfluencedCount++;
      }
    }
  });

  const nonStroopMistakes = totalMistakes - stroopInfluencedCount;

  document.getElementById('totalMistakesValue').textContent = totalMistakes;
  document.getElementById('stroopInfluencedValue').textContent = stroopInfluencedCount;
  document.getElementById('nonStroopValue').textContent = nonStroopMistakes;

  document.getElementById('metaSeedValue').textContent = document.getElementById('seed').value;
  document.getElementById('metaGridValue').textContent = `${state.currentGridSize}x${state.currentGridSize}`;
  document.getElementById('metaLanguageValue').textContent = state.currentLanguage;
  document.getElementById('metaDifficultyValue').textContent = state.currentDifficulty;

  document.getElementById('summaryHeader').textContent = getUIText('summary_header');
  document.getElementById('totalMistakesLabel').textContent = getUIText('summary_total_mistakes');
  document.getElementById('stroopInfluencedLabel').textContent = getUIText('summary_stroop_influenced');
  document.getElementById('nonStroopLabel').textContent = getUIText('summary_non_stroop');
  document.getElementById('legendHeader').textContent = getUIText('legend_header');
  document.getElementById('legendCorrectText').textContent = getUIText('legend_correct');
  document.getElementById('legendIncorrectText').textContent = getUIText('legend_incorrect');
  document.getElementById('legendStroopText').textContent = getUIText('legend_stroop');

  displayStroopGuidance(totalMistakes, stroopInfluencedCount);

  document.getElementById('mistakeSummarySection').classList.add('visible');
}

/**
 * Analyze and visualize mistakes
 */
export function analyzeAndVisualizeMistakes() {
  state.setIdentificationMode(false);
  analyzeIdentificationResults();
  applyTileMarking();
  displaySummary();
}

/**
 * Close summary panel and clear markings
 */
export function closeSummaryPanel() {
  document.getElementById('mistakeSummarySection').classList.remove('visible');
  document.getElementById('stroopGuidanceSection')?.classList.remove('visible');

  document.querySelectorAll('.puzzle-cell').forEach(cell => {
    cell.classList.remove('tile-correct-id', 'tile-incorrect-id', 'tile-stroop-influenced');
  });

  state.mistakeAnalysis.clear();
  state.identificationResults.clear();
}

// ===========================================
// IDENTIFICATION UI
// ===========================================

/**
 * Get identification prompt text
 */
export function getIdentificationPromptText() {
  if (!state.identificationMode || !state.identificationStep.currentColor) {
    return '';
  }

  const colorToken = state.identificationStep.currentColor;
  const colorLabel = colorLabelsJson[colorToken]?.[state.currentLanguage] ?? colorToken;
  const promptTemplate = getUIText('identification_prompt');

  return promptTemplate.replace('{color}', colorLabel);
}

/**
 * Get next color indicator text
 */
export function getNextColorIndicator() {
  if (!state.identificationMode || state.identificationStep.queueIndex < 0) {
    return '';
  }

  const nextIndex = state.identificationStep.queueIndex + 1;
  if (nextIndex >= state.colorQueue.length) {
    return '';
  }

  const nextColor = state.colorQueue[nextIndex];
  const colorLabel = colorLabelsJson[nextColor]?.[state.currentLanguage] ?? nextColor;
  const template = getUIText('identification_next_color');

  return template.replace('{color}', colorLabel);
}

/**
 * Update identification prompt UI
 */
export function updateIdentificationPromptUI() {
  const promptPanel = document.getElementById('identificationPrompt');
  const swatch = document.getElementById('identificationColorSwatch');
  const promptText = document.getElementById('identificationPromptText');
  const nextIndicator = document.getElementById('identificationNextIndicator');
  const doneBtn = document.getElementById('identificationDoneBtn');
  const cancelBtn = document.getElementById('identificationCancelBtn');

  if (state.identificationMode && state.identificationStep.currentColor) {
    promptPanel.classList.add('visible');
    swatch.style.backgroundColor = colorsJson[state.identificationStep.currentColor] || '';
    promptText.textContent = getIdentificationPromptText();

    const nextText = getNextColorIndicator();
    nextIndicator.textContent = nextText;
    nextIndicator.style.display = nextText ? 'block' : 'none';

    doneBtn.textContent = getUIText('identification_done_btn');
    cancelBtn.textContent = getUIText('identification_cancel_btn');

    setTimeout(() => doneBtn.focus(), 100);
  } else {
    promptPanel.classList.remove('visible');
  }
}

/**
 * Start identification mode
 */
export function startIdentificationMode() {
  const discrepancyColors = calculateDiscrepancies();
  if (discrepancyColors.length === 0) {
    return;
  }

  state.selectedTiles.clear();
  document.querySelectorAll('.puzzle-cell.selected').forEach(cell => {
    cell.classList.remove('selected');
    cell.setAttribute('aria-pressed', 'false');
  });

  enterIdentificationMode(discrepancyColors);
  updateIdentificationPromptUI();
}

/**
 * Handle "Done" button click
 */
export function handleIdentificationDone() {
  if (!state.identificationMode) {
    return;
  }

  const currentColor = state.identificationStep.currentColor;
  if (currentColor) {
    state.identificationResults.set(currentColor, new Set(state.selectedTiles));
  }

  state.selectedTiles.clear();
  document.querySelectorAll('.puzzle-cell.selected').forEach(cell => {
    cell.classList.remove('selected');
    cell.setAttribute('aria-pressed', 'false');
  });

  const nextIndex = state.identificationStep.queueIndex + 1;
  if (nextIndex >= state.colorQueue.length) {
    state.setIdentificationStep({ currentColor: null, queueIndex: -1 });
    updateIdentificationPromptUI();
    analyzeAndVisualizeMistakes();
    return;
  }

  state.setIdentificationStep({
    currentColor: state.colorQueue[nextIndex],
    queueIndex: nextIndex
  });

  updateIdentificationPromptUI();
}

/**
 * Handle "Cancel" button click
 */
export function handleIdentificationCancel() {
  exitIdentificationMode();
  updateIdentificationPromptUI();
}

/**
 * Handle global keyboard events for identification mode
 */
export function handleGlobalKeydown(e) {
  if (e.key === 'Escape' && state.identificationMode) {
    e.preventDefault();
    handleIdentificationCancel();
  }
}
