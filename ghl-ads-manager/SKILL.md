---
name: ghl-ads-manager
description: Runs GoHighLevel's built-in Ad Manager for Facebook/Instagram, Google, and LinkedIn campaigns entirely through the GHL API. Use when the user says "launch a Facebook ad campaign", "check what ad accounts are connected", "audit our ad platforms", "pause that Google campaign", "resume the LinkedIn ads", "pull the ad performance report", "how's the campaign spend looking", "build a custom audience for the service offer ad", "upload this ad creative", "set up a new ad set", "turn that ad back on", or "what platforms can we run ads on". This is the programmatic bridge to LinkedIn and Google ads in the stack and the fastest lane for Facebook/Instagram ads inside this stack. Pairs with ghl-crm for routing and ghl-browser for first-time OAuth connections and LinkedIn audience building.
---

# GHL Ad Manager Playbook⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Runs paid campaigns for Facebook/Instagram, Google, and LinkedIn out of GoHighLevel's
built-in Ad Manager (`ad-publishing` domain, 95 operations). This is the bridge for
platforms the rest of the stack cannot reach directly: LinkedIn and Google have no other
API or MCP connection anywhere in the toolset, so every LinkedIn/Google ad task routes
here. For anything already living inside a GHL location
(service enquiry campaigns, lead generation tied to GHL contacts/pipelines), this is the
faster, contact-aware lane.

## Execution ladder

1. **MCP, optional**: run `claude mcp list` and use the registered GoHighLevel server
   name. Ad publishing needs its full-catalog tools: search, describe, then execute the
   relevant `ad-publishing` operation.
2. **Direct REST**: use the method and path in `references/operations.md` with the token
   from repo-root `secrets/ghl.env`.
3. **CLI**: use repo-root `scripts/ghl raw METHOD /path [body]`. REST and CLI work
   without MCP.

## Core playbooks

### 1. Audit connected ad accounts and platforms
Goal: know what's live before touching anything.
1. `fb-get-integration` for Facebook app connection status.
2. `fb-get-ad-accounts` for connected ad account IDs, names, currencies.
3. `fb-get-pages` plus `fb-get-pixels` for connected Pages and pixels (needed for any FB ad).
4. `google-get-integration` then `google-get-ad-accounts`.
5. `li-get-integration` then `li-get-ad-accounts`.
6. Verify: report each platform as connected (with account IDs) or absent. A platform
   with no integration record needs a first-time OAuth connect, and that step is
   browser-only (see below); everything after it is API.

### 2. Launch a Facebook/Instagram campaign, draft first
Goal: build campaign, ad set, and ad as a draft, verify the structure, gate activation.
1. `describe_operation fb-upsert-campaign` to confirm required fields for this token's
   schema version (objective, adAccountId, name, status).
2. `execute_operation fb-upsert-campaign` with `idempotencyKey` like `fb-camp-<slug>-<date>`,
   body `status: "PAUSED"`. Never create with `status: "ACTIVE"`. Returns `campaignId`.
3. `fb-search-targeting` for interest/location IDs, then `execute_operation fb-upsert-adset`
   (new idempotencyKey) referencing `campaignId`, budget, targeting, `status: "PAUSED"`.
4. New creative asset: upload via the `medias` domain first (outside ad-publishing), get
   the hosted URL. Then `execute_operation fb-upsert-ad` (new idempotencyKey) referencing
   `adSetId`, the creative URL, primary text, headline, link, CTA, `status: "PAUSED"`.
5. Verify: `fb-get-campaign` and `fb-get-campaign-publishing-progress` to fetch the built
   structure back and eyeball every field.
6. Stop. Report the full structure (objective, budget, audience, creative) in plain terms.
   Only call `fb-publish-campaign` (first activation) or `fb-resume-campaign` /
   `fb-resume-adset` / `fb-resume-ad` (reactivating something already published) after an
   explicit go-ahead in the conversation. Those are the calls that spend real money.

### 3. Launch a Google Ads campaign, draft first
1. `google-get-ad-accounts` to confirm the target account.
2. `google-search-targeting`, `google-get-target-interests`, and `google-get-keyword-ideas`
   for keyword and audience research.
3. `describe_operation google-upsert-campaign` first. The opId says "campaign" but the
   path is `/ad-publishing/google/ads`, so confirm the live body shape rather than
   guessing from the name. `execute_operation` with `idempotencyKey`, `status: "PAUSED"`.
4. `google-upsert-assets` to attach headlines, descriptions, images (Google's creative
   lives in its own assets store, not the shared medias domain).
5. Verify: `google-get-campaign-by-id` fetch-back.
6. Gate: `google-publish-ad` activates spend, explicit go-ahead required first.

### 4. Launch a LinkedIn campaign, draft first
1. `li-get-ad-accounts` to confirm the target account.
2. `li-search-targeting` for audience facets (no dedicated LinkedIn audience store in this
   API, see gotchas).
3. `describe_operation li-upsert-campaign-group` then `execute_operation` with
   `idempotencyKey`, drafted status.
4. Verify: `li-get-campaign-group` fetch-back.
5. Gate: `li-publish-campaign-group` activates spend, explicit go-ahead required. After
   first publish, every further status change (pause/resume/archive) goes through
   `li-update-ad-status`, LinkedIn's only lifecycle lever in this catalog.

### 5. Pause or resume a live campaign, ad set, or ad
- Facebook: `fb-pause-campaign` / `fb-pause-adset` / `fb-pause-ad` any time, no approval
  needed (pausing only stops spend). `fb-resume-*` restarts spend, same gate as activation.
- Google: no dedicated pause/resume op in this catalog. Status is a field inside
  `google-upsert-campaign`; `describe_operation` first to confirm the enum, then re-run
  upsert with the same `campaignId` and the new status, new `idempotencyKey`.
- LinkedIn: `li-update-ad-status` (PATCH), `describe_operation` first for the exact status
  enum. Setting to paused is safe autonomously; setting to active needs the go-ahead.
- Verify every pause/resume by fetching the record back and confirming the status field
  actually flipped. Don't trust the write response alone.

### 6. Pull a performance/reporting snapshot
All reporting ops are read-only, safe to run any time, no approval needed.
- Facebook: `fb-get-reporting` (account-level), then `fb-get-campaign-reporting/{campaignId}`
  for drill-down, then `fb-get-reporting-list` for saved report definitions.
- Google: `google-get-reporting`, then `google-get-campaign-reporting/{campaignId}`, then
  `google-get-reporting-list`.
- LinkedIn: `li-get-ad-analytics`, then `li-get-campaign-group-reporting/{campaignGroupId}`,
  then `li-get-reporting-list`.
Pick a date range, pull account-level first, then drill into a named campaign only if asked.

### 7. Manage audiences and segments
- Facebook: `fb-get-custom-audiences` / `fb-get-custom-audience-by-id` to inspect,
  `fb-update-custom-audience` to create or edit (confirm via `describe_operation` whether
  a new `audienceId` creates or requires a separate call), `fb-add-custom-audience-member`
  / `fb-remove-custom-audience-member` / `fb-batch-update-audience-members` for list
  membership, `fb-delete-custom-audience` to remove (explicit approval, irreversible).
- Google: `google-get-audiences` / `google-upsert-audience` for audience definitions,
  `google-get-segments` / `google-upsert-segment` / `google-delete-segment` for segments,
  `google-create-offline-user-list-job` to upload a customer list (emails/phones) as a
  Customer Match audience seed.
- LinkedIn: no audience-management endpoint exists in this catalog. `li-search-targeting`
  only covers interest/company facets. Route custom-list or matched-audience work to the
  LinkedIn Campaign Manager UI directly (browser-only edge, see below).

### 8. Upload and attach ad creative
- Facebook and LinkedIn ads reference assets by URL from the shared `medias` domain
  (outside ad-publishing). Upload there first, capture the hosted URL, then pass it in
  the `fb-upsert-ad` body (image/video field) or the LinkedIn ad creative fields inside
  `li-upsert-campaign-group`.
- Google has its own creative store: `google-upsert-assets` (headlines, descriptions,
  images, sitelinks), referenced by asset ID in the campaign body.
- Verify by fetching the ad/campaign back and confirming the creative field is populated
  as expected. There is no dedicated ad-preview endpoint in this catalog.

## Domain gotchas

- opId names and paths don't always match (`google-upsert-campaign` lives at
  `/ad-publishing/google/ads`, `google-publish-ad` activates what is really a campaign).
  Run `describe_operation` before the first use of any op in a session, don't assume the
  name tells you the shape.
- Facebook and Google separate DRAFT (upsert with a paused status) from ACTIVATION
  (a dedicated publish/resume call) into two distinct calls. LinkedIn folds every status
  change after the first publish into one op, `li-update-ad-status`.
- Full custom-audience CRUD with member-level add/remove exists only for Facebook. Google
  audiences are segment/list-based. LinkedIn has no audience endpoint at all here.
- Lead forms in this domain (`fb-create-page-lead-form`, `li-create-lead-form`,
  `fb-create-conversation-form`) are platform-native forms (Facebook Instant Forms,
  LinkedIn Lead Gen Forms) and are API-writable. Don't confuse these with GHL's own form
  builder, which stays browser-only per the master capability matrix.
- Creative assets are not part of ad-publishing for Facebook or LinkedIn, they live in
  the general `medias` domain. Only Google has a dedicated ad-publishing assets store.
- Every write needs a stable, deliberate `idempotencyKey` (ghl-crm rule). Reuse a
  task-derived key (e.g. `fb-camp-launch-<slug>`) so a retry never creates a duplicate
  draft campaign.
- `fb-create-integration` / `google-create-integration` / `li-create-integration` manage
  an already-authorized connection; the first-time OAuth consent screen for a brand new
  ad account still has to happen in the browser (see below) even though these write
  endpoints exist.

## Browser-only edges

- Connecting a NEW ad account or platform for the first time (OAuth consent screen):
  drive it once via `ghl-browser`, Ad Manager settings tab. Every op above only manages
  accounts already connected.
- LinkedIn custom-list or matched-audience building: no endpoint exists in this catalog;
  use the LinkedIn Campaign Manager UI directly, or `ghl-browser` if driving through GHL's
  embedded view.
- Anything inside GHL's own form, funnel, or page builder is a different domain and stays
  browser-only per the master capability matrix. Don't route those tasks here.

## Safety rails

Inherits `ghl-crm`'s baseline: deliberate idempotency, verify every write, no blind
retries. Domain-specific:

1. Building or editing a DRAFT is always autonomous. Campaigns, ad sets, ads, creative,
   and audiences created with a paused/draft status need no approval.
2. ACTIVATING spend always needs an explicit go-ahead in the conversation:
   `fb-publish-campaign`, `fb-resume-campaign`/`adset`/`ad`, `google-publish-ad`,
   `li-publish-campaign-group`, and any `li-update-ad-status` call that moves a campaign
   to an active state. State platform, campaign name, budget, and daily/lifetime spend
   before asking.
3. Pausing a live campaign, ad set, or ad is always safe to do autonomously, it only
   stops spend.
4. Deleting a campaign, ad set, ad, or audience needs explicit approval. It's irreversible
   on the platform side even though GHL only calls one API.
5. Never invent budget, targeting, objective, or creative values. Pull them from the
   user's brief or an existing draft; flag missing inputs instead of guessing.
6. Report every draft build back in plain terms (platform, objective, budget, audience,
   creative) before asking whether to activate it.

Router key `sk-uc260v` — resolved by the skills index on load.
