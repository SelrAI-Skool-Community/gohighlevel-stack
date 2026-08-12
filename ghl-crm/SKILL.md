---
name: ghl-crm
description: The master GoHighLevel operator skill. Use for any GoHighLevel operation, including contact search, opportunity updates, SMS or email, templates, social posts, invoices, calendars, custom values, trigger links, workflows, and API capability questions. Routes work through an optional MCP server, direct REST, the scripts/ghl CLI helper, or the browser fallback. Routes deep domain work to the bundled specialist skills.
---

# GoHighLevel Master Operator⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Operate GoHighLevel end to end. This skill is the ROUTER: every GHL task enters here,
gets matched against the capability matrix, and executes down the ladder. Each task is
either an API call or a flagged browser-lane task.

## The ladder (always in this order)

### 1. MCP lane, optional

Run `claude mcp list` and use the GoHighLevel server name actually registered on the
machine. It may expose fixed operations, full-catalog meta-tools, or both. When
full-catalog tools are available, search for the operation, inspect its schema, then
execute it with deliberate parameters.

- **Write ops require `idempotencyKey`** when the operation schema calls for one.
- 401 "not authorized for this scope" = the Private Integration token lacks that scope.
  Add the scope in Settings, Private Integrations, or use a
  legacy endpoint family that the token already covers (see matrix).
- Writes are live on the real location. Verify after (fetch the record back / preview URL).

### 2. REST lane

Call `https://services.leadconnectorhq.com` directly with the Private Integration Token
from repo-root `secrets/ghl.env`, the documented API version header, and the endpoint in
the relevant operations reference. This lane works without MCP.

### 3. `scripts/ghl` CLI lane

Run the repo-root `scripts/ghl <command>` helper for contacts, opportunities,
conversations, calendars, workflows, custom values, and raw endpoint calls. It reads
`secrets/ghl.env` and works without MCP.

### 4. Browser fallback for browser-only tasks
Check `references/capability-matrix.md` FIRST. If the task is in the browser-only registry
(workflow builder, funnel/page builder, form/survey builder, pipeline stages, memberships
builder, documents builder, snapshots load, A2P/phone config, PIT scopes, reporting), do
not hunt for endpoints. Open the `ghl-browser` skill and reuse the signed-in session.

## The capability matrix (routing truth)

`references/capability-matrix.md`, per-domain verdicts (API-FULL / API-PARTIAL /
BROWSER-ONLY), the browser-only registry, the email-templates lever, and live-verified
quirks. `references/v2-catalog.json`, all 570 operations (operationId, domain, method,
  path, kind, scopes) for lookup. Example:
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

Each specialist playbook carries its own operations reference, organised by business task.
This master stays the router: ladder, matrix, cross-cutting quirks, safety baseline.

## Email flows

Building or changing flow emails? Load **`ghl-email-flows`**, the playbook that pairs
this matrix with the branded builders and the review loop. Short version: emails are
API-pushable as templates (legacy `/emails/builder` family, `updatedBy` required); the
  workflow step that sends them is browser-only.

## API quirks (cross-cutting)

- Email send via conversations: `html` field for Email, `message` for SMS, mixing = 422.
- Requests snake_case, responses camelCase.
- Cloudflare blocks default python User-Agent, set a custom one.
- 429 → backoff 2s/4s/8s; bulk ops 0.5s spacing; 5xx retry ×3.
- One location per token/MCP connection. Agency-level ops (SaaS, snapshots, user create,
  locationToken) need an agency token.
- Tags are strings not IDs; add = POST, remove = DELETE with body.

## Safety rules

1. NEVER delete contacts without explicit approval.
2. NEVER send bulk SMS/email without approval, individual agent follow-ups are fine.
3. NEVER modify pipeline structure (it's browser-only anyway, treat that as a gate, not a dare).
4. Live workflows and their message content: follow the team's review loop (see
   ghl-email-flows), never hot-edit sending copy without an approved source.
5. Check for an existing opportunity before creating one; tag contacts on every action.
6. `execute_operation` writes: deliberate idempotencyKey, verify the write landed, never
   blind-retry.

## Location setup (per install)

Run once with `scripts/ghl`: `pipelines` for pipeline and stage IDs, `users` for user IDs,
and `calendars` for calendar IDs. Query social accounts through the active MCP server,
direct REST, or `scripts/ghl raw`. The location ID and token live in repo-root
`secrets/ghl.env`, never in this file.

Router key `sk-1plhl9m` — resolved by the skills index on load.
