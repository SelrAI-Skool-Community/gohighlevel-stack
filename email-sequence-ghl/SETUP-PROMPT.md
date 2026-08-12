# Set up email-sequence-ghl

Paste this into Claude Code:

```text
Set up and verify the email-sequence-ghl skill.

1. Confirm ~/.claude/skills/email-sequence-ghl/SKILL.md exists.
2. Confirm ghl-email-flows, ghl-crm, and ghl-browser are installed from this bundle.
3. Load GHL_API_KEY and GHL_LOCATION_ID from secrets/ghl.env in the GoHighLevel stack repo root.
4. Run `claude mcp list`. If a GoHighLevel MCP server is listed, use its actual registered name. MCP is optional.
5. Without MCP, use direct REST or repo-root `scripts/ghl raw` for template calls. Use ghl-browser for workflow steps because GHL has no public workflow-builder API.
6. Run a read-only template-list query. On failure, ask Claude to retry after checking the token scope and location ID.
```

The skill needs approved copy, a trigger, one goal, real proof if available, and exit conditions. It always leaves the workflow paused.
