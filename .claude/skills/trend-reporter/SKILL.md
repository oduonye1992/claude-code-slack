---
name: trend-reporter
description: Analyzes trending topics and generates structured trend data. Triggers on trend analysis, market research, what's trending, viral content discussions.
---

# Trend Reporter Skill

You are the trend reporter. When invoked, follow this pipeline:

## Steps

1. **Fetch trends** — Run `python3 scripts/fetch_google_trends.py --region US --category technology` to get current trending topics. Adjust `--region` and `--category` based on the user's request.

2. **Analyze relevance** — Filter trends for relevance to mental health, wellness, self-care, and the Aurie app's target audience. Read `knowledge/audience/personas.md` for audience context.

3. **Score sentiment** — For each relevant trend, run `python3 scripts/analyze_sentiment.py --text "<trend topic>"` to get a sentiment score.

4. **Store results** — Save the analyzed trends to the `trends` table in `data/agent_memory.db` using the database utilities.

5. **Report** — Format the top 5 trends as a Slack-friendly summary with:
   - Trend name and search volume
   - Relevance score (1-10) to our niche
   - Sentiment (positive/negative/neutral)
   - Suggested content angle for Aurie

## Output Format

Return a JSON array of trend objects to stdout. Each object:

```json
{
  "topic": "string",
  "search_volume": "number",
  "relevance_score": "number (1-10)",
  "sentiment": "positive | negative | neutral",
  "sentiment_score": "number (-1 to 1)",
  "content_angle": "string"
}
```
