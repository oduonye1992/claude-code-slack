#!/usr/bin/env python3
"""Generate a Veo 3.1 video prompt from a trend file.

Reads a JSON trend file (output of fetch_google_trends.py or analyze_sentiment.py),
builds a structured Veo 3.1 prompt, and outputs it as JSON to stdout.

See docs/veo3_meta_prompt_guide.md for the full prompt architecture.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any


# Persona pool — rotated to ensure diverse representation
_PERSONAS: list[dict[str, str]] = [
    {
        "name": "Anxious Ava",
        "description": "Mid-twenties, South Asian woman, natural hair, work-stressed but hopeful",
        "setting": "home desk or sofa, late afternoon light",
    },
    {
        "name": "Mindful Marcus",
        "description": "Early thirties, Black man, casual work-from-home clothes, thoughtful",
        "setting": "kitchen table or living room, morning light",
    },
    {
        "name": "Curious Carla",
        "description": "Early forties, Latina woman, parent-tired but grounded, warm expression",
        "setting": "family home, after-school hour light",
    },
]

_HOOKS: list[str] = [
    "POV: you finally asked for help",
    "Nobody talks about what {topic} actually feels like",
    "What if I told you 5 minutes a day could change everything",
    "This is what {topic} looks like from the inside",
    "I stopped pretending I was fine — here's what changed",
]

_CTAS: list[str] = [
    "Download Aurie — your pocket mental health companion. Link in bio.",
    "Try Aurie free. 3-minute daily check-ins. No judgment.",
    "Aurie: talk to someone who gets it, anytime.",
]


def pick_persona(index: int = 0) -> dict[str, str]:
    """Select a persona by rotating index.

    Args:
        index: Rotation index (modulo applied automatically).

    Returns:
        Persona dict with name, description, and setting.
    """
    return _PERSONAS[index % len(_PERSONAS)]


def build_prompt(trend: dict[str, Any], persona_index: int = 0) -> dict[str, Any]:
    """Build a structured Veo 3.1 prompt from a trend object.

    Args:
        trend: Trend dict with at minimum a ``topic`` key.
        persona_index: Which persona to use (0=Ava, 1=Marcus, 2=Carla).

    Returns:
        Dict containing all Veo 3.1 prompt components.
    """
    topic = trend.get("topic", "mental wellness")
    persona = pick_persona(persona_index)

    hook = _HOOKS[persona_index % len(_HOOKS)].format(topic=topic)
    cta = _CTAS[persona_index % len(_CTAS)]

    return {
        "trend": topic,
        "persona": persona["name"],
        "prompt": {
            "scene": (
                f"{persona['description']} sits quietly in {persona['setting']}. "
                f"The video opens on a still moment — a beat of recognition around '{topic}'. "
                "Handheld camera, slightly unsteady. Authentic, lived-in environment."
            ),
            "subject": persona["description"],
            "audio": {
                "background": "Soft lo-fi piano, 68–72 BPM, warm reverb",
                "voiceover": (
                    f"Warm, first-person, slightly imperfect delivery. "
                    f"Theme: {topic}. Sample: 'I didn't know it had a name until I looked it up.'"
                ),
                "ambient": "Soft apartment ambience — distant city, quiet hum",
            },
            "text_overlays": {
                "0:00-0:03": hook,
                "0:09-0:13": f"More people experience {topic} than you think.",
                "0:26-0:30": cta,
            },
            "style": {
                "colour_grade": "Warm, slightly desaturated, filmic",
                "lighting": "Soft natural or single warm lamp — no studio light",
                "camera": "Handheld with gentle drift, occasional slow push-in",
            },
            "duration_seconds": 30,
            "aspect_ratio": "9:16",
        },
        "compliance_check_required": True,
        "append_to": "knowledge/content/veo3-prompts.md",
    }


def main() -> None:
    """Entry point: parse args, read trend file, generate prompt, print JSON."""
    parser = argparse.ArgumentParser(
        description="Generate a Veo 3.1 video prompt from a trend file"
    )
    parser.add_argument(
        "--trend-file",
        required=True,
        type=Path,
        help="Path to JSON trend file (single object or first item of array)",
    )
    parser.add_argument(
        "--persona-index",
        type=int,
        default=0,
        help="Persona rotation index (0=Ava, 1=Marcus, 2=Carla)",
    )
    args = parser.parse_args()

    try:
        raw = json.loads(args.trend_file.read_text())
        trend: dict[str, Any] = raw[0] if isinstance(raw, list) else raw
        prompt = build_prompt(trend, persona_index=args.persona_index)
        print(json.dumps(prompt, indent=2))
    except FileNotFoundError:
        print(f"ERROR: trend file not found: {args.trend_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
