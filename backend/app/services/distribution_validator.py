"""
Distribution validation for ColorFocus puzzle grids.

Validates that color distribution in puzzles is within acceptable bounds
to prevent heavily skewed puzzles that would make the game unfair.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from backend.app.constants.colors import ColorToken


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

    def validate(
        self, color_counts: Dict[ColorToken, int], active_colors: Optional[List[ColorToken]] = None
    ) -> ValidationResult:
        """
        Validate a color distribution.

        Args:
            color_counts: Dictionary mapping ColorToken to count.
            active_colors: List of colors to validate (defaults to all ColorToken if None).

        Returns:
            ValidationResult with is_valid and any issues found.
        """
        issues: List[str] = []
        colors_to_check = active_colors if active_colors is not None else list(ColorToken)

        for token in colors_to_check:
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
