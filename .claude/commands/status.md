---
name: status
description: Run a full system health check
---

# /status — System Health Check

Run a comprehensive health check of the Scout system:

1. **Database**: Check connectivity to `data/agent_memory.db`, report table counts and DB size
2. **Slack**: Verify the Slack connection is active
3. **API Keys**: Confirm Anthropic API key is valid (without exposing it)
4. **Billing**: Report current spend vs. limit from `scripts/billing_check.py`
5. **Last Trend**: Show timestamp of the most recent trend capture
6. **Uptime**: Report how long the bot has been running

Execute: `python3 scripts/health_check.py`

Format the results as a Slack message with status indicators:
- `:white_check_mark:` for healthy systems
- `:warning:` for degraded systems
- `:x:` for failed systems
