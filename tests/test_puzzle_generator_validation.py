"""
Validation and serialization tests for puzzle generation service.

These tests verify:
1. Distribution validator catches skewed distributions
2. JSON output is correct and serializable
3. Edge case seeds and extreme congruence values
4. End-to-end generation workflow
5. New accessible palette color usage
"""

import json

from backend.app.constants.colors import ColorToken
from backend.app.constants.color_labels import Language
from backend.app.models.puzzle import PuzzleGrid
from backend.app.services.puzzle_generator import PuzzleGenerator
from backend.app.services.distribution_validator import (
    DistributionValidator,
    ValidationResult,
)


# New accessible palette tokens
NEW_PALETTE_TOKENS = [
    ColorToken.BLACK, ColorToken.BROWN, ColorToken.PURPLE, ColorToken.BLUE,
    ColorToken.GRAY, ColorToken.PINK, ColorToken.ORANGE, ColorToken.YELLOW
]

# Standard tier (4 colors) for default puzzles
STANDARD_TIER_COLORS = [
    ColorToken.BLACK, ColorToken.BLUE, ColorToken.ORANGE, ColorToken.YELLOW
]


class TestDistributionValidation:
    """Test distribution validation functionality with new accessible palette."""

    def test_validator_rejects_heavily_skewed_distribution(self):
        """Test that validator rejects grids with heavily skewed color distribution."""
        validator = DistributionValidator(min_count=6, max_count=10)

        skewed_counts = {
            ColorToken.BLUE: 20,
            ColorToken.ORANGE: 2,
            ColorToken.PURPLE: 8,
            ColorToken.BLACK: 8,
            ColorToken.BROWN: 8,
            ColorToken.PINK: 8,
            ColorToken.YELLOW: 8,
            ColorToken.GRAY: 2,
        }

        result = validator.validate(skewed_counts)

        assert not result.is_valid
        assert len(result.issues) > 0

    def test_validator_accepts_distribution_within_tolerance(self):
        """Test that validator accepts grids within acceptable tolerance."""
        validator = DistributionValidator(min_count=6, max_count=10)

        balanced_counts = {token: 8 for token in NEW_PALETTE_TOKENS}

        result = validator.validate(balanced_counts)

        assert result.is_valid
        assert len(result.issues) == 0

    def test_validator_accepts_minor_variation(self):
        """Test that validator accepts distribution with minor variation."""
        validator = DistributionValidator(min_count=6, max_count=10)

        varied_counts = {
            ColorToken.BLUE: 6,
            ColorToken.ORANGE: 10,
            ColorToken.PURPLE: 7,
            ColorToken.BLACK: 9,
            ColorToken.BROWN: 8,
            ColorToken.PINK: 8,
            ColorToken.YELLOW: 8,
            ColorToken.GRAY: 8,
        }

        result = validator.validate(varied_counts)

        assert result.is_valid


class TestJsonSerialization:
    """Test JSON serialization of puzzle structures."""

    def test_json_output_format_matches_expected_structure(self):
        """Test JSON output format matches expected structure."""
        generator = PuzzleGenerator(seed=12345)
        puzzle = generator.generate()

        data = puzzle.to_dict()

        assert "grid" in data
        assert "metadata" in data
        assert len(data["grid"]) == 8
        assert len(data["grid"][0]) == 8

        first_cell = data["grid"][0][0]
        assert "word" in first_cell
        assert "inkColor" in first_cell

        meta = data["metadata"]
        assert "seed" in meta
        assert "rows" in meta
        assert "cols" in meta
        assert "congruence_percentage" in meta

    def test_to_dict_produces_json_serializable_output(self):
        """Test that to_dict() produces JSON-serializable output."""
        generator = PuzzleGenerator(seed=12345)
        puzzle = generator.generate()

        data = puzzle.to_dict()

        json_string = json.dumps(data)
        assert isinstance(json_string, str)

        parsed = json.loads(json_string)
        assert parsed == data

    def test_color_tokens_serialized_as_strings(self):
        """Test that ColorToken values are serialized as strings."""
        generator = PuzzleGenerator(seed=12345)
        puzzle = generator.generate()

        data = puzzle.to_dict()

        for row in data["grid"]:
            for cell in row:
                assert isinstance(cell["word"], str)
                assert isinstance(cell["inkColor"], str)


class TestEdgeCaseSeeds:
    """Test edge case seed values for robustness."""

    def test_seed_zero_produces_valid_grid(self):
        """Test that seed=0 produces a valid 8x8 grid."""
        generator = PuzzleGenerator(seed=0)
        puzzle = generator.generate()

        assert isinstance(puzzle, PuzzleGrid)
        assert len(puzzle.cells) == 8
        assert all(len(row) == 8 for row in puzzle.cells)
        assert puzzle.metadata.seed == 0

    def test_very_large_seed_produces_valid_grid(self):
        """Test that a very large seed value produces a valid grid."""
        large_seed = 2**30 - 1
        generator = PuzzleGenerator(seed=large_seed)
        puzzle = generator.generate()

        assert isinstance(puzzle, PuzzleGrid)
        assert len(puzzle.cells) == 8
        assert all(len(row) == 8 for row in puzzle.cells)
        assert puzzle.metadata.seed == large_seed


class TestExtremeCongruenceValues:
    """Test extreme congruence values (0.0 and 1.0)."""

    def test_zero_congruence_produces_no_matches(self):
        """Test that 0.0 congruence produces zero word-ink matches."""
        generator = PuzzleGenerator(seed=42, congruence_percentage=0.0)
        puzzle = generator.generate()

        congruent_count = 0
        for row in puzzle.cells:
            for cell in row:
                if cell.word == cell.ink_color:
                    congruent_count += 1

        assert congruent_count == 0

    def test_full_congruence_produces_all_matches(self):
        """Test that 1.0 congruence produces all word-ink matches."""
        generator = PuzzleGenerator(seed=42, congruence_percentage=1.0)
        puzzle = generator.generate()

        congruent_count = 0
        for row in puzzle.cells:
            for cell in row:
                if cell.word == cell.ink_color:
                    congruent_count += 1

        assert congruent_count == 64


class TestEndToEndGenerationWorkflow:
    """Integration test for full puzzle generation workflow."""

    def test_full_generation_workflow(self):
        """Test complete generation workflow: create, generate, serialize, share."""
        seed = 99999
        congruence = 0.25
        generator = PuzzleGenerator(
            seed=seed,
            congruence_percentage=congruence,
            language=Language.ZH_TW,
        )

        puzzle = generator.generate()

        assert len(puzzle.cells) == 8
        assert all(len(row) == 8 for row in puzzle.cells)

        assert puzzle.metadata.seed == seed
        assert puzzle.metadata.congruence_percentage == congruence
        assert puzzle.metadata.rows == 8
        assert puzzle.metadata.cols == 8

        puzzle_dict = puzzle.to_dict()
        json_output = json.dumps(puzzle_dict)
        assert len(json_output) > 0

        generator2 = PuzzleGenerator(seed=seed, congruence_percentage=congruence)
        puzzle2 = generator2.generate()

        for r in range(8):
            for c in range(8):
                assert puzzle.cells[r][c].word == puzzle2.cells[r][c].word
                assert puzzle.cells[r][c].ink_color == puzzle2.cells[r][c].ink_color


class TestNewAccessiblePaletteColors:
    """Test that puzzle generation uses the new accessible color palette."""

    def test_generated_colors_are_from_new_palette(self):
        """Test that all generated ink colors are from the new accessible palette."""
        generator = PuzzleGenerator(seed=42, color_count=8)
        puzzle = generator.generate()

        for row in puzzle.cells:
            for cell in row:
                assert cell.ink_color in NEW_PALETTE_TOKENS
                assert cell.word in NEW_PALETTE_TOKENS

    def test_accessible_tier_uses_only_black_and_yellow(self):
        """Test that 2-color 'Accessible' tier uses only BLACK and YELLOW."""
        generator = PuzzleGenerator(seed=42, color_count=2)
        puzzle = generator.generate()

        accessible_colors = [ColorToken.BLACK, ColorToken.YELLOW]

        for row in puzzle.cells:
            for cell in row:
                assert cell.ink_color in accessible_colors
                assert cell.word in accessible_colors

    def test_standard_tier_uses_four_colors(self):
        """Test that 4-color 'Standard' tier uses BLACK, BLUE, ORANGE, YELLOW."""
        generator = PuzzleGenerator(seed=42, color_count=4)
        puzzle = generator.generate()

        for row in puzzle.cells:
            for cell in row:
                assert cell.ink_color in STANDARD_TIER_COLORS
                assert cell.word in STANDARD_TIER_COLORS
