#!/usr/bin/env python3
"""Check current Anthropic API billing usage vs. configured limits.

This is a stub implementation. TODO: integrate with Anthropic usage API
once it becomes available in the SDK.

Outputs a JSON cost/limit report to stdout.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any


def get_stub_billing() -> dict[str, Any]:
    """Return stub billing data.

    Returns:
        Dict with current spend, limit, and metadata.
        All monetary values are in USD.
    """
    # TODO: Replace with real API call:
    # client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    # usage = client.usage.get_current_period()  # hypothetical endpoint
    return {
        "status": "stub",
        "message": "Real billing API not yet available — showing placeholder data",
        "current_period": {
            "start": "2026-02-01T00:00:00Z",
            "end": "2026-02-28T23:59:59Z",
        },
        "spend_usd": 0.00,
        "limit_usd": float(os.getenv("BILLING_LIMIT_USD", "50")),
        "tokens_used": 0,
        "api_key_present": bool(os.getenv("ANTHROPIC_API_KEY")),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    """Entry point: fetch billing info and print JSON report."""
    try:
        report = get_stub_billing()
        print(json.dumps(report, indent=2))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
