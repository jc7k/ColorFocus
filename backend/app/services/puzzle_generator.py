"""
Puzzle generator service for ColorFocus word jungle grids.

This module provides deterministic generation of 8x8 puzzle grids with
Stroop interference patterns for cognitive training exercises.

Usage:
    from backend.app.services.puzzle_generator import PuzzleGenerator

    # Generate with explicit seed
    generator = PuzzleGenerator(seed=12345, congruence_percentage=0.125)
    puzzle = generator.generate()

    # Generate with auto-generated seed
    generator = PuzzleGenerator()
    puzzle = generator.generate()
    print(f"Seed used: {puzzle.metadata.seed}")

    # Serialize to JSON
    puzzle_dict = puzzle.to_dict()
"""

import logging
import random
import time
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional

from backend.app.constants.colors import ColorToken
from backend.app.constants.color_labels import Language
from backend.app.models.puzzle import PuzzleCell, PuzzleGrid, PuzzleMetadata

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """
    Result of a distribution validation check.

    Attributes:
        is_valid: Whether the distribution passed validation.
        issues: List of issues found during validation.
    """

    is_valid: bool
    issues: List[str]


class DistributionValidator:
    """
    Validates color distribution in puzzle grids.

    Ensures ink color distribution is within acceptable bounds to prevent
    heavily skewed puzzles that would make the game unfair.

    Attributes:
        min_count: Minimum acceptable count for any color (default: 6).
        max_count: Maximum acceptable count for any color (default: 10).
    """

    def __init__(self, min_count: int = 6, max_count: int = 10):
        """
        Initialize the validator with tolerance bounds.

        Args:
            min_count: Minimum acceptable appearances per color.
            max_count: Maximum acceptable appearances per color.
        """
        self.min_count = min_count
        self.max_count = max_count

    def validate(self, color_counts: Dict[ColorToken, int]) -> ValidationResult:
        """
        Validate a color distribution.

        Args:
            color_counts: Dictionary mapping ColorToken to count.

        Returns:
            ValidationResult with is_valid and any issues found.
        """
        issues: List[str] = []

        for token in ColorToken:
            count = color_counts.get(token, 0)

            if count < self.min_count:
                issues.append(
                    f"{token.value} appears {count} times, below minimum {self.min_count}"
                )
            elif count > self.max_count:
                issues.append(
                    f"{token.value} appears {count} times, above maximum {self.max_count}"
                )

        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
        )


class PuzzleGenerator:
    """
    Generator for 8x8 Stroop interference puzzle grids.

    Produces deterministic puzzle grids where color words are rendered in
    different ink colors to create cognitive interference effects.

    Attributes:
        seed: The random seed for deterministic generation.
        congruence_percentage: Percentage of cells where word matches ink (0.0-1.0).
        language: Language for color word labels.
    """

    # Fixed grid dimensions per specification
    ROWS = 8
    COLS = 8
    TOTAL_CELLS = ROWS * COLS  # 64

    # Retry configuration
    MAX_RETRIES = 3

    def __init__(
        self,
        seed: Optional[int] = None,
        congruence_percentage: float = 0.125,
        language: Language = Language.CHINESE,
    ):
        """
        Initialize the puzzle generator.

        Args:
            seed: Optional random seed for reproducibility. Auto-generated if None.
            congruence_percentage: Percentage of cells where word matches ink color.
                                   Default 0.125 (12.5%) for maximum Stroop interference.
            language: Language for color labels (default: CHINESE).
        """
        self.seed = seed if seed is not None else self._generate_seed()
        self.congruence_percentage = congruence_percentage
        self.language = language
        self._rng = random.Random(self.seed)
        self._validator = DistributionValidator()

    @staticmethod
    def _generate_seed() -> int:
        """Generate a seed based on current time in nanoseconds."""
        return int(time.time_ns() % (2**31))

    def generate(self) -> PuzzleGrid:
        """
        Generate a new 8x8 puzzle grid.

        The algorithm:
        1. Create ink color distribution (8 of each color = 64 total)
        2. Assign words based on congruence percentage
        3. Shuffle cells for spatial randomness
        4. Reshape into 8x8 grid
        5. Validate distribution and retry if needed

        Returns:
            PuzzleGrid with cells and metadata.
        """
        current_seed = self.seed
        attempts = 0

        while attempts < self.MAX_RETRIES:
            # Reset RNG with current seed for this attempt
            self._rng = random.Random(current_seed)

            # Step 1: Create ink color distribution
            ink_colors = self._create_ink_distribution()

            # Step 2: Assign words with congruence control
            cells_flat = self._assign_words(ink_colors)

            # Step 3: Shuffle for spatial randomness
            self._rng.shuffle(cells_flat)

            # Step 4: Reshape to 8x8 grid
            cells_2d = self._reshape_to_grid(cells_flat)

            # Step 5: Validate distribution
            ink_counts = self._count_ink_colors(cells_2d)
            validation_result = self._validator.validate(ink_counts)

            if validation_result.is_valid:
                # Build metadata and return valid grid
                metadata = PuzzleMetadata(
                    seed=self.seed,
                    rows=self.ROWS,
                    cols=self.COLS,
                    congruence_percentage=self.congruence_percentage,
                )
                return PuzzleGrid(cells=cells_2d, metadata=metadata)

            # Validation failed - log warning and retry with derived seed
            attempts += 1
            logger.warning(
                "Distribution validation failed (attempt %d/%d): %s",
                attempts,
                self.MAX_RETRIES,
                validation_result.issues,
            )
            current_seed = self._derive_new_seed(current_seed, attempts)

        # All retries exhausted - return last generated grid with warning
        logger.warning(
            "Max retries (%d) exhausted, returning potentially skewed grid",
            self.MAX_RETRIES,
        )
        metadata = PuzzleMetadata(
            seed=self.seed,
            rows=self.ROWS,
            cols=self.COLS,
            congruence_percentage=self.congruence_percentage,
        )
        return PuzzleGrid(cells=cells_2d, metadata=metadata)

    def _derive_new_seed(self, original_seed: int, attempt: int) -> int:
        """
        Derive a new seed from the original seed and attempt number.

        Args:
            original_seed: The original seed value.
            attempt: The current retry attempt number.

        Returns:
            A new seed value derived from the original.
        """
        return (original_seed * 31 + attempt) % (2**31)

    def _count_ink_colors(
        self, cells_2d: List[List[PuzzleCell]]
    ) -> Dict[ColorToken, int]:
        """
        Count ink color occurrences in a 2D grid.

        Args:
            cells_2d: 2D list of PuzzleCell objects.

        Returns:
            Dictionary mapping ColorToken to occurrence count.
        """
        ink_colors = []
        for row in cells_2d:
            for cell in row:
                ink_colors.append(cell.ink_color)
        return Counter(ink_colors)

    def _create_ink_distribution(self) -> List[ColorToken]:
        """
        Create a list of 64 ink colors with roughly equal distribution.

        Each of the 8 colors appears exactly 8 times for perfect balance.

        Returns:
            List of 64 ColorToken values representing ink colors.
        """
        color_tokens = list(ColorToken)
        cells_per_color = self.TOTAL_CELLS // len(color_tokens)  # 8

        ink_colors: List[ColorToken] = []
        for token in color_tokens:
            ink_colors.extend([token] * cells_per_color)

        # Shuffle to randomize initial distribution
        self._rng.shuffle(ink_colors)

        return ink_colors

    def _assign_words(self, ink_colors: List[ColorToken]) -> List[PuzzleCell]:
        """
        Assign word values to cells based on congruence percentage.

        For each cell, decide whether word should match ink color based
        on congruence_percentage. If incongruent, select a different ColorToken.

        Args:
            ink_colors: List of ink colors for each cell.

        Returns:
            List of PuzzleCell objects with word and ink_color assigned.
        """
        cells: List[PuzzleCell] = []
        all_colors = list(ColorToken)

        for ink_color in ink_colors:
            # Decide if this cell should be congruent (word == ink)
            is_congruent = self._rng.random() < self.congruence_percentage

            if is_congruent:
                word = ink_color
            else:
                # Select a different color for the word
                other_colors = [c for c in all_colors if c != ink_color]
                word = self._rng.choice(other_colors)

            cells.append(PuzzleCell(word=word, ink_color=ink_color))

        return cells

    def _reshape_to_grid(
        self, cells_flat: List[PuzzleCell]
    ) -> List[List[PuzzleCell]]:
        """
        Reshape a flat list of cells into a 2D grid.

        Args:
            cells_flat: Flat list of 64 PuzzleCell objects.

        Returns:
            2D list (8x8) of PuzzleCell objects.
        """
        grid: List[List[PuzzleCell]] = []
        for row_idx in range(self.ROWS):
            start = row_idx * self.COLS
            end = start + self.COLS
            grid.append(cells_flat[start:end])

        return grid
