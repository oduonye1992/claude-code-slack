# Scout Scripts

Standalone Python scripts for the Scout trend analysis and content pipeline.

All scripts:
- Require Python 3.11+ (no extra dependencies beyond stdlib)
- Output JSON to **stdout**
- Output errors to **stderr**
- Exit `0` on success, `1` on failure

---

## fetch_google_trends.py

Fetch trending topics filtered by region and category.

**Currently a stub** — returns realistic placeholder data. TODO: integrate `pytrends`.

```bash
python3 scripts/fetch_google_trends.py --region US --category health
```

| Flag | Default | Description |
|---|---|---|
| `--region` | `US` | ISO 3166-1 alpha-2 country code |
| `--category` | `health` | Topic category filter |

**Output** — array of trend objects:

```json
[
  {
    "topic": "anxiety at work",
    "search_volume": 95000,
    "region": "US",
    "category": "health",
    "rising": true,
    "fetched_at": "2026-02-27T12:00:00+00:00",
    "source": "stub"
  }
]
```

---

## analyze_sentiment.py

Analyse the sentiment of a text string using keyword heuristics.

TODO: Replace heuristic with a proper model (VADER or Anthropic API call).

```bash
python3 scripts/analyze_sentiment.py --text "anxiety at work is rising"
```

| Flag | Required | Description |
|---|---|---|
| `--text` | Yes | Text string to analyse |

**Output:**

```json
{
  "sentiment": "negative",
  "score": -0.05,
  "positive_hits": 0,
  "negative_hits": 1,
  "word_count": 5
}
```

---

## generate_veo_prompt.py

Generate a structured Veo 3.1 video prompt from a trend file.

```bash
# First write the latest trend to a file
python3 scripts/fetch_google_trends.py | python3 -c "
import json, sys, pathlib
data = json.load(sys.stdin)
pathlib.Path('data').mkdir(exist_ok=True)
pathlib.Path('data/latest_trend.json').write_text(json.dumps(data[0]))
"

# Then generate the prompt
python3 scripts/generate_veo_prompt.py --trend-file data/latest_trend.json
python3 scripts/generate_veo_prompt.py --trend-file data/latest_trend.json --persona-index 1
```

| Flag | Default | Description |
|---|---|---|
| `--trend-file` | _(required)_ | Path to JSON trend file |
| `--persona-index` | `0` | Persona rotation: 0=Ava, 1=Marcus, 2=Carla |

**Output:** Full Veo 3.1 prompt JSON — see `docs/veo3_meta_prompt_guide.md` for schema.

---

## db_migrate.py

Apply SQLite schema migrations. Safe to run multiple times.

Creates tables: `trends`, `veo_prompts`, `schema_migrations`.

```bash
python3 scripts/db_migrate.py
python3 scripts/db_migrate.py --db-path data/custom.db
```

| Flag | Default | Description |
|---|---|---|
| `--db-path` | `data/bot.db` | Path to SQLite database |

**Output:**

```json
{
  "status": "ok",
  "db_path": "data/bot.db",
  "applied": [1, 2, 3],
  "skipped": [],
  "timestamp": "2026-02-27T12:00:00+00:00"
}
```

---

## health_check.py

Run a system health check. Used by the `/status` command and the Stop hook.

```bash
python3 scripts/health_check.py
python3 scripts/health_check.py --quick   # critical checks only
```

| Flag | Description |
|---|---|
| `--quick` | Only check env vars and database (faster, used in Stop hook) |

**Output:**

```json
{
  "status": "ok",
  "timestamp": "2026-02-27T12:00:00+00:00",
  "quick": false,
  "checks": {
    "database": { "status": "ok", "tables": ["trends", "veo_prompts"], "size_kb": 24.0 },
    "env_vars": { "status": "ok", "missing_required": [], "missing_optional": [] },
    "scripts": { "status": "ok", "missing_scripts": [] },
    "knowledge_base": { "status": "ok", "missing_files": [] }
  }
}
```

Exit code `1` if any check status is `"error"`.

---

## billing_check.py

Check current Anthropic API billing. Currently a stub.

```bash
python3 scripts/billing_check.py
```

**Output:**

```json
{
  "status": "stub",
  "spend_usd": 0.00,
  "limit_usd": 50.0,
  "tokens_used": 0,
  "api_key_present": true,
  "fetched_at": "2026-02-27T12:00:00+00:00"
}
```
