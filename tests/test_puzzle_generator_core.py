"""
Core tests for puzzle generation service.

These tests verify basic puzzle generation functionality:
1. Generator produces valid 8x8 grids (64 cells total)
2. Same seed produces identical grids (reproducibility)
3. Different seeds produce different grids
4. Ink color distribution is roughly equal
5. Congruence percentage parameter affects word-ink matching
6. Metadata generation and language configuration
"""

from collections import Counter

from backend.app.constants.colors import ColorToken
from backend.app.constants.color_labels import Language
from backend.app.models.puzzle import PuzzleGrid
from backend.app.services.puzzle_generator import PuzzleGenerator


# New accessible palette tokens
NEW_PALETTE_TOKENS = [
    ColorToken.BLACK, ColorToken.BROWN, ColorToken.PURPLE, ColorToken.BLUE,
    ColorToken.GRAY, ColorToken.PINK, ColorToken.ORANGE, ColorToken.YELLOW
]

# Standard tier (4 colors) for default puzzles
STANDARD_TIER_COLORS = [
    ColorToken.BLACK, ColorToken.BLUE, ColorToken.ORANGE, ColorToken.YELLOW
]


class TestPuzzleGeneratorBasics:
    """Test basic puzzle generation functionality."""

    def test_generate_returns_8x8_grid(self):
        """Test that generate() returns an 8x8 grid (64 cells total)."""
        generator = PuzzleGenerator(seed=12345)
        puzzle = generator.generate()

        assert isinstance(puzzle, PuzzleGrid)
        assert len(puzzle.cells) == 8, "Grid should have 8 rows"
        for row in puzzle.cells:
            assert len(row) == 8, "Each row should have 8 columns"

        total_cells = sum(len(row) for row in puzzle.cells)
        assert total_cells == 64, f"Grid should have 64 cells, got {total_cells}"

    def test_same_seed_produces_identical_grids(self):
        """Test that same seed produces identical grids (reproducibility)."""
        seed = 42
        generator1 = PuzzleGenerator(seed=seed)
        generator2 = PuzzleGenerator(seed=seed)

        puzzle1 = generator1.generate()
        puzzle2 = generator2.generate()

        for r in range(8):
            for c in range(8):
                cell1 = puzzle1.cells[r][c]
                cell2 = puzzle2.cells[r][c]
                assert cell1.word == cell2.word
                assert cell1.ink_color == cell2.ink_color

    def test_different_seeds_produce_different_grids(self):
        """Test that different seeds produce different grids."""
        generator1 = PuzzleGenerator(seed=12345)
        generator2 = PuzzleGenerator(seed=67890)

        puzzle1 = generator1.generate()
        puzzle2 = generator2.generate()

        differences = 0
        for r in range(8):
            for c in range(8):
                cell1 = puzzle1.cells[r][c]
                cell2 = puzzle2.cells[r][c]
                if cell1.word != cell2.word or cell1.ink_color != cell2.ink_color:
                    differences += 1

        assert differences > 0, "Different seeds should produce different grids"


class TestColorDistribution:
    """Test ink color distribution in generated puzzles."""

    def test_ink_color_distribution_roughly_equal(self):
        """Test that ink color distribution is roughly equal based on color_count."""
        generator = PuzzleGenerator(seed=42, color_count=8)
        puzzle = generator.generate()

        ink_colors = []
        for row in puzzle.cells:
            for cell in row:
                ink_colors.append(cell.ink_color)

        counts = Counter(ink_colors)

        for token in NEW_PALETTE_TOKENS:
            count = counts.get(token, 0)
            assert 6 <= count <= 10, (
                f"Color {token} appears {count} times, expected 6-10"
            )

    def test_ink_color_distribution_with_4_colors(self):
        """Test that ink color distribution works with default 4 colors."""
        generator = PuzzleGenerator(seed=42)
        puzzle = generator.generate()

        assert puzzle.metadata.color_count == 4

        ink_colors = []
        for row in puzzle.cells:
            for cell in row:
                ink_colors.append(cell.ink_color)

        counts = Counter(ink_colors)

        for token in STANDARD_TIER_COLORS:
            count = counts.get(token, 0)
            assert 14 <= count <= 18, (
                f"Color {token} appears {count} times, expected 14-18"
            )

        inactive_colors = [t for t in NEW_PALETTE_TOKENS if t not in STANDARD_TIER_COLORS]
        for token in inactive_colors:
            assert counts.get(token, 0) == 0


class TestCongruenceControl:
    """Test congruence percentage affects word-ink matching."""

    def test_congruence_percentage_affects_matching(self):
        """Test that congruence percentage parameter affects word-ink matching."""
        low_gen = PuzzleGenerator(seed=100, congruence_percentage=0.0)
        low_puzzle = low_gen.generate()

        high_gen = PuzzleGenerator(seed=100, congruence_percentage=1.0)
        high_puzzle = high_gen.generate()

        def count_congruent(puzzle: PuzzleGrid) -> int:
            congruent = 0
            for row in puzzle.cells:
                for cell in row:
                    if cell.word == cell.ink_color:
                        congruent += 1
            return congruent

        low_congruent = count_congruent(low_puzzle)
        high_congruent = count_congruent(high_puzzle)

        assert high_congruent > low_congruent

    def test_default_congruence_is_low(self):
        """Test that default congruence is low (mostly incongruent for Stroop)."""
        generator = PuzzleGenerator(seed=42)

        assert generator.congruence_percentage == 0.125

        puzzle = generator.generate()

        congruent = 0
        for row in puzzle.cells:
            for cell in row:
                if cell.word == cell.ink_color:
                    congruent += 1

        assert congruent <= 16


class TestMetadata:
    """Test puzzle metadata generation."""

    def test_auto_generated_seed_in_metadata(self):
        """Test that auto-generated seed is included in metadata."""
        generator = PuzzleGenerator()
        puzzle = generator.generate()

        assert puzzle.metadata.seed is not None
        assert isinstance(puzzle.metadata.seed, int)
        assert puzzle.metadata.seed > 0

    def test_metadata_includes_all_required_fields(self):
        """Test that metadata includes seed, dimensions, and congruence_percentage."""
        generator = PuzzleGenerator(seed=12345, congruence_percentage=0.25)
        puzzle = generator.generate()

        assert puzzle.metadata.seed == 12345
        assert puzzle.metadata.rows == 8
        assert puzzle.metadata.cols == 8
        assert puzzle.metadata.congruence_percentage == 0.25


class TestLanguageConfiguration:
    """Test language configuration support with new zh-TW locale."""

    def test_language_parameter_accepted(self):
        """Test that language parameter is accepted by generator."""
        gen_tw = PuzzleGenerator(seed=42, language=Language.ZH_TW)
        assert gen_tw.language == Language.ZH_TW

        gen_en = PuzzleGenerator(seed=42, language=Language.ENGLISH)
        assert gen_en.language == Language.ENGLISH

    def test_default_language_is_zh_tw(self):
        """Test that default language is zh-TW (Traditional Chinese)."""
        generator = PuzzleGenerator(seed=42)
        assert generator.language == Language.ZH_TW
