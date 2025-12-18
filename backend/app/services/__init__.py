"""
Services module for ColorFocus backend.

Exports service classes for business logic.
"""

from backend.app.services.puzzle_generator import PuzzleGenerator

__all__: list[str] = ["PuzzleGenerator"]
