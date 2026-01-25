#!/usr/bin/env python3
"""
Generate Claude Code skills from Agent-OS standards.

Reads agent-os/standards/index.yml and creates one skill file per category
in .claude/skills/, with each skill referencing all standards in that category.

Usage:
    uv run scripts/generate-skills-from-standards.py
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Run: uv add pyyaml")
    sys.exit(1)


def load_index(index_path: Path) -> dict:
    """Load and parse the standards index.yml file."""
    if not index_path.exists():
        print(f"Error: {index_path} not found")
        print("Run /discover-standards first to create standards.")
        sys.exit(1)

    with open(index_path) as f:
        return yaml.safe_load(f) or {}


def generate_skill_content(category: str, standards: dict) -> str:
    """Generate the markdown content for a skill file."""
    # Build the title from category name
    title = category.replace("-", " ").title()

    # Build references list
    references = []
    for standard_name, info in sorted(standards.items()):
        ref_path = f"@agent-os/standards/{category}/{standard_name}.md"
        description = info.get("description", "")
        references.append((ref_path, description))

    # Generate the skill content
    lines = [
        f"# {title} Standards",
        "",
        f"Apply {title.lower()} standards from this project.",
        "",
        "## Standards",
        "",
    ]

    for ref_path, description in references:
        lines.append(ref_path)
        if description:
            lines.append(f"  <!-- {description} -->")
        lines.append("")

    lines.extend([
        "## Instructions",
        "",
        f"When working on {category.replace('-', ' ')}-related code:",
        "",
        "1. Read the referenced standards above",
        "2. Apply all relevant patterns and conventions",
        "3. If a standard conflicts with the task, ask for clarification",
        "",
    ])

    return "\n".join(lines)


def main():
    # Determine paths relative to script location
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    index_path = project_root / "agent-os" / "standards" / "index.yml"
    skills_dir = project_root / ".claude" / "skills"

    # Load the index
    index = load_index(index_path)

    if not index:
        print("Error: index.yml is empty")
        sys.exit(1)

    # Create skills directory if needed
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Track what we create
    created = []
    skipped = []

    for category, standards in sorted(index.items()):
        if not standards:
            skipped.append(category)
            continue

        skill_path = skills_dir / f"{category}.md"
        content = generate_skill_content(category, standards)

        # Write the skill file
        skill_path.write_text(content)
        created.append(category)

    # Report results
    print(f"Generated {len(created)} skill(s) in .claude/skills/:")
    for category in created:
        standards_count = len(index[category])
        print(f"  - {category}.md ({standards_count} standard(s))")

    if skipped:
        print(f"\nSkipped {len(skipped)} empty category(ies): {', '.join(skipped)}")

    print(f"\nSkills are now available in Claude Code (e.g., /accessibility, /git, /frontend).")


if __name__ == "__main__":
    main()
