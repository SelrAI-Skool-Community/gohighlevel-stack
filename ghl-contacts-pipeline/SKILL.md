---
name: ghl-contacts-pipeline
description: Runs the daily CRM engine in GoHighLevel. contacts, opportunities/pipeline, conversations, tags/custom fields, custom objects, trigger links, and workflow/campaign enrolment for a contact database. Use when the user says "add this lead to GHL", "tag this contact", "create an opportunity for X", "move this deal to a new stage", "send a follow-up SMS/email to this contact", "search contacts by tag", "build a segment of people who...", "enrol this contact in the nurture workflow", "check for stale opportunities", "log a note/task on this contact", "who's in the pipeline right now", "set up a custom field for X", "create a trigger link for this event".
---

# GHL Contacts & Pipeline⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Runs the day-to-day CRM lane: the contact database, the sales
pipeline, and every 1:1 conversation and follow-up task that touches a contact record.
This is the domain a new enquiry, a follow-up SMS, a stale-deal sweep, or a segment
build lands in. Invoicing and social live in sibling domain skills;
this one owns contacts, opportunities, conversations, tags/fields, custom objects,
associations, trigger links, and enrolment.

## Execution ladder

1. **ghl-official fixed tools first**: 8 contact tools (create/get/get-all/update/upsert,
   add-tags/remove-tags, get-all-tasks), 4 opportunity tools (get/search/update/get-pipelines),
   3 conversation tools (search/get-messages/send-a-new-message). Fastest lane for the
   90% case, reach for these before the v2 meta-tools.
2. **ghl-v2 meta-tools** for everything in `references/operations.md` the fixed tools
   don't cover (notes, followers, custom objects, associations, trigger links, workflow
   enrolment, business linkage, custom field/value CRUD): `search_operations` then
   `describe_operation` then `execute_operation`.
3. No MCP client (cron/server/Codex batch): `ghl-crm/scripts/ghl_v2_call.py`.
   Full ladder, quirks, and the fixed-tool inventory live in skill `ghl-crm`.

## Core playbooks

### 1. Speed-to-lead (new lead in, first touch inside minutes)
1. Check for a duplicate: `get-duplicate-contact` (email/phone) before creating.
2. Create or upsert: `create-contact` (or `upsert-contact` if the lead might already
   exist from an ad form). Capture source in a custom field, not just a tag.
3. Tag immediately: `add-tags` with a source tag (e.g. `lead-google-ads-aug`). Every
   contact that enters the pipeline gets tagged on the way in.
4. Create the opportunity: `create-opportunity` (or `Upsert-opportunity`) against the
   right `pipelineId`/`stageId`. Read current stage IDs from `get-pipelines` first,
   never hardcode.
5. First-touch message via `send-a-new-message`: SMS uses the `message` field, Email
   uses the `html` field, never both (422). Pick one channel per send.
6. Create a follow-up task: `create-task` on the contact, due within 24h, assigned to
   the right user. This is the safety net if the automated first touch doesn't land
   a reply.
7. Verify: `get-contact` to confirm tags landed, `get-opportunity` to confirm stage.

### 2. Pipeline hygiene sweep (stale opportunity report + stage moves)
1. Pull pipeline structure once: `get-pipelines` (stage IDs, names). Cache for the
   session, don't re-fetch per contact.
2. Pull the working set: `search-opportunities-advanced` filtered by pipeline + stage,
   or `task-search` across the location if the sweep is task-driven instead.
3. Compute staleness client-side (no `daysInStage` filter in the API): compare
   `updatedAt`/`lastStatusChangeAt` on each opportunity against today.
4. For each stale one, log a note (`create-note`) with the finding, then either
   `update-opportunity-status` (won/lost/abandoned) or `update-opportunity` to move
   stage. Never delete an opportunity to "clean up" a report.
5. Roll the sweep into a summary (count per stage, count flagged stale, oldest 5).
   This is a report, not a bulk write: each stage move stays a deliberate, individually
   verified `execute_operation` call.
6. Verify a sample of the moved ones with `get-opportunity` before calling it done.

### 3. Segment build (tags + custom fields + search)
1. Confirm the custom field exists before filtering on it: `get-custom-fields-by-object-key`
   (objectKey `contact`) or `get-custom-fields` (location-scoped shorthand). Create one
   with `custom-fields.create-custom-field` if it's genuinely new, don't guess an ID.
2. Build the filter with `search-contacts-advanced`. Combine tag filters and custom
   field filters in one `filters` array rather than looping single-tag searches.
3. For a reusable segment, don't just save the query: tag every matching contact with
   a durable segment tag (`add-tags`, bulk via `contacts.create-association` for large
   sets) so downstream workflows/campaigns can target the tag directly.
4. Verify: re-run the search and confirm the returned count matches expectations before
   handing the segment off to an enrolment or export.

### 4. Individual follow-up message (conversations)
1. Find or create the thread: `search-conversation` by contactId, or `create-conversation`
   if none exists yet.
2. Send via `send-a-new-message`. **SMS: `message` field. Email: `html` field. Mixing
   either field on the wrong channel or sending both = 422.** Pick the channel first,
   then the field.
3. Attachments: `add-message-attachments` after the message is created, not inline in
   the send body.
4. Log the touch: `create-note` on the contact so the conversation is visible from the
   contact record, not just the inbox.
5. Verify: `get-messages` on the conversation to confirm the send landed and check
   delivery status before assuming it worked.

### 5. Enrol a contact into a workflow or legacy campaign
1. Confirm the workflow/campaign exists and get its ID: `get-workflow` (name+ID list
   only) or `get-campaigns`.
2. Enrol: `add-contact-to-workflow` (preferred, current system) or
   `add-contact-to-campaign` (legacy). This is the ONLY write surface into workflows;
   building or editing the workflow itself is browser-only.
3. To pull someone out: `delete-contact-from-workflow`, `remove-contact-from-campaign`,
   or `remove-contact-from-every-campaign` (full reset, use deliberately).
4. Tag the enrolment (`add-tags`) so reporting can see who's actively in a nurture
   sequence without querying the workflow itself.

### 6. Custom objects for non-contact records
1. Check the schema exists: `get-object-by-location-id` / `get-object-schema-by-key`.
   Create with `create-custom-object-schema` only for a genuinely new record type
   (e.g. "properties", "equipment", "memberships" outside the built-in objects). Schema
   creation has no delete, get the key right first time.
2. Create records: `create-object-record` against the `schemaKey`.
3. Link a record to a contact: `create-relation` (associations domain) using the
   association key from `get-association-key-by-key-name`. This is how a custom
   object record connects back to a contact or opportunity.
4. Search/update/delete records exactly like contacts: `search-object-records`,
   `update-object-record`, `delete-object-record`.

### 7. Trigger-link tracking
1. Create the link: `create-link` with a destination URL and a descriptive name (event
   plus channel, e.g. `renovation-promo-sms-link`). One link per channel/campaign so click
   attribution stays clean.
2. Drop the link into the SMS/email body from playbook 1 or 4 above.
3. Check performance: `search-trigger-links` or `get-link-by-id` for click counts.
4. Retire a link after the campaign ends: `delete-link` rather than leaving dead links
   accumulating. Never delete one that's still live in a sent message.

## Domain gotchas

- Conversations 422: `html` for Email, `message` for SMS. Confirmed cross-cutting quirk
  in ghl-crm, repeated here because this domain sends the most messages.
- Pipeline/stage **structure** (create/rename/reorder stages) is browser-only.
  Moving an opportunity between EXISTING stages via `update-opportunity` or
  `update-opportunity-status` is fully API. Read `get-pipelines` before assuming a
  stage ID.
- `contacts.create-association` (bulk tag update) and `associations.create-association`
  (record-to-record links) are different operations despite the similar opId name.
  Confirm the domain (`contacts` vs `associations`) before calling `describe_operation`.
- Custom object schemas have no delete endpoint. Treat schema creation as permanent,
  get the field list right before creating.
- Location "marketing templates" (`/locations/{id}/templates`) are GET+DELETE only,
  no create/update via API. Building a new template goes through the email builder
  family (see `ghl-email-flows`), not this endpoint.
- Write ops need a deliberate `idempotencyKey` or they 400. Never a blind retry loop.

## Browser-only edges (route to `ghl-browser`)

- Pipeline/stage structure: creating, renaming, or reordering stages.
- Workflow builder: steps, triggers, the emails/SMS content inside a workflow step.
- Location "marketing template" create/update (GET+DELETE only via API).
- Anything needing a Private Integration scope this token doesn't carry. That's a
  Settings change, not a missing endpoint.

## Safety rails

Inherits `ghl-crm`'s rails in full: no contact deletes without explicit approval, no
bulk SMS/email blasts without approval (individual follow-ups are fine), never touch
pipeline structure via API, verify every write, tag on every action that changes a
contact's state. Domain-specific additions:
- Check for an existing opportunity (`search-opportunity`) before creating a new one
  for the same contact. Duplicate opportunities corrupt pipeline reporting.
- Hygiene sweeps report first, move stages second. Never bulk-move a whole stale
  cohort in one pass without a per-record verify.
- Custom object schema creation is a one-way door (no delete). Confirm the field list
  before running `create-custom-object-schema`.

Router key `sk-18ihx67` — resolved by the skills index on load.
