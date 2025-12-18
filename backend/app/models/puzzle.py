"""
Puzzle data structures for ColorFocus word jungle grids.

This module provides type-safe dataclasses for representing puzzle grids
with Stroop interference patterns.

Usage:
    from backend.app.models.puzzle import PuzzleCell, PuzzleGrid, PuzzleMetadata

    # Create a cell with word "BLUE" rendered in orange ink
    cell = PuzzleCell(word=ColorToken.BLUE, ink_color=ColorToken.ORANGE)

    # Create metadata for an 8x8 grid
    metadata = PuzzleMetadata(seed=12345, rows=8, cols=8, congruence_percentage=0.125)

    # Create the full puzzle grid
    grid = PuzzleGrid(cells=[[cell, ...], ...], metadata=metadata)

    # Serialize to JSON-compatible dict
    data = grid.to_dict()
"""

from dataclasses import dataclass
from typing import Any, Dict, List

from backend.app.constants.colors import ColorToken


@dataclass
class PuzzleCell:
    """
    A single cell in a puzzle grid.

    Attributes:
        word: The color token representing the word meaning (semantic content).
        ink_color: The color token representing the display color (ink/visual color).

    For Stroop interference, word and ink_color are typically different
    (incongruent), requiring the user to focus on one while ignoring the other.
    """

    word: ColorToken
    ink_color: ColorToken

    def to_dict(self) -> Dict[str, str]:
        """
        Serialize the cell to a JSON-compatible dictionary.

        Returns:
            Dictionary with 'word' and 'inkColor' keys containing string values.
        """
        return {
            "word": self.word.value,
            "inkColor": self.ink_color.value,
        }


@dataclass
class PuzzleMetadata:
    """
    Metadata for a puzzle grid.

    Attributes:
        seed: The random seed used for deterministic generation.
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.
        congruence_percentage: Percentage of cells where word matches ink color (0.0-1.0).
        color_count: Number of colors used in the puzzle (2-8, default 4).
    """

    seed: int
    rows: int
    cols: int
    congruence_percentage: float
    color_count: int = 4

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the metadata to a JSON-compatible dictionary.

        Returns:
            Dictionary with seed, rows, cols, congruence_percentage, and color_count keys.
        """
        return {
            "seed": self.seed,
            "rows": self.rows,
            "cols": self.cols,
            "congruence_percentage": self.congruence_percentage,
            "color_count": self.color_count,
        }


@dataclass
class PuzzleGrid:
    """
    A complete puzzle grid with cells and metadata.

    Attributes:
        cells: 2D list of PuzzleCell objects representing the grid.
        metadata: PuzzleMetadata containing generation parameters.
    """

    cells: List[List[PuzzleCell]]
    metadata: PuzzleMetadata

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the puzzle grid to a JSON-compatible dictionary.

        Returns:
            Dictionary with 'grid' (2D array of cell dicts) and 'metadata' keys.
        """
        return {
            "grid": [[cell.to_dict() for cell in row] for row in self.cells],
            "metadata": self.metadata.to_dict(),
        }
