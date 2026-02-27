#!/usr/bin/env python3
"""System health check for Scout.

Checks database connectivity, environment variables, and filesystem state.
Outputs a JSON health report to stdout.

Exit codes:
  0 — all checks healthy
  1 — one or more checks failed or errored
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def check_database(db_path: Path) -> dict[str, Any]:
    """Verify SQLite database is accessible and return basic stats.

    Args:
        db_path: Path to the SQLite database file.

    Returns:
        Health check result dict.
    """
    if not db_path.exists():
        return {"status": "warn", "message": f"DB not found at {db_path}"}

    try:
        conn = sqlite3.connect(str(db_path))
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        size_kb = round(db_path.stat().st_size / 1024, 1)
        conn.close()
        return {
            "status": "ok",
            "db_path": str(db_path),
            "tables": [t[0] for t in tables],
            "size_kb": size_kb,
        }
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "message": str(exc)}


def check_env_vars(quick: bool) -> dict[str, Any]:
    """Verify required environment variables are set.

    Args:
        quick: If True, only check the most critical vars.

    Returns:
        Health check result dict.
    """
    required = ["SLACK_BOT_TOKEN", "SLACK_APP_TOKEN", "ANTHROPIC_API_KEY"]
    optional = ["APPROVED_DIRECTORY", "ALLOWED_USERS", "ENABLE_API_SERVER"]

    missing_required = [k for k in required if not os.getenv(k)]
    missing_optional = [] if quick else [k for k in optional if not os.getenv(k)]

    status = "error" if missing_required else ("warn" if missing_optional else "ok")
    return {
        "status": status,
        "missing_required": missing_required,
        "missing_optional": missing_optional,
    }


def check_scripts_dir() -> dict[str, Any]:
    """Verify that the scripts/ directory exists and key scripts are present.

    Returns:
        Health check result dict.
    """
    scripts_dir = Path("scripts")
    expected = [
        "fetch_google_trends.py",
        "analyze_sentiment.py",
        "generate_veo_prompt.py",
        "db_migrate.py",
        "health_check.py",
        "billing_check.py",
    ]
    missing = [s for s in expected if not (scripts_dir / s).exists()]
    status = "error" if missing else "ok"
    return {"status": status, "missing_scripts": missing}


def check_knowledge_base() -> dict[str, Any]:
    """Verify key knowledge base files are present.

    Returns:
        Health check result dict.
    """
    key_files = [
        "knowledge/INDEX.md",
        "knowledge/clinical/compliance.md",
        "knowledge/brand/README.md",
        "knowledge/content/hooks.md",
    ]
    missing = [f for f in key_files if not Path(f).exists()]
    status = "warn" if missing else "ok"
    return {"status": status, "missing_files": missing}


def overall_status(checks: dict[str, dict[str, Any]]) -> str:
    """Derive overall status from individual check results.

    Args:
        checks: Dict mapping check name to result dict.

    Returns:
        "ok", "warn", or "error".
    """
    statuses = [v.get("status", "ok") for v in checks.values()]
    if "error" in statuses:
        return "error"
    if "warn" in statuses:
        return "warn"
    return "ok"


def main() -> None:
    """Entry point: run health checks and print JSON report."""
    parser = argparse.ArgumentParser(description="Scout system health check")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run only critical checks (faster)",
    )
    args = parser.parse_args()

    db_path = Path(os.getenv("DATABASE_PATH", "data/bot.db"))

    checks: dict[str, Any] = {
        "database": check_database(db_path),
        "env_vars": check_env_vars(quick=args.quick),
    }

    if not args.quick:
        checks["scripts"] = check_scripts_dir()
        checks["knowledge_base"] = check_knowledge_base()

    report = {
        "status": overall_status(checks),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "quick": args.quick,
        "checks": checks,
    }

    print(json.dumps(report, indent=2))

    if report["status"] == "error":
        sys.exit(1)


if __name__ == "__main__":
    main()
