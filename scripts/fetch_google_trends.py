#!/usr/bin/env python3
"""Fetch trending topics from Google Trends (stub — TODO: integrate pytrends).

Outputs a JSON array of trend objects to stdout.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any


def build_stub_trends(region: str, category: str) -> list[dict[str, Any]]:
    """Build stub trend data for development and testing.

    Args:
        region: ISO 3166-1 alpha-2 country code (e.g. "US").
        category: Trend category filter (e.g. "health").

    Returns:
        List of trend objects with topic, search_volume, and metadata.
    """
    return [
        {
            "topic": "anxiety at work",
            "search_volume": 95000,
            "region": region,
            "category": category,
            "rising": True,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source": "stub",
        },
        {
            "topic": "burnout recovery",
            "search_volume": 72000,
            "region": region,
            "category": category,
            "rising": True,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source": "stub",
        },
        {
            "topic": "mindfulness for beginners",
            "search_volume": 65000,
            "region": region,
            "category": category,
            "rising": False,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source": "stub",
        },
        {
            "topic": "Sunday scaries",
            "search_volume": 58000,
            "region": region,
            "category": category,
            "rising": True,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source": "stub",
        },
        {
            "topic": "therapy waiting list",
            "search_volume": 43000,
            "region": region,
            "category": category,
            "rising": True,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source": "stub",
        },
    ]


def main() -> None:
    """Entry point: parse args, fetch trends, print JSON."""
    parser = argparse.ArgumentParser(
        description="Fetch trending topics (stub for pytrends integration)"
    )
    parser.add_argument(
        "--region",
        default="US",
        help="ISO country code (default: US)",
    )
    parser.add_argument(
        "--category",
        default="health",
        help="Trend category (default: health)",
    )
    args = parser.parse_args()

    try:
        # TODO: Replace with real pytrends integration:
        # from pytrends.request import TrendReq
        # pytrends = TrendReq(hl="en-US", tz=360)
        # pytrends.build_payload(kw_list=[args.category], geo=args.region)
        # data = pytrends.trending_searches(pn=args.region.lower())
        trends = build_stub_trends(region=args.region, category=args.category)
        print(json.dumps(trends, indent=2))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
