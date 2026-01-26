"""
Grid container and CSS tests for ColorFocus.

Task Group 1: Container and Cell CSS Updates.
Tests verify container max-width, mobile behavior, and responsive scaling.
"""

import re
from conftest import load_puzzle_css


class TestContainerMaxWidth:
    """
    Verify container max-width has been updated from 520px to 500px.
    """

    def test_puzzle_grid_max_width_is_500px(self):
        """Test that .puzzle-grid max-width is set to 500px."""
        css = load_puzzle_css()
        puzzle_grid_match = re.search(
            r'\.puzzle-grid\s*\{[^}]*max-width:\s*500px',
            css,
            re.DOTALL
        )
        assert puzzle_grid_match is not None, (
            ".puzzle-grid should have max-width: 500px"
        )

    def test_container_uses_max_width_not_fixed_width(self):
        """Test that container uses max-width (not fixed width) to allow scaling."""
        css = load_puzzle_css()
        assert 'max-width:' in css or 'max-width :' in css, (
            "Container should use max-width for responsive scaling"
        )
        puzzle_grid_section = re.search(
            r'\.puzzle-grid\s*\{[^}]+\}',
            css,
            re.DOTALL
        )
        if puzzle_grid_section:
            section_text = puzzle_grid_section.group(0)
            has_only_max_width = 'max-width' in section_text
            assert has_only_max_width, (
                ".puzzle-grid should use max-width for scaling, not fixed width"
            )

    def test_container_centered_with_auto_margin(self):
        """Test that container remains centered with margin: 0 auto."""
        css = load_puzzle_css()
        puzzle_grid_match = re.search(
            r'\.puzzle-grid\s*\{[^}]*margin:\s*0\s+auto',
            css,
            re.DOTALL
        )
        assert puzzle_grid_match is not None, (
            ".puzzle-grid should have margin: 0 auto for centering"
        )


class TestMobileContainerBehavior:
    """
    Verify mobile viewport behavior remains functional.
    """

    def test_mobile_media_query_exists_for_480px(self):
        """Test that mobile media query exists for 480px viewport."""
        css = load_puzzle_css()
        assert '@media (max-width: 480px)' in css, (
            "Mobile media query for 480px should exist"
        )

    def test_mobile_puzzle_grid_uses_full_width(self):
        """Test that mobile puzzle grid uses 100% width."""
        css = load_puzzle_css()
        mobile_section = re.search(
            r'@media\s*\(\s*max-width:\s*480px\s*\)\s*\{[^@]+',
            css,
            re.DOTALL
        )
        assert mobile_section is not None, (
            "480px mobile media query should exist"
        )
        mobile_css = mobile_section.group(0)
        assert 'width: 100%' in mobile_css or 'width:100%' in mobile_css, (
            "Mobile puzzle-grid should use width: 100%"
        )

    def test_mobile_puzzle_grid_has_reduced_gap(self):
        """Test that mobile puzzle grid has reduced gap (1-2px for compact layout)."""
        css = load_puzzle_css()
        mobile_section = re.search(
            r'@media\s*\(\s*max-width:\s*480px\s*\)\s*\{[^@]+',
            css,
            re.DOTALL
        )
        assert mobile_section is not None, (
            "480px mobile media query should exist"
        )
        mobile_css = mobile_section.group(0)
        has_reduced_gap = (
            'gap: 1px' in mobile_css or 'gap:1px' in mobile_css or
            'gap: 2px' in mobile_css or 'gap:2px' in mobile_css
        )
        assert has_reduced_gap, (
            "Mobile puzzle-grid should use reduced gap (1px or 2px)"
        )
