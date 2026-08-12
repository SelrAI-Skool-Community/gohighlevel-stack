# GHL Capability Matrix — API/MCP vs Browser-Only

Verified 2026-07-12 against the live v2 MCP operation catalog (570 operations, 37 domains),
the official OpenAPI specs (github.com/GoHighLevel/highlevel-api-docs), and live probes on a
real location. This file is the routing truth: check it BEFORE deciding how to execute any
GHL task. If a task's domain says BROWSER-ONLY, do not burn time hunting for an endpoint —
go straight to the browser lane (skill `ghl-browser`, engine agent-browser).

## How to read this

- **API-FULL** — do it via ghl-v2 `execute_operation` (or a fixed ghl-official tool / raw REST).
- **API-PARTIAL** — some operations exist; the listed gaps are browser-only.
- **BROWSER-ONLY** — no public API surface. Flag it, use the browser lane.

## The ladder (always in this order)

1. **ghl-official fixed tools** — 36 tools (expanded from 21 by GHL), fastest for common CRM ops (contacts, opps, convos, calendars, social, blogs, emails, payments).
2. **ghl-v2 meta-tools** — everything else the API can do: `search_operations` → `describe_operation` → `execute_operation`. 570 ops.
3. **Raw REST / bash `ghl` helper** — when MCP is unavailable or for bulk loops. Base `https://services.leadconnectorhq.com`, header `Version: 2021-07-28`.
4. **Browser lane** — skill `ghl-browser` (agent-browser + 2FA-via-Gmail). Codex browser lane is the cross-agent alternative.

## Domain matrix

| Domain | Ops | Verdict | Notes |
|---|---|---|---|
| contacts | 31 | API-FULL | CRUD, search, upsert, tags, tasks, notes, followers, campaign/workflow enrol |
| conversations | 20 | API-FULL | search, send SMS/Email/WA/IG/FB, attachments, recordings, transcriptions |
| calendars | 59 | API-FULL | calendars, groups, events, free slots, block slots, resources, notifications |
| opportunities | 12 | API-PARTIAL | CRUD/search/status OK. **Pipelines/stages CRUD = BROWSER-ONLY** (GET pipelines only) |
| invoices | 37 | API-FULL | invoices, templates, recurring schedules, estimates (+send, convert), text2pay |
| products | 27 | API-FULL | products, prices, inventory, collections, reviews |
| payments | 22 | API-PARTIAL | orders/transactions/subscriptions READ; record-payment, coupons CRUD, custom providers |
| social-planner | 43 | API-FULL | posts CRUD, bulk CSV, OAuth attach, categories/queues, comments, stats |
| emails | 18 (v3) + builder | API-FULL* | See "Email templates & campaigns" below — the load-bearing one |
| medias | 6 | API-FULL | upload/list/update/folders — powers all image assets for emails/posts |
| blogs | 7 | API-PARTIAL | create/update posts, no post DELETE, no blog-site create |
| links (trigger links) | 6 | API-FULL | full CRUD + search |
| locations | 26 | API-PARTIAL | custom values CRUD, custom fields CRUD, tags CRUD, recurring tasks. Location email/sms "marketing templates": GET+DELETE only |
| custom-fields (v2) | 8 | API-FULL | fields + folders, all object types |
| objects (custom objects) | 9 | API-FULL | schemas + records CRUD + search (no schema delete) |
| associations | 10 | API-FULL | associations + relations |
| knowledge-base | 14 | API-FULL | KBs, FAQs, website crawler train (powers Conversation AI) |
| conversation-ai / voice-ai | 11+ | API-FULL | agents CRUD, actions, call logs; agent-studio: create/execute/promote |
| chat-widget | 7 | API-FULL | CRUD + clone (v3) |
| forms | 2 | **BROWSER-ONLY builder** | API = list + submissions read only. No create/edit, no fields, no submit endpoint |
| surveys | 2 | **BROWSER-ONLY builder** | read-only list + submissions |
| funnels | 7 | **BROWSER-ONLY builder** | API = list funnels/pages + count + **redirects CRUD** (only write). No page content read/write |
| workflows | 1 | **BROWSER-ONLY** | API = `GET /workflows/` name list ONLY. No steps, no create/edit, no workflow emails. Only write anywhere: enrol contact `POST /contacts/{id}/workflow/{workflowId}` |
| campaigns (legacy) | 1 | BROWSER-ONLY config | GET list; contact add/remove via contacts domain |
| users | 6 | API-FULL | create needs agency-level token |
| businesses | 5 | API-FULL | |
| store | 17 | API-FULL | shipping zones/rates/carriers, store settings |
| saas | 22 | API (agency token) | enable/pause/rebill — agency-level auth required |
| snapshots | 4 | API-PARTIAL | list + share-link + push-status. **Create/load snapshot = BROWSER-ONLY** |
| proposals (documents) | 4 | API-PARTIAL | list + SEND only. **Document/template builder = BROWSER-ONLY** |
| phone-system | 4 | API-PARTIAL | pools/available/purchase/active. **Config/release/A2P = BROWSER-ONLY** |
| courses/memberships | 1 | **BROWSER-ONLY builder** | single bulk-import endpoint; no lessons/enrolments/progress |
| ad-publishing | 95 | API-FULL | HighLevel Ad Manager: FB/Google/LinkedIn campaigns, publish/pause, reporting, audiences |
| brand-boards | 11 | API-FULL | + brand voices (v3) |
| affiliate-manager | 4 | READ-ONLY API | payouts/commissions read |
| marketplace / oauth | 11 | API | app rebilling, installedLocations, locationToken |

## BROWSER-ONLY registry (flag these — no public API, confirmed)

1. **Workflow builder** — create/edit workflows, steps, actions, the Triggers tab, and the emails/SMS inside workflow steps. (Our email-flows case.)
2. **Funnel / website page builder** — page content read AND write.
3. **Form builder** and **Survey builder**.
4. **Pipeline + stage create/rename/reorder** (moving opportunities between existing stages IS API). SOFTENING 2026-07-12: our PIT now carries the new `pipelines.write` scope and a raw `POST /opportunities/pipelines` probe returned 422 validation (auth passed) — the endpoint EXISTS but isn't in the v2 catalog yet. Pipeline CRUD via API may be arriving; re-probe before defaulting to browser lane. Structure writes still need the account owner's explicit OK (safety rule 3).
5. **Memberships / courses builder**.
6. **Documents & Contracts builder** (send-only API).
7. **Snapshot create/load**.
8. **A2P 10DLC / Trust Center / phone number configuration**.
9. **Reporting dashboards** and agency-wide views (API is sub-account-scoped).
10. **Private Integration token scope management** (Settings → Private Integrations).
11. **Location "marketing templates" create/update** (`/locations/{id}/templates` is GET+DELETE only).

Evidence for the big four: workflows spec has 1 path; funnels spec write = redirects only; forms spec = 3 read paths; pipelines = single GET. Top ideas-board requests confirm (workflow CRUD, pipeline API, funnel/form API, "Become An API First Company").

## Email templates & campaigns (the email-flows lever — live-proven 2026-07-12)

Two API generations, BOTH usable:

**Legacy builder family — works with our current token TODAY:**
- `POST /emails/builder` `{locationId, name, type:"html"}` → returns template `id`
- `POST /emails/builder/data` `{locationId, templateId, html, editorType:"html", previewText, updatedBy}` — **`updatedBy` is REQUIRED** (422 without it). Accepts full raw HTML; also accepts `dnd` JSON for drag-drop-editor templates (schema undocumented — round-trip an existing template's dnd rather than hand-writing it)
- `GET /emails/builder?locationId=&limit=&search=` — list
- `DELETE /emails/builder/{locationId}/{templateId}`
- Success returns a Firebase `previewUrl` — fetch it to verify the render.

**v3 templates + campaigns (in the v2 MCP catalog):**
- `/emails/locations/{locationId}/templates` CRUD + import + folders — needs `emails/templates.*` scope (our PIT HAS it as of 2026-07-12 — verified 200 via ghl-v2 `list-email-templates`). NOTE: raw REST to these `/emails/locations/...` paths 404s at the public gateway; route them through ghl-v2 `execute_operation`, which maps them correctly.
- Email CAMPAIGNS: create/update/schedule/delete + stats (`emails/campaigns.*`) — full campaign sends via API
- `GET .../campaigns/workflows` — read workflow email campaign entries (read-only window into workflow emails)

**What this means for flows:** branded emails are built as code, pushed as GHL email templates via API, verified via previewUrl. The ONLY manual/browser step left is attaching the template inside the workflow email step (workflow builder = browser-only).

**BETTER (proven 2026-07-14, Install nurture v3 port): skip the attach entirely.** Every workflow email step already has a hidden BACKING template in the emails system. Overwrite IT and the workflow sends the new body immediately — no UI, no publish cycle:
1. Discover the backing id: open the workflow in agent-browser with `network requests --filter templateId` on, click the email step → the app fires `GET /emails/campaigns/{loc}/template?...actionId=...&templateId=<BACKING_ID>`.
2. `POST /emails/builder/data` with that templateId + new html (+updatedBy) → `{ok:true, previewUrl}`. Verify via previewUrl (GHL adds Outlook mso fixes; text stays 1:1).
Still browser-only: adding steps (waits/SMS), SMS bodies, template *selection* swaps (the panel's Save action can hang forever and silently lose the change — never trust it; verify by reload). Full recipe: memory `ghl-workflow-email-api-trick.md`.

## Cross-cutting quirks (live-verified)

- `execute_operation` (ghl-v2): write ops need `idempotencyKey` (any stable string) or they 400. Ops carry `requiresApproval: true` — supply the key deliberately, never retry-loop a write blind.
- 401 "not authorized for this scope" from v2 execute = the PIT is missing that scope, NOT a bug. Fix: GHL Settings → Private Integrations → edit scopes (browser lane), or use the legacy endpoint family if one exists.
- REST: header `Version: 2021-07-28` required. Custom User-Agent (Cloudflare blocks python-requests default).
- Rate limits: 429 → exponential backoff (2s/4s/8s); bulk loops 0.5s spacing.
- Sub-account scope: one location per token/MCP connection. Agency ops (SaaS, snapshots, user-create, locationToken) need an agency token.
- MCP inherits every API gap — the v2 MCP cannot build workflows/funnels/forms either. The matrix above IS the MCP's ceiling.
- `GET /emails/builder` list can LAG behind newly API-created templates (create/update/delete by ID still work; keep the returned IDs). Verify via the returned previewUrl, not the list.
- Private Integrations UI (scope edit / create with sensitive scopes): the final Confirm can hang server-side under automation (observed 2026-07-12, two flows) — BUT the save can land anyway. Before re-staging or asking for a manual click, PROBE a gated endpoint: 401 = scope really missing; 200/422 = the "hung" save actually went through (proven 2026-07-12).
