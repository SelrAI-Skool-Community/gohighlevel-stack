# API and browser lanes

## Lane A: email templates

The builder API below was verified live against a real GHL location.

```text
POST /emails/builder
{locationId, name, type:"html"}
→ {id}

POST /emails/builder/data
{locationId, templateId, html, editorType:"html", previewText, updatedBy:"<who>"}
→ {ok, previewUrl}

GET /emails/builder?locationId=...
→ list/verify

DELETE /emails/builder/{loc}/{id}
→ remove old
```

`updatedBy` is required on the data call; omission returns 422. Open and inspect every returned `previewUrl`.

Give templates a predictable name so a later push can find and update them rather than
creating duplicates. A shape that works: `<chain>-<variant>-E<n>-v<N> - <subject stub>`,
for example `quote-followup-E1-v3 - Still thinking it over?`.

The v3 templates/campaigns API also supports full campaign sends:

- `/emails/locations/{id}/templates`
- campaign create/schedule endpoints
- required PIT scopes: `emails/templates.*` and `emails/campaigns.*`

Use the inherited `scripts/push_templates.py` helper for the builder lane. Its own help text documents dry runs, predictable prefixes, exact-name updates, deletion by prefix, credential resolution, and rate limiting.

## Lane B: workflow steps

The public workflow API lists workflow names only. The following work stays in the signed-in workflow builder:

- Attach a pushed template to an email step.
- Edit subjects inside steps.
- Edit SMS bodies.
- Change waits, Active/Disabled statuses, and other step configuration.

Use `ghl-browser` with agent-browser for automated login and 2FA, or prepare a Codex browser handover. The capability matrix in `ghl-crm` records the boundary.

After any live GHL change, re-sync the flows dashboard so review truth and delivery truth match.
