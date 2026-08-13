# GHL Capability Matrix: API, MCP, and browser-only work⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

This file is the routing truth. Check it before choosing an execution lane. When a task
is browser-only, use `ghl-browser` instead of hunting for an endpoint.

## How to read this

- **API-FULL**: use the optional MCP server, direct REST, or `scripts/ghl`.
- **API-PARTIAL**: some operations exist; the listed gaps are browser-only.
- **BROWSER-ONLY**: no public API surface. Use `ghl-browser`.

## The ladder (always in this order)

1. **MCP, optional**: run `claude mcp list` and use the registered GoHighLevel server name.
2. **Direct REST**: use the Private Integration Token and the documented endpoint.
3. **`scripts/ghl` CLI**: use named commands or `scripts/ghl raw` with the same token.
4. **Browser fallback**: use `ghl-browser` only for the browser-only registry below.

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
| emails | 18 (v3) + builder | API-FULL* | See "Email templates & campaigns" below |
| medias | 6 | API-FULL | upload/list/update/folders; powers image assets for emails/posts |
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
| saas | 22 | API (agency token) | enable/pause/rebill; agency-level auth required |
| snapshots | 4 | API-PARTIAL | list + share-link + push-status. **Create/load snapshot = BROWSER-ONLY** |
| proposals (documents) | 4 | API-PARTIAL | list + SEND only. **Document/template builder = BROWSER-ONLY** |
| phone-system | 4 | API-PARTIAL | pools/available/purchase/active. **Config/release/A2P = BROWSER-ONLY** |
| courses/memberships | 1 | **BROWSER-ONLY builder** | single bulk-import endpoint; no lessons/enrolments/progress |
| ad-publishing | 95 | API-FULL | HighLevel Ad Manager: FB/Google/LinkedIn campaigns, publish/pause, reporting, audiences |
| brand-boards | 11 | API-FULL | + brand voices (v3) |
| affiliate-manager | 4 | READ-ONLY API | payouts/commissions read |
| marketplace / oauth | 11 | API | app rebilling, installedLocations, locationToken |

## BROWSER-ONLY registry (flag these, no public API, confirmed)

1. **Workflow builder**: create/edit workflows, steps, actions, the Triggers tab, and the emails/SMS inside workflow steps.
2. **Funnel / website page builder**: page content read and write.
3. **Form builder** and **Survey builder**.
4. **Pipeline and stage create/rename/reorder**. Moving opportunities between existing stages is available through the API.
5. **Memberships / courses builder**.
6. **Documents & Contracts builder** (send-only API).
7. **Snapshot create/load**.
8. **A2P 10DLC / Trust Center / phone number configuration**.
9. **Reporting dashboards** and agency-wide views (API is sub-account-scoped).
10. **Private Integration token scope management** (Settings → Private Integrations).
11. **Location "marketing templates" create/update** (`/locations/{id}/templates` is GET+DELETE only).

## Email templates and campaigns

Two API generations are usable:

**Legacy builder family:**
- `POST /emails/builder` `{locationId, name, type:"html"}` returns template `id`
- `POST /emails/builder/data` `{locationId, templateId, html, editorType:"html", previewText, updatedBy}`. **`updatedBy` is required** and omission returns 422. It accepts full raw HTML and `dnd` JSON. Round-trip an existing template's `dnd` value rather than writing that schema by hand.
- `GET /emails/builder?locationId=&limit=&search=` lists templates
- `DELETE /emails/builder/{locationId}/{templateId}`
- Success returns a `previewUrl`. Fetch it to verify the render.

**v3 templates and campaigns:**
- `/emails/locations/{locationId}/templates` supports CRUD, import, and folders and needs `emails/templates.*` scope. If the public REST gateway returns 404 for this path, use the full-catalog operation exposed by the registered GHL MCP server.
- Email campaigns support create, update, schedule, delete, and statistics with `emails/campaigns.*` scopes.
- `GET .../campaigns/workflows` reads workflow email campaign entries.

**What this means for flows:** build emails as code, push them as templates, and verify
the preview URL. Attaching a template inside a workflow email step is browser-only.

An existing workflow email step has a backing template in the email system:

1. Open the workflow in `ghl-browser`, inspect network requests filtered by `templateId`,
   and click the email step. Record the backing template ID from the template request.
2. `POST /emails/builder/data` with that template ID, the new HTML, and `updatedBy`.
3. Open the returned preview URL, then reload the workflow and verify the change.

Adding waits or SMS steps, editing SMS bodies, and changing template selection remain
browser-only.

## Cross-cutting quirks

- Full-catalog write operations may require `idempotencyKey`. Supply a stable key and never blind-retry a write.
- 401 "not authorized for this scope" means the token is missing that scope. Edit the Private Integration scopes or use a permitted endpoint family.
- REST: header `Version: 2021-07-28` required. Custom User-Agent (Cloudflare blocks python-requests default).
- Rate limits: 429 → exponential backoff (2s/4s/8s); bulk loops 0.5s spacing.
- Sub-account scope: one location per token/MCP connection. Agency ops (SaaS, snapshots, user-create, locationToken) need an agency token.
- MCP inherits every API gap. It cannot build workflows, funnels, or forms.
- `GET /emails/builder` can lag behind newly created templates. Keep returned IDs and verify through the preview URL.
- If the Private Integrations confirmation screen appears to hang, probe a gated endpoint before retrying. A 401 means the scope is missing. A 200 or 422 means the save landed.

Router key `sk-1plhl9m` — resolved by the skills index on load.
