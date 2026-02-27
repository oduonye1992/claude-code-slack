#!/usr/bin/env python3
"""Run SQLite schema migrations for the Scout database.

Creates or upgrades the Scout-specific tables in the given SQLite database.
Safe to run multiple times — uses CREATE TABLE IF NOT EXISTS.

Outputs a JSON migration report to stdout.
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MIGRATIONS: list[tuple[int, str]] = [
    (
        1,
        """
        CREATE TABLE IF NOT EXISTS trends (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            topic       TEXT    NOT NULL,
            search_volume INTEGER,
            region      TEXT,
            category    TEXT,
            rising      INTEGER,
            relevance_score REAL,
            sentiment   TEXT,
            sentiment_score REAL,
            content_angle TEXT,
            source      TEXT    DEFAULT 'stub',
            fetched_at  TEXT    NOT NULL,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
        """,
    ),
    (
        2,
        """
        CREATE TABLE IF NOT EXISTS veo_prompts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            trend_id    INTEGER REFERENCES trends(id),
            topic       TEXT    NOT NULL,
            persona     TEXT,
            prompt_json TEXT    NOT NULL,
            approved    INTEGER DEFAULT 0,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
        """,
    ),
    (
        3,
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version     INTEGER PRIMARY KEY,
            applied_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
        """,
    ),
]


def get_applied_versions(conn: sqlite3.Connection) -> set[int]:
    """Return set of already-applied migration version numbers.

    Args:
        conn: Open SQLite connection.

    Returns:
        Set of integer version numbers already in schema_migrations.
    """
    try:
        rows = conn.execute("SELECT version FROM schema_migrations").fetchall()
        return {r[0] for r in rows}
    except sqlite3.OperationalError:
        return set()


def run_migrations(db_path: Path) -> dict[str, Any]:
    """Apply pending migrations to the database at db_path.

    Args:
        db_path: Path to the SQLite database file.

    Returns:
        Report dict with applied/skipped counts and status.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))

    applied: list[int] = []
    skipped: list[int] = []

    try:
        # Ensure schema_migrations table exists first
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version     INTEGER PRIMARY KEY,
                applied_at  TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()

        done = get_applied_versions(conn)

        for version, sql in MIGRATIONS:
            if version in done:
                skipped.append(version)
                continue
            conn.executescript(sql)
            conn.execute(
                "INSERT OR IGNORE INTO schema_migrations (version, applied_at) VALUES (?, ?)",
                (version, datetime.now(timezone.utc).isoformat()),
            )
            conn.commit()
            applied.append(version)

    finally:
        conn.close()

    return {
        "status": "ok",
        "db_path": str(db_path),
        "applied": applied,
        "skipped": skipped,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    """Entry point: parse args, run migrations, print JSON report."""
    parser = argparse.ArgumentParser(
        description="Run Scout SQLite schema migrations"
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=Path("data/bot.db"),
        help="Path to SQLite database (default: data/bot.db)",
    )
    args = parser.parse_args()

    try:
        report = run_migrations(args.db_path)
        print(json.dumps(report, indent=2))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
