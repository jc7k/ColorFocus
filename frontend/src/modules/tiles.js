/**
 * Tile selection and interaction module.
 * Handles tile selection, keyboard navigation, and audio feedback.
 */

import * as state from './state.js';

// ===========================================
// AUDIO FEEDBACK
// ===========================================

/**
 * Play selection sound feedback (lazy initialize AudioContext)
 */
export function playSelectionSound() {
  if (!state.soundEnabled) return;

  try {
    // Lazy initialize AudioContext on first user interaction
    if (!state.audioContext) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) {
        state.setAudioContext(new AudioContextClass());
      }
    }

    if (!state.audioContext) return;

    // Resume context if suspended (required by browser autoplay policies)
    if (state.audioContext.state === 'suspended') {
      state.audioContext.resume();
    }

    // Create a short, gentle "pop" sound
    const oscillator = state.audioContext.createOscillator();
    const gainNode = state.audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(state.audioContext.destination);

    // Use a soft sine wave at a pleasant frequency
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(800, state.audioContext.currentTime);

    // Quick fade in and out for a soft "pop"
    gainNode.gain.setValueAtTime(0, state.audioContext.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.1, state.audioContext.currentTime + 0.01);
    gainNode.gain.exponentialRampToValueAtTime(0.001, state.audioContext.currentTime + 0.08);

    oscillator.start(state.audioContext.currentTime);
    oscillator.stop(state.audioContext.currentTime + 0.08);
  } catch (e) {
    // Silently fail - audio is a nice-to-have, not critical
    console.debug('Audio playback failed:', e);
  }
}

// ===========================================
// TILE SELECTION
// ===========================================

/**
 * Toggle tile selection
 */
export function toggleTileSelection(index) {
  const cell = document.querySelector(`.puzzle-cell[data-index="${index}"]`);
  if (!cell) return;

  if (state.selectedTiles.has(index)) {
    state.selectedTiles.delete(index);
    cell.classList.remove('selected');
    cell.setAttribute('aria-pressed', 'false');
  } else {
    state.selectedTiles.add(index);
    cell.classList.add('selected');
    cell.setAttribute('aria-pressed', 'true');
    playSelectionSound();
  }
}

/**
 * Clear all tile selections
 */
export function clearAllSelections() {
  // If in identification mode, this clears selections for current color
  if (state.identificationMode) {
    // Store current selections before clearing (they'll be processed later)
    state.selectedTiles.clear();
    document.querySelectorAll('.puzzle-cell.selected').forEach(cell => {
      cell.classList.remove('selected');
      cell.setAttribute('aria-pressed', 'false');
    });
    return;
  }

  // Normal mode: clear all selections
  state.selectedTiles.clear();
  document.querySelectorAll('.puzzle-cell.selected').forEach(cell => {
    cell.classList.remove('selected');
    cell.setAttribute('aria-pressed', 'false');
  });
}

// ===========================================
// KEYBOARD NAVIGATION
// ===========================================

/**
 * Calculate new tile index based on arrow key press
 */
export function calculateNewTileIndex(currentIndex, key, gridSize) {
  const row = Math.floor(currentIndex / gridSize);
  const col = currentIndex % gridSize;

  switch (key) {
    case 'ArrowUp':
      return row > 0 ? currentIndex - gridSize : currentIndex;
    case 'ArrowDown':
      return row < gridSize - 1 ? currentIndex + gridSize : currentIndex;
    case 'ArrowLeft':
      return col > 0 ? currentIndex - 1 : currentIndex;
    case 'ArrowRight':
      return col < gridSize - 1 ? currentIndex + 1 : currentIndex;
    default:
      return currentIndex;
  }
}

/**
 * Handle keyboard navigation within the puzzle grid
 */
export function handleGridKeydown(event) {
  const key = event.key;

  // Handle arrow key navigation
  if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(key)) {
    event.preventDefault();
    const newIndex = calculateNewTileIndex(state.focusedTileIndex, key, state.currentGridSize);

    if (newIndex !== state.focusedTileIndex) {
      // Update roving tabindex
      const currentCell = document.querySelector(`.puzzle-cell[data-index="${state.focusedTileIndex}"]`);
      const newCell = document.querySelector(`.puzzle-cell[data-index="${newIndex}"]`);

      if (currentCell && newCell) {
        currentCell.setAttribute('tabindex', '-1');
        newCell.setAttribute('tabindex', '0');
        newCell.focus();
        state.setFocusedTileIndex(newIndex);
      }
    }
  }

  // Handle spacebar to toggle selection
  if (key === ' ' || key === 'Spacebar') {
    event.preventDefault();
    toggleTileSelection(state.focusedTileIndex);
  }
}

// ===========================================
// TILE MARKING UTILITIES
// ===========================================

/**
 * Mark tiles as assigned visually
 */
export function markTilesAsAssigned(tileIndices, token) {
  tileIndices.forEach(index => {
    const cell = document.querySelector(`.puzzle-cell[data-index="${index}"]`);
    if (cell) {
      cell.classList.add('assigned');
      cell.classList.remove('selected');
      cell.setAttribute('aria-pressed', 'false');
    }
  });
}

/**
 * Mark tiles with Stroop warning
 */
export function markStroopWarnings(errors) {
  errors.forEach(error => {
    const cell = document.querySelector(`.puzzle-cell[data-index="${error.tileIndex}"]`);
    if (cell) {
      cell.classList.add('stroop-warning');
    }
  });
}
