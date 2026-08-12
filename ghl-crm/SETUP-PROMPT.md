# Set up ghl-crm

Paste this into Claude Code:

```text
Set up and verify the ghl-crm skill.

1. Confirm ~/.claude/skills/ghl-crm/SKILL.md and the ghl-browser skill exist.
2. Load GHL_API_KEY and GHL_LOCATION_ID from secrets/ghl.env in the GoHighLevel stack repo root.
3. Run `claude mcp list`. If a GoHighLevel MCP server is listed, use its actual registered name. MCP is optional.
4. Without MCP, use direct REST with the Private Integration Token or the repo-root `scripts/ghl` helper.
5. Run `bash ~/.claude/skills/ghl-crm/scripts/smoke.sh`.
6. Run a read-only contact-list query. On failure, ask Claude to retry after checking the token scope and location ID.
```

## Routing

| Work | Route |
|---|---|
| Contacts, opportunities, conversations, calendars, payments, blogs, social, AI, ads | MCP, direct REST, or `scripts/ghl` |
| Workflow enrolment | MCP, direct REST, or `scripts/ghl raw` |
| Workflow, funnel, form, and pipeline-stage builders | `ghl-browser` |

## Common failures

| Symptom | Fix |
|---|---|
| GHL MCP tools missing | Run `claude mcp list`. Use the listed GoHighLevel server name, or continue through REST or `scripts/ghl` |
| 401 Unauthorized | Check the Private Integration Token and its scopes in `secrets/ghl.env` |
| 404 Not Found | Check `GHL_LOCATION_ID` and the endpoint path |
| 422 on email send | Use `html` for email and `message` for SMS, then retry |

The specialist skills in this bundle cover ads, payments, calendars, social, Conversation
AI, contacts, email flows, landing pages, and browser-only work.
