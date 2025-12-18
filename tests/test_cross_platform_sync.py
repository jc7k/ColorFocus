"""
Cross-platform synchronization tests for Color Token System.

These tests verify that TypeScript and Python constants both match
the source JSON, ensuring build will fail if constants drift from
the single source of truth.

This test is part of Task Group 4: Cross-Platform Validation.
"""

import json
import re
from pathlib import Path


# Paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
COLORS_JSON_PATH = PROJECT_ROOT / "shared" / "colors.json"
PYTHON_COLORS_MODULE = PROJECT_ROOT / "backend" / "app" / "constants" / "colors.py"
TS_COLORS_MODULE = PROJECT_ROOT / "frontend" / "src" / "constants" / "colors.ts"


def load_source_colors() -> dict:
    """Load the source of truth colors.json file."""
    with open(COLORS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestCrossPlatformSynchronization:
    """
    Verify that both TypeScript and Python implementations match the source JSON.

    If these tests fail, it indicates drift between the source of truth and
    the platform-specific constants, which would break cross-platform consistency.
    """

    def test_python_constants_match_source_json(self):
        """
        Test that Python COLORS dictionary exactly matches source JSON hex values.

        This is a critical synchronization test - failure indicates the Python
        constants have drifted from the source of truth.
        """
        from backend.app.constants.colors import COLORS, ColorToken, ColorVariant

        source_colors = load_source_colors()
        mismatches = []

        for token_name, token_data in source_colors.items():
            token_enum = ColorToken(token_name)

            if token_enum not in COLORS:
                mismatches.append(f"Python missing token: {token_name}")
                continue

            for variant_name, expected_hex in token_data["variants"].items():
                variant_enum = ColorVariant(variant_name.upper())

                if variant_enum not in COLORS[token_enum]:
                    mismatches.append(f"Python missing variant: {token_name}.{variant_name}")
                    continue

                actual_hex = COLORS[token_enum][variant_enum]
                if actual_hex != expected_hex:
                    mismatches.append(
                        f"Python hex mismatch {token_name}.{variant_name}: "
                        f"expected {expected_hex}, got {actual_hex}"
                    )

        assert not mismatches, (
            f"Python constants have drifted from source JSON:\n"
            + "\n".join(f"  - {m}" for m in mismatches)
        )

    def test_typescript_imports_from_shared_json(self):
        """
        Test that TypeScript constants file imports from the shared JSON.

        This verifies the TypeScript implementation uses the single source of
        truth rather than maintaining duplicate color definitions.
        """
        assert TS_COLORS_MODULE.exists(), (
            f"TypeScript colors module not found at {TS_COLORS_MODULE}"
        )

        ts_content = TS_COLORS_MODULE.read_text(encoding="utf-8")

        # Verify it imports from shared colors.json
        # The import statement should reference the shared JSON file
        has_json_import = (
            "colors.json" in ts_content and
            ("import" in ts_content or "require" in ts_content)
        )

        assert has_json_import, (
            "TypeScript module should import from shared colors.json. "
            "Found no import statement referencing colors.json."
        )

        # Verify the import is from the correct path (shared directory)
        assert "../../../shared/colors.json" in ts_content or "@shared/colors.json" in ts_content, (
            "TypeScript should import from the shared directory (../../../shared/colors.json)"
        )

    def test_all_source_tokens_have_both_platform_implementations(self):
        """
        Test that every token in source JSON has implementations in both platforms.

        This ensures no tokens are accidentally omitted from either platform.
        """
        from backend.app.constants.colors import ColorToken as PyColorToken

        source_colors = load_source_colors()
        source_token_names = set(source_colors.keys())

        # Check Python has all tokens
        python_token_names = {token.value for token in PyColorToken}
        missing_in_python = source_token_names - python_token_names
        assert not missing_in_python, (
            f"Python ColorToken missing tokens: {missing_in_python}"
        )

        # Check TypeScript module references all tokens in the enum
        ts_content = TS_COLORS_MODULE.read_text(encoding="utf-8")
        missing_in_ts = []
        for token_name in source_token_names:
            # Look for enum declaration like: BLUE = 'BLUE'
            if f"{token_name} = '{token_name}'" not in ts_content:
                missing_in_ts.append(token_name)

        assert not missing_in_ts, (
            f"TypeScript ColorToken enum missing tokens: {missing_in_ts}"
        )


class TestSourceOfTruthIntegrity:
    """
    Verify that the source of truth JSON file maintains integrity.

    These tests provide an additional layer of validation that the JSON
    hasn't been corrupted or modified in ways that would break synchronization.
    """

    def test_source_json_has_expected_token_count(self):
        """Test that source JSON has exactly 8 color tokens."""
        source_colors = load_source_colors()

        expected_tokens = {"BLUE", "ORANGE", "PURPLE", "BLACK", "CYAN", "AMBER", "MAGENTA", "GRAY"}
        actual_tokens = set(source_colors.keys())

        assert actual_tokens == expected_tokens, (
            f"Source JSON token mismatch.\n"
            f"Expected: {expected_tokens}\n"
            f"Actual: {actual_tokens}\n"
            f"Missing: {expected_tokens - actual_tokens}\n"
            f"Extra: {actual_tokens - expected_tokens}"
        )

    def test_source_json_variant_structure_is_consistent(self):
        """
        Test that all tokens follow the expected variant structure.

        Most tokens: dark, base, bright
        BLACK: base, bright (dark is optional)
        """
        source_colors = load_source_colors()

        for token_name, token_data in source_colors.items():
            variants = set(token_data.get("variants", {}).keys())

            # base and bright are required for all tokens
            assert "base" in variants, f"{token_name} missing 'base' variant"
            assert "bright" in variants, f"{token_name} missing 'bright' variant"

            # dark is required for all tokens except BLACK
            if token_name != "BLACK":
                assert "dark" in variants, f"{token_name} missing 'dark' variant"
