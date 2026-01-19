"""
Tests for Stroop interference optimization in puzzle generation.

The optimization swaps cell positions to increase adjacent Stroop interference
without changing the overall color distribution.
"""

from collections import Counter

import pytest

from backend.app.constants.colors import ColorToken
from backend.app.models.puzzle import PuzzleCell
from backend.app.services.puzzle_generator import PuzzleGenerator


class TestStroopOptimization:
    """Tests for the Stroop interference optimization functions."""

    def test_get_adjacent_indices_corner(self):
        """Corner cells should have exactly 2 adjacent indices."""
        gen = PuzzleGenerator(seed=42)

        # Top-left corner (index 0) in 4x4 grid
        adj = gen._get_adjacent_indices(0, grid_size=4)
        assert len(adj) == 2
        assert set(adj) == {1, 4}  # right, down

        # Bottom-right corner (index 15) in 4x4 grid
        adj = gen._get_adjacent_indices(15, grid_size=4)
        assert len(adj) == 2
        assert set(adj) == {14, 11}  # left, up

    def test_get_adjacent_indices_edge(self):
        """Edge cells (non-corner) should have exactly 3 adjacent indices."""
        gen = PuzzleGenerator(seed=42)

        # Top edge, middle (index 1) in 4x4 grid
        adj = gen._get_adjacent_indices(1, grid_size=4)
        assert len(adj) == 3
        assert set(adj) == {0, 2, 5}  # left, right, down

    def test_get_adjacent_indices_center(self):
        """Center cells should have exactly 4 adjacent indices."""
        gen = PuzzleGenerator(seed=42)

        # Center cell (index 5) in 4x4 grid
        adj = gen._get_adjacent_indices(5, grid_size=4)
        assert len(adj) == 4
        assert set(adj) == {1, 4, 6, 9}  # up, left, right, down

    def test_interference_at_counts_correctly(self):
        """Interference count should include both directions of matching."""
        gen = PuzzleGenerator(seed=42)

        # Create a 2x2 grid where we can predict interference
        # Cell 0: word=BLUE, ink=BLACK
        # Cell 1: word=BLACK, ink=BLUE  <- word matches cell 0's ink
        # Cell 2: word=YELLOW, ink=ORANGE
        # Cell 3: word=ORANGE, ink=YELLOW
        cells = [
            PuzzleCell(word=ColorToken.BLUE, ink_color=ColorToken.BLACK),
            PuzzleCell(word=ColorToken.BLACK, ink_color=ColorToken.BLUE),
            PuzzleCell(word=ColorToken.YELLOW, ink_color=ColorToken.ORANGE),
            PuzzleCell(word=ColorToken.ORANGE, ink_color=ColorToken.YELLOW),
        ]

        # Cell 0 neighbors: cell 1 (right), cell 2 (down)
        # Cell 0 ink is BLACK, cell 1 word is BLACK -> interference!
        # Cell 1 ink is BLUE, cell 0 word is BLUE -> interference!
        interference_0 = gen._interference_at(cells, 0, grid_size=2)
        assert interference_0 == 2  # Both directions match

    def test_optimization_increases_interference(self):
        """Optimization should increase or maintain interference pair count."""
        gen = PuzzleGenerator(seed=12345, color_count=4)

        # Create cells without optimization
        ink_colors = gen._create_ink_distribution()
        cells_flat = gen._assign_words(ink_colors)
        gen._rng.shuffle(cells_flat)

        # Count interference before optimization
        before_count = sum(
            gen._interference_at(cells_flat, i, gen.COLS)
            for i in range(len(cells_flat))
        )

        # Optimize
        optimized = gen._optimize_stroop_interference(cells_flat, gen.COLS)

        # Count interference after optimization
        after_count = sum(
            gen._interference_at(optimized, i, gen.COLS)
            for i in range(len(optimized))
        )

        # Should be at least as good (greedy algorithm)
        assert after_count >= before_count

    def test_optimization_preserves_color_distribution(self):
        """Swaps must not change the count of each ink color."""
        gen = PuzzleGenerator(seed=54321, color_count=4)

        # Create cells
        ink_colors = gen._create_ink_distribution()
        cells_flat = gen._assign_words(ink_colors)
        gen._rng.shuffle(cells_flat)

        # Count ink colors before
        before_ink = Counter(c.ink_color for c in cells_flat)
        before_word = Counter(c.word for c in cells_flat)

        # Optimize
        optimized = gen._optimize_stroop_interference(cells_flat, gen.COLS)

        # Count ink colors after
        after_ink = Counter(c.ink_color for c in optimized)
        after_word = Counter(c.word for c in optimized)

        # Distribution must be preserved
        assert before_ink == after_ink
        assert before_word == after_word

    def test_optimization_is_deterministic(self):
        """Same seed should produce same optimized puzzle."""
        puzzle1 = PuzzleGenerator(seed=99999, color_count=4).generate()
        puzzle2 = PuzzleGenerator(seed=99999, color_count=4).generate()

        # Flatten both grids and compare
        flat1 = [cell for row in puzzle1.cells for cell in row]
        flat2 = [cell for row in puzzle2.cells for cell in row]

        for c1, c2 in zip(flat1, flat2):
            assert c1.word == c2.word
            assert c1.ink_color == c2.ink_color

    def test_optimization_with_small_grid(self):
        """Optimization should work with 3x3 grid (accessible mode)."""
        # Use a generator configured for smaller puzzle
        gen = PuzzleGenerator(seed=11111, color_count=2)

        # Manually create a 3x3 test
        cells = [
            PuzzleCell(word=ColorToken.BLACK, ink_color=ColorToken.YELLOW),
            PuzzleCell(word=ColorToken.YELLOW, ink_color=ColorToken.BLACK),
            PuzzleCell(word=ColorToken.BLACK, ink_color=ColorToken.YELLOW),
            PuzzleCell(word=ColorToken.YELLOW, ink_color=ColorToken.BLACK),
            PuzzleCell(word=ColorToken.BLACK, ink_color=ColorToken.YELLOW),
            PuzzleCell(word=ColorToken.YELLOW, ink_color=ColorToken.BLACK),
            PuzzleCell(word=ColorToken.BLACK, ink_color=ColorToken.YELLOW),
            PuzzleCell(word=ColorToken.YELLOW, ink_color=ColorToken.BLACK),
            PuzzleCell(word=ColorToken.BLACK, ink_color=ColorToken.YELLOW),
        ]

        # Should not raise
        optimized = gen._optimize_stroop_interference(cells, grid_size=3)

        # Should preserve cell count
        assert len(optimized) == 9

    def test_optimization_handles_maximum_interference(self):
        """Optimization should handle already-optimal grids gracefully."""
        gen = PuzzleGenerator(seed=77777, color_count=2)

        # Create a grid that's already highly interfering
        # Alternating pattern maximizes interference
        cells = []
        for i in range(16):
            if i % 2 == 0:
                cells.append(
                    PuzzleCell(word=ColorToken.BLACK, ink_color=ColorToken.YELLOW)
                )
            else:
                cells.append(
                    PuzzleCell(word=ColorToken.YELLOW, ink_color=ColorToken.BLACK)
                )

        # Should complete without error
        optimized = gen._optimize_stroop_interference(cells, grid_size=4)

        # Should still have same cells
        assert len(optimized) == 16

    def test_full_generate_includes_optimization(self):
        """Full puzzle generation should produce optimized grids."""
        # Generate two puzzles with same seed
        puzzle = PuzzleGenerator(seed=42424, color_count=4).generate()

        # Verify grid structure is intact
        assert len(puzzle.cells) == 8
        assert all(len(row) == 8 for row in puzzle.cells)

        # Verify each cell has word and ink_color
        for row in puzzle.cells:
            for cell in row:
                assert cell.word is not None
                assert cell.ink_color is not None
                assert isinstance(cell.word, ColorToken)
                assert isinstance(cell.ink_color, ColorToken)
