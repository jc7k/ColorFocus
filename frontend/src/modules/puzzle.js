/**
 * Puzzle generation module.
 * Handles puzzle creation, rendering, and font sizing.
 */

import { COLOR_SUBSETS, sanitizeNumber } from './config.js';
import { colorsJson, colorLabelsJson } from './data.js';
import * as state from './state.js';
import { getUIText, updateGridCSS } from './ui.js';
import { handleGridKeydown, toggleTileSelection } from './tiles.js';

// ===========================================
// PRNG (Seeded Random Number Generator)
// ===========================================

/**
 * Mulberry32 PRNG - deterministic random number generator
 */
export function mulberry32(seed) {
  return function() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

/**
 * Fisher-Yates shuffle with seeded random
 */
export function shuffle(array, random) {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// ===========================================
// STROOP INTERFERENCE OPTIMIZATION
// ===========================================

/**
 * Get adjacent indices for a cell (orthogonal neighbors only)
 */
export function getAdjacentIndices(flatIndex, gridSize) {
  const row = Math.floor(flatIndex / gridSize);
  const col = flatIndex % gridSize;
  const neighbors = [];

  if (row > 0) neighbors.push(flatIndex - gridSize); // Above
  if (row < gridSize - 1) neighbors.push(flatIndex + gridSize); // Below
  if (col > 0) neighbors.push(flatIndex - 1); // Left
  if (col < gridSize - 1) neighbors.push(flatIndex + 1); // Right

  return neighbors;
}

/**
 * Calculate interference score at a cell
 */
export function interferenceAt(cells, idx, gridSize) {
  const neighbors = getAdjacentIndices(idx, gridSize);
  let interference = 0;
  const cell = cells[idx];

  for (const ni of neighbors) {
    const neighbor = cells[ni];
    // Interference when neighbor's word matches this cell's ink color
    if (neighbor.word === cell.inkColor) interference++;
    // Interference when this cell's word matches neighbor's ink color
    if (cell.word === neighbor.inkColor) interference++;
  }

  return interference;
}

/**
 * Optimize puzzle for maximum Stroop interference
 */
export function optimizeStroopInterference(cells, gridSize, random, maxSwaps = 50) {
  const optimized = [...cells];

  for (let iter = 0; iter < maxSwaps; iter++) {
    // Pick two random indices to potentially swap
    const i = Math.floor(random() * cells.length);
    let j = Math.floor(random() * cells.length);
    if (i === j) continue;

    // Calculate current interference
    const beforeI = interferenceAt(optimized, i, gridSize);
    const beforeJ = interferenceAt(optimized, j, gridSize);

    // Swap
    [optimized[i], optimized[j]] = [optimized[j], optimized[i]];

    // Calculate new interference
    const afterI = interferenceAt(optimized, i, gridSize);
    const afterJ = interferenceAt(optimized, j, gridSize);

    // Keep swap only if interference increased
    if (afterI + afterJ <= beforeI + beforeJ) {
      // Revert swap
      [optimized[i], optimized[j]] = [optimized[j], optimized[i]];
    }
  }

  return optimized;
}

// ===========================================
// FONT SIZE CALCULATION
// ===========================================

/**
 * Calculate optimal font size based on cell dimensions and language
 */
export function calculatePuzzleFontSize() {
  const grid = document.getElementById('puzzleGrid');
  if (!grid) return 16; // Default fallback

  // Get actual grid dimensions
  const gridRect = grid.getBoundingClientRect();
  const gridWidth = gridRect.width;

  // Calculate cell width accounting for gaps
  const gap = parseInt(grid.style.gap) || 2;
  const columns = state.currentGridSize;
  const totalGap = gap * (columns - 1);
  const cellWidth = (gridWidth - totalGap) / columns;

  // Language-based width multipliers (based on longest word character count)
  // zh-TW: single characters = 1.15
  // vietnamese: 3-5 chars = 2.6
  // english: MAGENTA = 7 chars = 4.2
  // spanish: NARANJA = 7 chars = 4.2
  const widthMultipliers = {
    'zh-TW': 1.15,
    english: 4.2,
    spanish: 4.2,
    vietnamese: 2.6
  };

  const multiplier = widthMultipliers[state.currentLanguage] || 4.2;

  // Calculate font size to fill ~80% of cell width
  const fontSize = (cellWidth * 0.8) / multiplier;

  // Clamp to reasonable bounds (10px min, no max - let cell size determine)
  return Math.max(10, fontSize);
}

/**
 * Apply calculated font size to all puzzle cells
 */
export function applyPuzzleFontSize() {
  const fontSize = calculatePuzzleFontSize();
  document.querySelectorAll('.puzzle-cell').forEach(cell => {
    cell.style.fontSize = `${fontSize}px`;
  });
}

// ===========================================
// PUZZLE RENDERING
// ===========================================

/**
 * Render the puzzle grid display (without regenerating data)
 */
export function renderPuzzleDisplay() {
  if (!state.currentPuzzle) return;

  const grid = document.getElementById('puzzleGrid');
  grid.innerHTML = '';

  // Reset focused tile index when re-rendering
  state.setFocusedTileIndex(0);

  state.currentPuzzle.forEach((cell, index) => {
    const div = document.createElement('div');
    div.className = 'puzzle-cell';
    div.setAttribute('data-index', index);
    div.setAttribute('role', 'gridcell');
    div.textContent = colorLabelsJson[cell.word][state.currentLanguage];
    div.style.color = colorsJson[cell.inkColor];

    // Apply selected class and aria-pressed if tile is in selectedTiles set
    if (state.selectedTiles.has(index)) {
      div.classList.add('selected');
      div.setAttribute('aria-pressed', 'true');
    } else {
      div.setAttribute('aria-pressed', 'false');
    }

    // Roving tabindex: first tile gets tabindex 0, others get -1
    div.setAttribute('tabindex', index === 0 ? '0' : '-1');

    // Add click handler for tile selection
    div.addEventListener('click', () => {
      toggleTileSelection(index);
      // Update focus to clicked tile
      const previousCell = document.querySelector(`.puzzle-cell[data-index="${state.focusedTileIndex}"]`);
      if (previousCell) {
        previousCell.setAttribute('tabindex', '-1');
      }
      div.setAttribute('tabindex', '0');
      state.setFocusedTileIndex(index);
    });

    // Add keyboard event handler
    div.addEventListener('keydown', handleGridKeydown);

    grid.appendChild(div);
  });

  // Apply font size after rendering
  applyPuzzleFontSize();
}

/**
 * Update metadata display with translated labels
 */
export function updateMetadata() {
  if (!state.currentPuzzle) return;

  const metaDiv = document.getElementById('metadata');
  metaDiv.textContent = ''; // Clear safely

  const totalCells = state.currentGridSize * state.currentGridSize;
  const gridSizeDisplay = `${state.currentGridSize}x${state.currentGridSize}`;
  const metaItems = [
    { label: getUIText('metadata_seed'), value: String(state.currentSeed) },
    { label: getUIText('metadata_colors'), value: String(state.currentColorCount) },
    { label: getUIText('metadata_grid'), value: gridSizeDisplay },
    { label: getUIText('metadata_congruent'), value: `${state.currentCongruentCount}/${totalCells} (${(state.currentCongruentCount/totalCells*100).toFixed(1)}%)` }
  ];

  metaItems.forEach(item => {
    const div = document.createElement('div');
    div.className = 'metadata-item';

    const labelSpan = document.createElement('span');
    labelSpan.textContent = item.label;
    div.appendChild(labelSpan);

    const valueSpan = document.createElement('span');
    valueSpan.className = 'metadata-value';
    valueSpan.textContent = item.value;
    div.appendChild(valueSpan);

    metaDiv.appendChild(div);
  });
}

// ===========================================
// PUZZLE GENERATION
// ===========================================

/**
 * Generate a new puzzle
 * @param {Object} callbacks - Optional callbacks for answer rendering
 */
export function generatePuzzle(callbacks = {}) {
  // Reset state
  state.setHasChecked(false);
  state.setAnswerKeyRevealed(false);
  state.selectedTiles.clear();
  state.resetIdentificationState();
  state.resetAssignmentState();
  state.setFocusedTileIndex(0);
  document.getElementById('answerKeyContent').classList.remove('revealed');
  document.getElementById('revealBtn').textContent = getUIText('reveal_btn');
  document.getElementById('revealWarning').style.display = 'block';
  document.getElementById('resultsSection').classList.remove('visible');
  document.getElementById('checkBtn').disabled = false;

  const seedInput = document.getElementById('seed');
  const congruenceInput = document.getElementById('congruence');
  const colorCountSelect = document.getElementById('colorCount');

  // Apply input sanitization for security
  const seed = sanitizeNumber(seedInput.value, 0, 2147483647, 42);
  const congruencePercent = sanitizeNumber(congruenceInput.value, 0, 100, 12.5);
  const congruence = congruencePercent / 100;
  const colorCount = sanitizeNumber(colorCountSelect.value, 1, 8, 4);

  // Store for metadata re-rendering
  state.setCurrentSeed(seed);
  state.setCurrentColorCount(colorCount);

  const random = mulberry32(seed);
  state.setActiveColors(COLOR_SUBSETS[colorCount] || COLOR_SUBSETS[2]);

  // Create ink distribution (roughly equal with small variations)
  const totalCells = state.currentGridSize * state.currentGridSize;
  const basePerColor = Math.floor(totalCells / colorCount);

  // Create base distribution then add random variation
  let inkColors = [];
  let remaining = totalCells;

  state.activeColors.forEach((token, i) => {
    if (i === state.activeColors.length - 1) {
      // Last color gets whatever remains
      for (let j = 0; j < remaining; j++) {
        inkColors.push(token);
      }
    } else {
      // Add variation: +/-2 from base, but keep within bounds
      const variation = Math.floor(random() * 5) - 2; // -2 to +2
      const count = Math.max(1, Math.min(basePerColor + 2, basePerColor + variation));
      for (let j = 0; j < count; j++) {
        inkColors.push(token);
      }
      remaining -= count;
    }
  });
  inkColors = shuffle(inkColors, random);

  // Assign words with congruence control
  const cells = inkColors.map(inkColor => {
    let word;
    if (random() < congruence) {
      word = inkColor; // Congruent
    } else {
      // Pick different color from active colors
      const otherColors = state.activeColors.filter(c => c !== inkColor);
      word = otherColors.length > 0
        ? otherColors[Math.floor(random() * otherColors.length)]
        : inkColor;
    }
    return { word, inkColor };
  });

  // Optimize for Stroop interference
  const optimizedCells = optimizeStroopInterference(cells, state.currentGridSize, random);
  state.setCurrentPuzzle(optimizedCells);

  // Update grid CSS for current grid size
  updateGridCSS();

  // Render grid
  renderPuzzleDisplay();

  // Count distribution (correct answers)
  const answers = {};
  let congruentCount = 0;
  cells.forEach(cell => {
    answers[cell.inkColor] = (answers[cell.inkColor] || 0) + 1;
    if (cell.word === cell.inkColor) congruentCount++;
  });
  state.setCorrectAnswers(answers);
  state.setCurrentCongruentCount(congruentCount);

  // Call optional callbacks for answer rendering
  if (callbacks.renderAnswerInputs) callbacks.renderAnswerInputs();
  if (callbacks.renderAnswerKey) callbacks.renderAnswerKey();

  // Render metadata with translated labels
  updateMetadata();
}

// ===========================================
// EVENT HANDLERS FOR WINDOW RESIZE
// ===========================================

/**
 * Initialize resize event handlers
 */
export function initResizeHandlers() {
  // Recalculate font size on window resize
  window.addEventListener('resize', () => {
    if (state.currentPuzzle) {
      applyPuzzleFontSize();
    }
  });

  // Recalculate font size on orientation change (mobile devices)
  window.addEventListener('orientationchange', () => {
    if (state.currentPuzzle) {
      setTimeout(() => {
        applyPuzzleFontSize();
      }, 100);
    }
  });
}
