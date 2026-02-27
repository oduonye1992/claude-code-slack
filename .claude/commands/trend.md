---
name: trend
description: Execute the full trend analysis and prompt generation pipeline
---

# /trend — Trend Analysis Pipeline

Execute the full trend-to-prompt pipeline:

## Steps

1. **Research phase** — Spawn the `@researcher` subagent to:
   - Run `python3 scripts/fetch_google_trends.py --region US --category health`
   - Analyze trends for relevance to Aurie's audience
   - Score sentiment with `python3 scripts/analyze_sentiment.py`

2. **Store results** — Save analyzed trends to `data/agent_memory.db` in the `trends` table

3. **Content generation** — Spawn the `@content-writer` subagent to:
   - Read the stored trend data
   - Generate Veo 3.1 video prompts using `python3 scripts/generate_veo_prompt.py`
   - Check prompts against compliance guidelines
   - Append approved prompts to `knowledge/content/veo3-prompts.md`

4. **Report** — Post a formatted summary to the current Slack channel:
   - Top 5 trends with relevance scores
   - Generated video prompts (1-3)
   - Suggested posting schedule

Format the report with Slack Block Kit for rich formatting.
