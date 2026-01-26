"""
Shared pytest fixtures and utilities for ColorFocus tests.
"""

import pytest
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
PUZZLE_HTML_PATH = PROJECT_ROOT / "frontend" / "puzzle.html"
PUZZLE_CSS_PATH = PROJECT_ROOT / "frontend" / "styles" / "puzzle.css"
MODULES_DIR = PROJECT_ROOT / "frontend" / "src" / "modules"


@pytest.fixture
def puzzle_html() -> str:
    """Load the puzzle.html file content."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def puzzle_css() -> str:
    """Load the puzzle.css file content."""
    with open(PUZZLE_CSS_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def puzzle_html_and_css(puzzle_html, puzzle_css) -> str:
    """
    Return combined HTML and CSS content for backwards-compatible tests.
    This allows tests that previously searched both HTML and inline CSS
    to continue working with minimal changes.
    """
    return puzzle_html + "\n" + puzzle_css


def load_puzzle_html() -> str:
    """Load the puzzle.html file (utility function for non-fixture use)."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


def load_puzzle_css() -> str:
    """Load the puzzle.css file (utility function for non-fixture use)."""
    with open(PUZZLE_CSS_PATH, "r", encoding="utf-8") as f:
        return f.read()


def load_puzzle_html_and_css() -> str:
    """
    Load combined HTML and CSS content (utility function for non-fixture use).
    """
    return load_puzzle_html() + "\n" + load_puzzle_css()


def load_puzzle_js() -> str:
    """
    Load all JavaScript module files (utility function for non-fixture use).
    Returns combined content of all JS modules.
    """
    js_content = []
    for js_file in MODULES_DIR.glob("*.js"):
        with open(js_file, "r", encoding="utf-8") as f:
            js_content.append(f"// === {js_file.name} ===\n{f.read()}")
    return "\n\n".join(js_content)


def load_puzzle_html_and_js() -> str:
    """
    Load combined HTML and JavaScript content (utility function for non-fixture use).
    For tests that check JavaScript patterns that may be in HTML or JS modules.
    """
    return load_puzzle_html() + "\n" + load_puzzle_js()


@pytest.fixture
def puzzle_js() -> str:
    """Load all JavaScript module content."""
    return load_puzzle_js()


@pytest.fixture
def puzzle_html_and_js(puzzle_html) -> str:
    """Return combined HTML and JS content."""
    return puzzle_html + "\n" + load_puzzle_js()
