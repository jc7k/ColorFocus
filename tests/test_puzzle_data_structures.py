"""
Tests for color labels and puzzle data structures.

These tests verify that:
1. All 8 ColorToken values have zh-TW labels defined
2. PuzzleCell dataclass contains word and inkColor fields
3. PuzzleGrid dataclass contains grid, metadata (seed, dimensions, congruence_percentage)
4. JSON serialization of puzzle structures works correctly

Updated for accessible color palette (2025-12-27):
- New 8-color palette: BLACK, BROWN, PURPLE, BLUE, GRAY, PINK, ORANGE, YELLOW
- Language key renamed from "chinese" to "zh-TW"
"""

import json

from backend.app.constants.colors import ColorToken
from backend.app.constants.color_labels import (
    COLOR_LABELS,
    Language,
    get_color_label,
)
from backend.app.models.puzzle import (
    PuzzleCell,
    PuzzleGrid,
    PuzzleMetadata,
)


class TestColorLabels:
    """Test that color labels are properly defined for all ColorToken values."""

    def test_all_color_tokens_have_chinese_labels(self):
        """Test that all 8 ColorToken values have zh-TW labels defined."""
        expected_tokens = [
            ColorToken.BLACK,
            ColorToken.BROWN,
            ColorToken.PURPLE,
            ColorToken.BLUE,
            ColorToken.GRAY,
            ColorToken.PINK,
            ColorToken.ORANGE,
            ColorToken.YELLOW,
        ]

        for token in expected_tokens:
            label = get_color_label(token, Language.ZH_TW)
            assert label is not None, f"Missing zh-TW label for {token}"
            assert len(label) > 0, f"Empty zh-TW label for {token}"

    def test_chinese_labels_match_prd_specification(self):
        """Test that zh-TW labels match new accessible palette specification."""
        expected_labels = {
            ColorToken.BLACK: "黑",
            ColorToken.BROWN: "棕",
            ColorToken.PURPLE: "紫",
            ColorToken.BLUE: "藍",
            ColorToken.GRAY: "灰",
            ColorToken.PINK: "粉",
            ColorToken.ORANGE: "橙",
            ColorToken.YELLOW: "黃",
        }

        for token, expected_label in expected_labels.items():
            actual_label = get_color_label(token, Language.ZH_TW)
            assert actual_label == expected_label, (
                f"zh-TW label mismatch for {token}: "
                f"expected '{expected_label}', got '{actual_label}'"
            )

    def test_all_color_tokens_have_english_labels(self):
        """Test that all 8 ColorToken values have English labels as fallback."""
        for token in ColorToken:
            label = get_color_label(token, Language.ENGLISH)
            assert label is not None, f"Missing English label for {token}"
            assert len(label) > 0, f"Empty English label for {token}"


class TestPuzzleDataStructures:
    """Test puzzle data structures (PuzzleCell, PuzzleMetadata, PuzzleGrid)."""

    def test_puzzle_cell_has_required_fields(self):
        """Test that PuzzleCell dataclass contains word and ink_color fields."""
        cell = PuzzleCell(word=ColorToken.BLUE, ink_color=ColorToken.ORANGE)

        assert hasattr(cell, "word"), "PuzzleCell missing 'word' field"
        assert hasattr(cell, "ink_color"), "PuzzleCell missing 'ink_color' field"
        assert cell.word == ColorToken.BLUE
        assert cell.ink_color == ColorToken.ORANGE

    def test_puzzle_metadata_has_required_fields(self):
        """Test that PuzzleMetadata has seed, rows, cols, congruence_percentage."""
        metadata = PuzzleMetadata(
            seed=12345,
            rows=8,
            cols=8,
            congruence_percentage=0.125,
        )

        assert hasattr(metadata, "seed"), "PuzzleMetadata missing 'seed' field"
        assert hasattr(metadata, "rows"), "PuzzleMetadata missing 'rows' field"
        assert hasattr(metadata, "cols"), "PuzzleMetadata missing 'cols' field"
        assert hasattr(metadata, "congruence_percentage"), (
            "PuzzleMetadata missing 'congruence_percentage' field"
        )
        assert metadata.seed == 12345
        assert metadata.rows == 8
        assert metadata.cols == 8
        assert metadata.congruence_percentage == 0.125

    def test_puzzle_grid_has_required_fields(self):
        """Test that PuzzleGrid contains cells and metadata."""
        cell = PuzzleCell(word=ColorToken.BLUE, ink_color=ColorToken.ORANGE)
        cells = [[cell]]
        metadata = PuzzleMetadata(seed=42, rows=1, cols=1, congruence_percentage=0.0)

        grid = PuzzleGrid(cells=cells, metadata=metadata)

        assert hasattr(grid, "cells"), "PuzzleGrid missing 'cells' field"
        assert hasattr(grid, "metadata"), "PuzzleGrid missing 'metadata' field"
        assert grid.cells == cells
        assert grid.metadata == metadata


class TestJsonSerialization:
    """Test JSON serialization of puzzle structures."""

    def test_puzzle_cell_serializes_to_json(self):
        """Test that PuzzleCell can be serialized to JSON-compatible dict."""
        cell = PuzzleCell(word=ColorToken.BLUE, ink_color=ColorToken.ORANGE)

        cell_dict = cell.to_dict()

        # Should be JSON-serializable
        json_str = json.dumps(cell_dict)
        assert json_str is not None

        # Check structure
        assert "word" in cell_dict
        assert "inkColor" in cell_dict
        assert cell_dict["word"] == "BLUE"
        assert cell_dict["inkColor"] == "ORANGE"

    def test_puzzle_grid_serializes_to_json(self):
        """Test that PuzzleGrid can be serialized to JSON-compatible dict."""
        cells = [
            [
                PuzzleCell(word=ColorToken.BLUE, ink_color=ColorToken.ORANGE),
                PuzzleCell(word=ColorToken.PURPLE, ink_color=ColorToken.PINK),
            ],
            [
                PuzzleCell(word=ColorToken.BLACK, ink_color=ColorToken.YELLOW),
                PuzzleCell(word=ColorToken.BROWN, ink_color=ColorToken.GRAY),
            ],
        ]
        metadata = PuzzleMetadata(seed=42, rows=2, cols=2, congruence_percentage=0.5)
        grid = PuzzleGrid(cells=cells, metadata=metadata)

        grid_dict = grid.to_dict()

        # Should be JSON-serializable
        json_str = json.dumps(grid_dict)
        assert json_str is not None

        # Check structure
        assert "grid" in grid_dict
        assert "metadata" in grid_dict
        assert grid_dict["metadata"]["seed"] == 42
        assert grid_dict["metadata"]["rows"] == 2
        assert grid_dict["metadata"]["cols"] == 2
        assert grid_dict["metadata"]["congruencePercentage"] == 0.5

        # Check grid structure
        assert len(grid_dict["grid"]) == 2
        assert len(grid_dict["grid"][0]) == 2
        assert grid_dict["grid"][0][0]["word"] == "BLUE"
        assert grid_dict["grid"][0][0]["inkColor"] == "ORANGE"
