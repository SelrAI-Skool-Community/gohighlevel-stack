# SETUP-PROMPT.md

Paste into Claude Code to install + verify the ghl-crm skill.

```
Install + verify the ghl-crm skill on this machine.

1. Confirm the skill exists at ~/.claude/skills/ghl-crm/.
2. Confirm GHL MCP servers are wired. Run `claude mcp list` and look for ghl-official
   (36 fixed tools) and ghl-v2 (5 meta-tools fronting the full 570-op catalog). If missing,
   add both as http servers pointed at services.leadconnectorhq.com (/mcp/ and
   /mcp/anthropic/v2) with the Private Integration token + locationId headers.
3. Run smoke: bash ~/.claude/skills/ghl-crm/scripts/smoke.sh. Expect SMOKE PASS (7 checks).
4. Confirm sister skill /ghl-browser is installed for UI-only ops the API can't do.
5. Once verified, the skill is ready: trigger phrases include "search GHL contacts",
   "create a GHL contact", "update opportunity", "send GHL SMS/email", "GHL pipeline status".
```

## What this skill drives

| Operation | Lane |
|---|---|
| Contacts (search/create/update/tags) | ghl-official fixed tools (fast lane) |
| Opportunities / pipelines | ghl-official + ghl-v2 |
| Conversations (SMS, email, voice) | ghl-official |
| Calendars / appointments | ghl-official + ghl-v2 (see /ghl-calendars-booking) |
| Invoices / products / payments | ghl-v2 (see /ghl-payments-invoicing) |
| Ads via GHL Ad Manager (FB/Google/LinkedIn) | ghl-v2 (see /ghl-ads-manager) |
| Social media posting + analytics | ghl-official + ghl-v2 (see /ghl-social-planner) |
| AI chat/voice agents, knowledge bases | ghl-v2 (see /ghl-conversation-ai) |
| Blogs (read/create/publish) | ghl-official |
| Custom fields / objects / trigger links | ghl-v2 (see /ghl-contacts-pipeline) |
| Workflow ENROLMENT only | ghl-v2 (builder itself is browser-only) |
| 2FA codes | /ghl-browser + Gmail MCP (autonomous) |
| Workflow/funnel/form builders, pipeline stages | /ghl-browser (BROWSER-ONLY, see capability matrix) |

## API quirks to remember

Documented in detail in SKILL.md. The three biggest:

1. **Email sends use `html` field, SMS sends use `message` field.** Mixing causes 422 errors.
2. **ghl-v2 write ops require `idempotencyKey`** — 400 without it.
3. **Request params: snake_case. Response body: camelCase.**

## Failure modes

| Symptom | Fix |
|---|---|
| `mcp__ghl-official__*` not available | Tools not loaded — run ToolSearch with `+ghl contacts` to load them |
| 401 Unauthorized | PIT missing that scope, or token rotated. Probe first (401 = scope, 404 = path). Token lives in your password manager, or the `secrets/ghl.env` file |
| 422 Unprocessable on email | Used `message` instead of `html`. Fix the payload. |
| Social post returns "account not connected" | Social re-auth needed. Use /ghl-browser to navigate Settings → Social Planner → reconnect |
| Pipeline not visible | Check `locationId` in your request matches the install's location (set via `$GHL_LOCATION_ID`) |

## Pairs with

- Domain playbooks: `/ghl-ads-manager`, `/ghl-payments-invoicing`, `/ghl-calendars-booking`,
  `/ghl-social-planner`, `/ghl-conversation-ai`, `/ghl-contacts-pipeline`, `/ghl-email-flows`
- `/ghl-browser` — UI-only ops, 2FA, persistent profile
- `/ghl-landing-pages` — GHL funnel + page shipping lanes
- `/ghl-connector` — credential source
