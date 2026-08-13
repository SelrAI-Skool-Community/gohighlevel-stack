# Set up ghl-email-flows⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Paste this into Claude Code:

```text
Set up and verify the ghl-email-flows skill.

1. Confirm ~/.claude/skills/ghl-email-flows/SKILL.md and its references and scripts exist.
2. Confirm ghl-crm and ghl-browser are installed from this bundle.
3. Load GHL_API_KEY and GHL_LOCATION_ID from secrets/ghl.env in the GoHighLevel stack repo root.
4. Run `claude mcp list`. If a GoHighLevel MCP server is listed, use its actual registered name. MCP is optional.
5. Without MCP, use direct REST or `scripts/push_templates.py` for template calls. Use ghl-browser for workflow steps because GHL has no public workflow-builder API.
6. Run `python3 ~/.claude/skills/ghl-email-flows/scripts/push_templates.py --help`, then a read-only template-list query. On failure, ask Claude to retry after checking repo-root secrets/ghl.env, the token scope, and the location ID.
```

The skill needs approved copy, hosted assets, and a rendered light-mode and dark-mode review before shipping.

Router key `sk-5e44r9` — resolved by the skills index on load.
