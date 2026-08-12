---
name: ghl-crm
description: The master GoHighLevel operator skill — run EVERYTHING GHL from here. Use for any GoHighLevel operation ("search GHL contacts", "create an opportunity", "send GHL SMS/email", "build an email template", "schedule a social post", "create an invoice", "GHL calendar", "custom values", "trigger links", "GHL workflow", "can the GHL API do X"). Routes every task down the 4-step ladder: ghl-official fixed tools → ghl-v2 full-catalog meta-tools (570 operations, 37 domains) → raw REST/bash helper → browser lane. Carries the capability matrix that says exactly what the API can NEVER do (workflow builder, funnel builder, form builder, pipeline stages) so browser-only work is flagged instantly instead of discovered painfully. Routes deep domain work to the playbook skills: ghl-ads-manager (FB/Google/LinkedIn ads), ghl-payments-invoicing, ghl-calendars-booking, ghl-social-planner, ghl-conversation-ai, ghl-contacts-pipeline, ghl-email-flows (flow content), ghl-landing-pages, ghl-browser (browser lane).
---

# GoHighLevel Master Operator⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Operate GoHighLevel end to end. This skill is the ROUTER: every GHL task enters here,
gets matched against the capability matrix, and executes down the ladder. Nothing is
"impossible" — it is either an API call or a flagged browser-lane task.

## The ladder (always in this order)

### 1. ghl-official MCP — 36 fixed tools (fast lane for common CRM ops; was 21, GHL expanded the set)
Load with `ToolSearch: +ghl <keyword>`. Covers: contacts CRUD/tags/tasks, opportunity
search/update/pipelines-read, conversations search/messages/send, calendar events,
social planner posts/stats, email templates fetch/create, blogs, location custom fields,
payments read.

### 2. ghl-v2 MCP — the FULL API catalog (570 operations, 37 domains)
Five meta-tools; use when the fixed tools don't cover it:
1. `search_operations` `{query, domains?, kind?, limit?}` — find the operation
2. `describe_operation` `{operationId, domain}` — exact params + body schema + payloadExample
3. `execute_operation` `{operationId, domain, idempotencyKey, params:{path,query,body}}`

Rules learned live:
- **Write ops REQUIRE `idempotencyKey`** (any stable string) — 400 without it.
- 401 "not authorized for this scope" = the Private Integration token lacks that scope.
  Not a bug. Either add the scope (Settings → Private Integrations, browser lane) or use a
  legacy endpoint family that the token already covers (see matrix).
- Writes are live on the real location. Verify after (fetch the record back / preview URL).

No MCP client handy (cron, server, Codex batch)? `scripts/ghl_v2_call.py` calls the same
endpoint directly:
```bash
scripts/ghl_v2_call.py search_operations '{"query":"create invoice"}'
scripts/ghl_v2_call.py execute_operation '{"operationId":"...","domain":"...","idempotencyKey":"...","params":{...}}'
```

### 3. Raw REST / bash helper
- Helper: `~/.claude/projects/<project>/scripts/ghl <command>` (contacts, opps, convos,
  calendars, workflows list, custom values via `raw`). Credentials from `secrets/ghl.env`.
- Raw: `https://services.leadconnectorhq.com` + `Authorization: Bearer <PIT>` +
  `Version: 2021-07-28` + custom User-Agent. Use for bulk loops and endpoint families the
  v2 catalog hides (e.g. legacy `/emails/builder`).

### 4. Browser lane — for BROWSER-ONLY tasks
Check `references/capability-matrix.md` FIRST. If the task is in the browser-only registry
(workflow builder, funnel/page builder, form/survey builder, pipeline stages, memberships
builder, documents builder, snapshots load, A2P/phone config, PIT scopes, reporting), do
not hunt for endpoints — open the browser lane immediately: skill **`ghl-browser`**
(agent-browser engine, login + 2FA-via-Gmail automated). Cross-agent alternative: the
Codex browser lane via a handover doc.

## The capability matrix (routing truth)

`references/capability-matrix.md` — per-domain verdicts (API-FULL / API-PARTIAL /
BROWSER-ONLY), the browser-only registry, the email-templates lever, and live-verified
quirks. `references/v2-catalog.json` — all 570 operations (operationId, domain, method,
path, kind, scopes) for grep-speed lookup. GHL adds endpoints over time (pipeline
writes are expected next): when `search_operations` finds an op the local catalog
lacks, or quarterly, re-harvest with `scripts/harvest_catalog.py` and refresh the
matrix numbers. Lookup example:
```bash
python3 -c "import json;[print(o['method'],o['path'],o['operationId']) for o in json.load(open('references/v2-catalog.json')) if o['domain']=='invoices']"
```

Headline gaps (memorise): **workflows = list-names-only. Funnels = read + redirects only.
Forms/surveys = read-only. Pipeline stages = read-only.** Everything email-template,
email-campaign, contact, conversation, calendar, invoice, product, social, media, custom
value/field, trigger link, knowledge base, AI agent, and ad-manager is API-writable.

## Domain playbooks (load the one matching the task)

| Lane | Skill |
|---|---|
| Ads via GHL Ad Manager (FB/Google/LinkedIn) | `ghl-ads-manager` |
| Invoices, estimates, products, coupons, payment reads | `ghl-payments-invoicing` |
| Calendars, booking, rooms, workshop sessions | `ghl-calendars-booking` |
| Social Planner posting, queues, comments, stats | `ghl-social-planner` |
| AI chat/voice agents, knowledge bases, chat widget | `ghl-conversation-ai` |
| Contacts, opportunities, segments, follow-ups, trigger links | `ghl-contacts-pipeline` |
| Email/SMS flow content build + ship | `ghl-email-flows` |
| Landing/funnel/VSL pages | `ghl-landing-pages` |
| Browser lane (anything BROWSER-ONLY) | `ghl-browser` |

Each playbook carries its own `references/operations.md` (catalog slice by business task).
This master stays the router: ladder, matrix, cross-cutting quirks, safety baseline.

## Email flows

Building or changing flow emails? Load **`/ghl-email-flows`** — the playbook that pairs
this matrix with the branded builders and the review loop. Short version: emails are
API-pushable as templates (legacy `/emails/builder` family, `updatedBy` required); the
workflow step that sends them is browser-only.

## API quirks (cross-cutting)

- Email send via conversations: `html` field for Email, `message` for SMS — mixing = 422.
- Requests snake_case, responses camelCase.
- Cloudflare blocks default python User-Agent — set a custom one.
- 429 → backoff 2s/4s/8s; bulk ops 0.5s spacing; 5xx retry ×3.
- One location per token/MCP connection. Agency-level ops (SaaS, snapshots, user create,
  locationToken) need an agency token.
- Tags are strings not IDs; add = POST, remove = DELETE with body.

## Safety rules

1. NEVER delete contacts without explicit approval.
2. NEVER send bulk SMS/email without approval — individual agent follow-ups are fine.
3. NEVER modify pipeline structure (it's browser-only anyway — treat that as a gate, not a dare).
4. Live workflows and their message content: follow the team's review loop (see
   /ghl-email-flows) — never hot-edit sending copy without an approved source.
5. Check for an existing opportunity before creating one; tag contacts on every action.
6. `execute_operation` writes: deliberate idempotencyKey, verify the write landed, never
   blind-retry.

## Location setup (per install)

Run once and record here: `ghl pipelines` (pipeline/stage IDs), `ghl users` (user IDs),
`ghl calendars` (calendar IDs), social accounts via
`mcp__ghl-official__social-media-posting_get-account`. Location ID + token live in
environment variables, or your password manager, or the `secrets/ghl.env` file — never in this file.

Router key `sk-1plhl9m` — resolved by the skills index on load.
