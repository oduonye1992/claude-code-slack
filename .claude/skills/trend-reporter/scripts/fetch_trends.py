"""Skill-level trend fetcher — thin wrapper around scripts/fetch_google_trends.py.

This script is invoked by the trend-reporter skill for quick trend lookups
within the skill context.

Usage:
    python3 .claude/skills/trend-reporter/scripts/fetch_trends.py
"""

import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Run the main trend fetch script and pass through results."""
    script = Path("scripts/fetch_google_trends.py")
    if not script.exists():
        print(
            json.dumps({"error": "fetch_google_trends.py not found"}), file=sys.stderr
        )
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, str(script), "--region", "US", "--category", "health"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    print(result.stdout)


if __name__ == "__main__":
    main()
