# Set up ghl-conversation-ai⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Paste this into Claude Code:

```text
Set up and verify the ghl-conversation-ai skill.

1. Confirm ~/.claude/skills/ghl-conversation-ai/SKILL.md and the ghl-crm skill exist.
2. Load GHL_API_KEY and GHL_LOCATION_ID from secrets/ghl.env in the GoHighLevel stack repo root.
3. Run `claude mcp list`. If a GoHighLevel MCP server is listed, use its actual registered name. MCP is optional.
4. Without MCP, use direct REST with the Private Integration Token or the repo-root `scripts/ghl raw` command.
5. Run a read-only knowledge-base query. On failure, ask Claude to retry after checking the token scope and location ID.
```

The operations list is in `references/operations.md`. Every documented operation has a REST fallback.

Router key `sk-03gy0y` — resolved by the skills index on load.
