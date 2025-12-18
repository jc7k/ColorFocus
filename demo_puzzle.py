#!/usr/bin/env python3
"""Quick demo of the Puzzle Grid Generator."""

import json
import sys
sys.path.insert(0, '/home/user/projects/ColorFocus')

from backend.app.services import PuzzleGenerator
from backend.app.constants import ColorToken, get_color_label, Language

def main():
    # Generate a puzzle
    generator = PuzzleGenerator(seed=42, congruence_percentage=0.125)
    puzzle = generator.generate()

    print("=" * 60)
    print("🧩 ColorFocus Puzzle Generator Demo")
    print("=" * 60)
    print(f"\n📊 Metadata:")
    print(f"   Seed: {puzzle.metadata.seed}")
    print(f"   Grid: {puzzle.metadata.rows}x{puzzle.metadata.cols}")
    print(f"   Congruence: {puzzle.metadata.congruence_percentage:.1%}")

    # Color codes for terminal output
    COLORS = {
        ColorToken.BLUE: "\033[94m",
        ColorToken.ORANGE: "\033[38;5;208m",
        ColorToken.PURPLE: "\033[95m",
        ColorToken.BLACK: "\033[90m",
        ColorToken.CYAN: "\033[96m",
        ColorToken.AMBER: "\033[93m",
        ColorToken.MAGENTA: "\033[35m",
        ColorToken.GRAY: "\033[37m",
    }
    RESET = "\033[0m"

    print(f"\n🎨 8x8 Stroop Puzzle Grid (Chinese labels, colored by ink):\n")

    for row in puzzle.cells:
        row_display = []
        for cell in row:
            label = get_color_label(cell.word, Language.CHINESE)
            color_code = COLORS.get(cell.ink_color, "")
            row_display.append(f"{color_code}{label}{RESET}")
        print("   " + "  ".join(row_display))

    # Count ink colors
    print(f"\n📈 Ink Color Distribution:")
    ink_counts = {}
    congruent_count = 0
    for row in puzzle.cells:
        for cell in row:
            ink_counts[cell.ink_color] = ink_counts.get(cell.ink_color, 0) + 1
            if cell.word == cell.ink_color:
                congruent_count += 1

    for token in ColorToken:
        count = ink_counts.get(token, 0)
        label = get_color_label(token, Language.CHINESE)
        english = get_color_label(token, Language.ENGLISH)
        bar = "█" * count
        print(f"   {label} ({english:7}): {bar} ({count})")

    print(f"\n🔀 Congruent cells (word = ink): {congruent_count}/64 ({congruent_count/64:.1%})")

    # Show JSON output
    print(f"\n📄 JSON Output (first 2 rows):")
    data = puzzle.to_dict()
    preview = {"grid": data["grid"][:2], "metadata": data["metadata"]}
    print(json.dumps(preview, indent=2, ensure_ascii=False))

    print("\n" + "=" * 60)
    print("✅ Puzzle generated successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
