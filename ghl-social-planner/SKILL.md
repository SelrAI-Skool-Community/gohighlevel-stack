---
name: ghl-social-planner
description: Runs GoHighLevel's Social Planner, covering connected account audits, single and bulk post scheduling, evergreen queues, comment moderation, and post/account statistics. Use when the user says "schedule a social post", "post this to Facebook and Instagram", "bulk-schedule these posts", "set up an evergreen queue", "recycle old posts", "check my connected social accounts", "reply to comments on that post", "pull social stats for last month", "upload this image to the media library", "clone that queue item", "what's connected to GHL social", or "queue up a week of posts". Domain playbook under ghl-crm, pairs with ghl-browser for OAuth connect flows and CSV file upload.
---

# GHL Social Planner⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Runs the Social Planner lane of GoHighLevel for a small service business:
connected-account hygiene, scheduling single
posts and full content calendars across Facebook, Instagram, LinkedIn, TikTok, Google
Business Profile and more, evergreen recycling queues, comment replies, and performance
reporting. This is a domain playbook: the ladder, cross-cutting quirks, and safety
baseline live in `ghl-crm`, read that first if anything here is unclear.

## Execution ladder (domain-specific)

1. **MCP, optional**: run `claude mcp list` and use the registered GoHighLevel server
   name. Use fixed social operations when available. Otherwise search, describe, then
   execute the relevant full-catalog operation.
2. **Direct REST**: use the method and path in `references/operations.md` with the token
   from repo-root `secrets/ghl.env`.
3. **CLI**: use repo-root `scripts/ghl raw METHOD /path [body]`. REST and CLI work
   without MCP.

Full operation list, reorganised by task, sits in `references/operations.md`.

## Core playbooks

### 1. Audit connected social accounts
Goal: know exactly what's connected before touching anything else.
1. `get-account` lists every connected account for
   the location: accountId, platform, display name, connection status.
2. Any account flagged expired or disconnected, run `get-oauth-accounts` to check token
   health for that specific platform/accountId.
3. Verify: cross-check the returned list against the platforms the task actually needs
   (for example "the Facebook page and the Instagram business account") before
   scheduling anything against an accountId that doesn't exist or is stale.

### 2. Schedule a single post across platforms
Goal: one piece of content, fanned out to N connected accounts, landing as a draft or
scheduled item, never live without an explicit ask.
1. `get-account` confirms the target accountIds are live.
2. If media is involved, upload/resolve it first (playbook 7) and get its URL/id.
3. `create-post` with `locationId`, `accountIds: [...]`, the caption/summary text,
   `media: [{url, type}]`, platform-specific fields where relevant (a title field for
   Google Business Profile or YouTube), `status: "scheduled"` (or `"draft"`),
   `scheduleDate` in ISO format, and a stable `idempotencyKey`.
4. Verify: `get-post` on the returned id confirms `status`, `scheduleDate`, and
   `accountIds` all match what was requested.

### 3. Bulk-schedule via CSV (or a parsed list)
Goal: load a content calendar (30 days of posts, say) in one pass.
- **Preferred, pure API path**: parse the source CSV/sheet locally, then loop
  `create-post` once per row with a stable per-row `idempotencyKey` (a hash of
  date+platform+caption) and the rate-limit spacing from `ghl-crm` (0.5s between
  writes). This avoids the native CSV importer entirely and is fully scriptable.
- **Native CSV importer path** (the file itself is uploaded through the browser, see
  Browser-only edges): once a CSV has been dropped into GHL's own importer, drive
  everything after the upload via API. `get-upload-status` polls parse progress,
  `get-csv-post` reviews a parsed row before it goes live, `delete-csv-post`/
  `delete-csv` drops bad rows or scraps the whole batch, `start-csv-finalize` commits
  it. Run `set-accounts` first if the CSV's account references need mapping to real
  accountIds.
- Verify either path with `get-posts` (list) filtered by the date range, confirming the
  expected count landed with the right `scheduleDate` values.

### 4. Manage categories/queues for evergreen recycling
Goal: a self-refilling queue that keeps recycling a pool of evergreen content.
1. `fetchAvailableCategories` shows what evergreen categories exist for the location.
2. `createQueue` creates a new queue tied to a category, the target accounts, and
   posting slots.
3. `fetchSlots` checks or generates the queue's posting time slots.
4. `createQueueItem` adds a piece of evergreen content to the queue (loop for a batch).
5. To edit an existing queue's calendar safely: `startEditSession`, then
   `fetchEditSessionCalendar`, make changes, then `saveEditSession` (or
   `discardEditSession` to abandon without touching the live calendar).
6. Recycling mechanics: `resetQueueItem` requeues an item after it's posted,
   `cloneQueueItem` duplicates a piece of evergreen content that's working,
   `deleteCurrentActivePostAndScheduleNext` pulls whatever's live right now and
   immediately promotes the next queued item (treat as a publish action, not a quiet
   delete, see Safety rails).
7. Verify: `fetchQueueItems` confirms items landed in the queue, `fetchQueueById`
   confirms the queue's own config (accounts, category, cadence).

### 5. Reply to / moderate comments
Goal: engage with or moderate comments on a published post.
1. `get-comment-list` (`POST /comments/{platform}/list`) with the post/external ID
   pulls the comment thread for that platform.
2. `create-comment` (`POST /comments/{platform}`) replies.
3. `create-like` / `delete-like` likes or unlikes a comment as a light moderation
   signal.
4. There is no delete-comment op in this pack, hiding or deleting a comment on the
   native platform is not API-reachable here (see Browser-only edges).

### 6. Pull post + account statistics
Goal: performance reporting for a date range or a specific account.
1. `get-statistics` (`POST /social-media-posting/statistics`) with locationId, date
   range, and accountIds/platform filter returns per-post or per-account metrics.
2. `get-posts` (list, filtered by date range/status) cross-references which posts
   actually ran in that window.
3. Combine into the report, spot-check any single post's numbers against `get-post`
   before quoting a figure back to the user.

### 7. Upload media to the library and attach to posts
Goal: get an asset into the shared media library, then reference it from a post.
1. This pack's 6 `medias` ops are library management (list, folder, rename/retag,
   delete), none of them is a raw multipart file upload. Before assuming that means
   browser-only, search the registered GHL MCP server for `upload media file` first,
   the full 570-op catalog may carry an upload endpoint this domain slice doesn't
   surface. If `describe_operation` confirms one, use it (organise into a folder first
   with `create-media-folder` for a campaign-sized batch).
2. If no upload op resolves, host the asset externally (existing CDN, or an already-
   uploaded location asset) and pass its URL straight into `create-post`'s `media`
   field, GHL accepts hosted URLs, not just library IDs.
3. `fetch-media-content` (`GET /medias/files`) lists the library and grabs an existing
   asset's URL/id for reuse.
4. Reference the resolved URL/id in `create-post` or `edit-post`'s `media` array.
5. Housekeeping: `update-media-object`/`bulk-update-media-objects` renames or retags,
   `delete-media-content`/`bulk-delete-media-objects` cleans up unused assets.
6. Verify: `get-post` on the created post confirms the media array resolved to a
   reachable URL.

## Domain gotchas

- Several "list" ops in this pack (`get-posts`, `fetchQueues`, `fetchQueueItems`,
  `get-comment-list`, `get-statistics`) are `POST` under the hood, the filters live in
  the request body, not the query string. The v2 catalog's `kind: write` label on these
  just reflects the HTTP verb, they are read-only requests.
- Categories come in two unrelated families: legacy location categories
  (`get-categories-location-id`/`get-categories-id`, read-only in this slice) versus the
  queue "category/queues" system (`createQueue` and friends, full CRUD). Evergreen
  recycling always uses the queue family, never the legacy one.
- Comment and statistics endpoints are keyed by `{platform}` in the path (`facebook`,
  `instagram`, `linkedin`, and so on), pull that value from `get-account`'s returned
  `platform` field rather than guessing it.
- `attach-oauth-accounts` reattaches or refreshes a token GHL already has a handshake
  for. It does not perform the initial platform login/consent screen, that is always a
  browser action (see below).
- `deleteCurrentActivePostAndScheduleNext` is not a soft delete: it takes down whatever
  is live right now and immediately promotes the next queued item into its place. Treat
  it as a publish-adjacent action.
- Write ops need a deliberate `idempotencyKey`, same rule as everywhere else in GHL,
  never blind-retry a failed write.

## Browser-only edges

- **Connecting a brand-new social account** (the first-time OAuth consent popup for
  Facebook, Instagram, LinkedIn, TikTok, Google Business Profile, and so on) happens
  inside GHL's own "Connect Account" flow in Social Planner settings. Route to
  `ghl-browser`.
- **Uploading the raw CSV file** for the native bulk importer has no confirmed
  multipart upload endpoint in this domain slice. Drop the file via the browser, then
  drive everything after upload (status polling, row review, finalize, delete) via API.
- **Deleting or hiding a single comment** on the native platform: only create/reply/
  like/unlike are exposed here, comment removal is a native-app or browser action.

## Safety rails

Inherits `ghl-crm`'s baseline (no bulk sends without approval, deliberate
idempotencyKey, verify every write, never delete contacts). Domain-specific:

1. **Scheduled and draft posts are autonomous.** Building out a content calendar with
   `status: "scheduled"` or `"draft"` needs no sign-off, that's the whole point of this
   skill.
2. **Anything that goes live on a real, outward-facing account right now needs an
   explicit ask first.** That includes any post created or edited with an immediate-
   publish status, and `deleteCurrentActivePostAndScheduleNext` (it publishes the next
   queue item the moment it runs).
3. **Bulk destructive ops need a preview before they run.** `bulk-delete-social-planner-
   posts` and `delete-account` act at scale, show the user the count and date range
   being touched before executing.
4. **CSV finalize commits a whole batch live to the calendar.** Review the parsed rows
   with `get-csv-post` before calling `start-csv-finalize`.

Router key `sk-19u2bfa` — resolved by the skills index on load.
