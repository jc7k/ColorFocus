"""
Tests for puzzle generation service.

These tests verify that:
1. Generator produces valid 8x8 grids (64 cells total)
2. Same seed produces identical grids (reproducibility)
3. Different seeds produce different grids
4. Ink color distribution is roughly equal (each color ~8 times, within tolerance)
5. Congruence percentage parameter affects word-ink matching
6. Default congruence is low (mostly incongruent for Stroop effect)
7. Auto-generated seed is included in metadata when none provided
8. Distribution validator catches skewed distributions
9. JSON output is correct and serializable
"""

import json
from collections import Counter

from backend.app.constants.colors import ColorToken
from backend.app.constants.color_labels import Language
from backend.app.models.puzzle import PuzzleCell, PuzzleGrid, PuzzleMetadata
from backend.app.services.puzzle_generator import (
    PuzzleGenerator,
    DistributionValidator,
    ValidationResult,
)


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

        # Verify total cell count
        total_cells = sum(len(row) for row in puzzle.cells)
        assert total_cells == 64, f"Grid should have 64 cells, got {total_cells}"

    def test_same_seed_produces_identical_grids(self):
        """Test that same seed produces identical grids (reproducibility)."""
        seed = 42
        generator1 = PuzzleGenerator(seed=seed)
        generator2 = PuzzleGenerator(seed=seed)

        puzzle1 = generator1.generate()
        puzzle2 = generator2.generate()

        # Compare grid contents
        for r in range(8):
            for c in range(8):
                cell1 = puzzle1.cells[r][c]
                cell2 = puzzle2.cells[r][c]
                assert cell1.word == cell2.word, (
                    f"Mismatch at ({r},{c}): word {cell1.word} != {cell2.word}"
                )
                assert cell1.ink_color == cell2.ink_color, (
                    f"Mismatch at ({r},{c}): ink_color {cell1.ink_color} != {cell2.ink_color}"
                )

    def test_different_seeds_produce_different_grids(self):
        """Test that different seeds produce different grids."""
        generator1 = PuzzleGenerator(seed=12345)
        generator2 = PuzzleGenerator(seed=67890)

        puzzle1 = generator1.generate()
        puzzle2 = generator2.generate()

        # At least some cells should differ
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
        # Test with 8 colors (legacy behavior)
        generator = PuzzleGenerator(seed=42, color_count=8)
        puzzle = generator.generate()

        # Count ink colors
        ink_colors = []
        for row in puzzle.cells:
            for cell in row:
                ink_colors.append(cell.ink_color)

        counts = Counter(ink_colors)

        # Each of 8 colors should appear approximately 8 times (64/8)
        # Tolerance: allow 6-10 appearances per color
        for token in ColorToken:
            count = counts.get(token, 0)
            assert 6 <= count <= 10, (
                f"Color {token} appears {count} times, expected 6-10"
            )

    def test_ink_color_distribution_with_4_colors(self):
        """Test that ink color distribution works with default 4 colors."""
        generator = PuzzleGenerator(seed=42)  # Default is 4 colors
        puzzle = generator.generate()

        assert puzzle.metadata.color_count == 4

        # Count ink colors
        ink_colors = []
        for row in puzzle.cells:
            for cell in row:
                ink_colors.append(cell.ink_color)

        counts = Counter(ink_colors)

        # With 4 colors, each should appear ~16 times (64/4)
        active_colors = [ColorToken.BLUE, ColorToken.ORANGE, ColorToken.PURPLE, ColorToken.BLACK]
        for token in active_colors:
            count = counts.get(token, 0)
            assert 14 <= count <= 18, (
                f"Color {token} appears {count} times, expected 14-18"
            )

        # Inactive colors should not appear
        for token in ColorToken:
            if token not in active_colors:
                assert counts.get(token, 0) == 0, (
                    f"Inactive color {token} should not appear"
                )


class TestCongruenceControl:
    """Test congruence percentage affects word-ink matching."""

    def test_congruence_percentage_affects_matching(self):
        """Test that congruence percentage parameter affects word-ink matching."""
        # Low congruence (mostly incongruent)
        low_gen = PuzzleGenerator(seed=100, congruence_percentage=0.0)
        low_puzzle = low_gen.generate()

        # High congruence (mostly congruent)
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

        # High congruence puzzle should have more matching cells
        assert high_congruent > low_congruent, (
            f"High congruence ({high_congruent}) should exceed low ({low_congruent})"
        )

    def test_default_congruence_is_low(self):
        """Test that default congruence is low (mostly incongruent for Stroop)."""
        generator = PuzzleGenerator(seed=42)  # Using default congruence

        assert generator.congruence_percentage == 0.125, (
            f"Default congruence should be 0.125, got {generator.congruence_percentage}"
        )

        puzzle = generator.generate()

        # Count congruent cells
        congruent = 0
        for row in puzzle.cells:
            for cell in row:
                if cell.word == cell.ink_color:
                    congruent += 1

        # With 0.125 congruence, expect roughly 8 congruent cells (64 * 0.125)
        # Allow some tolerance: 0-16 is acceptable (low congruence means mostly incongruent)
        assert congruent <= 16, (
            f"Default should be mostly incongruent, got {congruent} congruent cells"
        )


class TestMetadata:
    """Test puzzle metadata generation."""

    def test_auto_generated_seed_in_metadata(self):
        """Test that auto-generated seed is included in metadata when none provided."""
        generator = PuzzleGenerator()  # No seed provided
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
    """Test language configuration support."""

    def test_language_parameter_accepted(self):
        """Test that language parameter is accepted by generator."""
        # Test Chinese (default)
        gen_cn = PuzzleGenerator(seed=42, language=Language.CHINESE)
        assert gen_cn.language == Language.CHINESE

        # Test English
        gen_en = PuzzleGenerator(seed=42, language=Language.ENGLISH)
        assert gen_en.language == Language.ENGLISH

    def test_default_language_is_chinese(self):
        """Test that default language is Chinese."""
        generator = PuzzleGenerator(seed=42)
        assert generator.language == Language.CHINESE


class TestDistributionValidation:
    """Test distribution validation functionality."""

    def test_validator_rejects_heavily_skewed_distribution(self):
        """Test that validator rejects grids with heavily skewed color distribution."""
        validator = DistributionValidator(min_count=6, max_count=10)

        # Create a heavily skewed count distribution
        skewed_counts = {
            ColorToken.BLUE: 20,
            ColorToken.ORANGE: 2,
            ColorToken.PURPLE: 8,
            ColorToken.BLACK: 8,
            ColorToken.CYAN: 8,
            ColorToken.AMBER: 8,
            ColorToken.MAGENTA: 8,
            ColorToken.GRAY: 2,
        }

        result = validator.validate(skewed_counts)

        assert not result.is_valid, "Validator should reject skewed distribution"
        assert len(result.issues) > 0, "Validator should report issues"

    def test_validator_accepts_distribution_within_tolerance(self):
        """Test that validator accepts grids within acceptable tolerance."""
        validator = DistributionValidator(min_count=6, max_count=10)

        # Create a balanced distribution (exactly 8 each)
        balanced_counts = {token: 8 for token in ColorToken}

        result = validator.validate(balanced_counts)

        assert result.is_valid, "Validator should accept balanced distribution"
        assert len(result.issues) == 0, "Validator should report no issues"

    def test_validator_accepts_minor_variation(self):
        """Test that validator accepts distribution with minor variation."""
        validator = DistributionValidator(min_count=6, max_count=10)

        # Create distribution with minor variation (6-10 range)
        varied_counts = {
            ColorToken.BLUE: 6,
            ColorToken.ORANGE: 10,
            ColorToken.PURPLE: 7,
            ColorToken.BLACK: 9,
            ColorToken.CYAN: 8,
            ColorToken.AMBER: 8,
            ColorToken.MAGENTA: 8,
            ColorToken.GRAY: 8,
        }

        result = validator.validate(varied_counts)

        assert result.is_valid, "Validator should accept minor variation"


class TestJsonSerialization:
    """Test JSON serialization of puzzle structures."""

    def test_json_output_format_matches_expected_structure(self):
        """Test JSON output format matches expected structure."""
        generator = PuzzleGenerator(seed=12345)
        puzzle = generator.generate()

        data = puzzle.to_dict()

        # Verify top-level structure
        assert "grid" in data, "Output should have 'grid' key"
        assert "metadata" in data, "Output should have 'metadata' key"

        # Verify grid structure
        assert len(data["grid"]) == 8, "Grid should have 8 rows"
        assert len(data["grid"][0]) == 8, "Each row should have 8 columns"

        # Verify cell structure
        first_cell = data["grid"][0][0]
        assert "word" in first_cell, "Cell should have 'word' key"
        assert "inkColor" in first_cell, "Cell should have 'inkColor' key"

        # Verify metadata structure
        meta = data["metadata"]
        assert "seed" in meta, "Metadata should have 'seed' key"
        assert "rows" in meta, "Metadata should have 'rows' key"
        assert "cols" in meta, "Metadata should have 'cols' key"
        assert "congruence_percentage" in meta, "Metadata should have 'congruence_percentage' key"

    def test_to_dict_produces_json_serializable_output(self):
        """Test that to_dict() produces JSON-serializable output."""
        generator = PuzzleGenerator(seed=12345)
        puzzle = generator.generate()

        data = puzzle.to_dict()

        # Verify it can be serialized to JSON without errors
        json_string = json.dumps(data)
        assert isinstance(json_string, str)

        # Verify it can be deserialized back
        parsed = json.loads(json_string)
        assert parsed == data

    def test_color_tokens_serialized_as_strings(self):
        """Test that ColorToken values are serialized as strings."""
        generator = PuzzleGenerator(seed=12345)
        puzzle = generator.generate()

        data = puzzle.to_dict()

        # Check that all word and inkColor values are strings
        for row in data["grid"]:
            for cell in row:
                assert isinstance(cell["word"], str), "word should be string"
                assert isinstance(cell["inkColor"], str), "inkColor should be string"


# =============================================================================
# Task Group 4: Strategic Gap-Filling Tests (up to 5 additional tests)
# =============================================================================


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
        large_seed = 2**30 - 1  # Large but within 32-bit bounds
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

        # With 0.0 congruence, there should be no congruent cells
        assert congruent_count == 0, (
            f"Expected 0 congruent cells with 0.0 congruence, got {congruent_count}"
        )

    def test_full_congruence_produces_all_matches(self):
        """Test that 1.0 congruence produces all word-ink matches."""
        generator = PuzzleGenerator(seed=42, congruence_percentage=1.0)
        puzzle = generator.generate()

        congruent_count = 0
        for row in puzzle.cells:
            for cell in row:
                if cell.word == cell.ink_color:
                    congruent_count += 1

        # With 1.0 congruence, all 64 cells should be congruent
        assert congruent_count == 64, (
            f"Expected 64 congruent cells with 1.0 congruence, got {congruent_count}"
        )


class TestEndToEndGenerationWorkflow:
    """Integration test for full puzzle generation workflow."""

    def test_full_generation_workflow(self):
        """Test complete generation workflow: create, generate, serialize, share."""
        # Step 1: Create generator with specific parameters
        seed = 99999
        congruence = 0.25
        generator = PuzzleGenerator(
            seed=seed,
            congruence_percentage=congruence,
            language=Language.CHINESE,
        )

        # Step 2: Generate puzzle
        puzzle = generator.generate()

        # Step 3: Verify grid structure
        assert len(puzzle.cells) == 8
        assert all(len(row) == 8 for row in puzzle.cells)

        # Step 4: Verify metadata for traceability/sharing
        assert puzzle.metadata.seed == seed
        assert puzzle.metadata.congruence_percentage == congruence
        assert puzzle.metadata.rows == 8
        assert puzzle.metadata.cols == 8

        # Step 5: Serialize for API response
        puzzle_dict = puzzle.to_dict()
        json_output = json.dumps(puzzle_dict)
        assert len(json_output) > 0

        # Step 6: Verify reproducibility with same seed (simulate sharing)
        generator2 = PuzzleGenerator(seed=seed, congruence_percentage=congruence)
        puzzle2 = generator2.generate()

        # Verify identical output
        for r in range(8):
            for c in range(8):
                assert puzzle.cells[r][c].word == puzzle2.cells[r][c].word
                assert puzzle.cells[r][c].ink_color == puzzle2.cells[r][c].ink_color
