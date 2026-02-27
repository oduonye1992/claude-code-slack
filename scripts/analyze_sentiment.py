#!/usr/bin/env python3
"""Analyse sentiment of a text string using a simple keyword heuristic.

Outputs a JSON object with sentiment label and score to stdout.

TODO: Replace the keyword heuristic with a proper model call (e.g. Anthropic API or VADER).
"""

import argparse
import json
import sys
from typing import Any

# Simple keyword sets — replace with model-based approach in production
_POSITIVE_KEYWORDS: frozenset[str] = frozenset(
    {
        "happy",
        "joy",
        "love",
        "calm",
        "hope",
        "relief",
        "heal",
        "healing",
        "recovery",
        "better",
        "improve",
        "thrive",
        "peace",
        "mindful",
        "gratitude",
        "support",
        "comfort",
        "safe",
        "strength",
        "resilience",
    }
)

_NEGATIVE_KEYWORDS: frozenset[str] = frozenset(
    {
        "anxiety",
        "anxious",
        "stress",
        "stressed",
        "burnout",
        "depressed",
        "depression",
        "overwhelm",
        "overwhelmed",
        "panic",
        "fear",
        "dread",
        "lonely",
        "loneliness",
        "crisis",
        "struggle",
        "exhausted",
        "exhaustion",
        "tired",
        "suffer",
    }
)


def analyse(text: str) -> dict[str, Any]:
    """Compute a simple sentiment score from keyword matching.

    Args:
        text: Input text to analyse.

    Returns:
        Dict with ``sentiment`` label ("positive" | "negative" | "neutral") and
        ``score`` float in [-1.0, 1.0].
    """
    words = text.lower().split()
    total = len(words) or 1

    pos_hits = sum(1 for w in words if w.strip(".,!?") in _POSITIVE_KEYWORDS)
    neg_hits = sum(1 for w in words if w.strip(".,!?") in _NEGATIVE_KEYWORDS)

    raw_score = (pos_hits - neg_hits) / total
    # Clamp to [-1, 1]
    score = max(-1.0, min(1.0, raw_score * 10))

    if score > 0.05:
        label = "positive"
    elif score < -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {
        "sentiment": label,
        "score": round(score, 4),
        "positive_hits": pos_hits,
        "negative_hits": neg_hits,
        "word_count": total,
    }


def main() -> None:
    """Entry point: parse args, analyse sentiment, print JSON."""
    parser = argparse.ArgumentParser(
        description="Analyse sentiment of a text string"
    )
    parser.add_argument(
        "--text",
        required=True,
        help="Text to analyse",
    )
    args = parser.parse_args()

    try:
        result = analyse(args.text)
        print(json.dumps(result, indent=2))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
