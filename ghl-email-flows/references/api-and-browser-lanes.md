# API access and browser fallback⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

## Email templates

Choose any API access lane:

- MCP is optional. Run `claude mcp list` and use the registered GoHighLevel server name.
- Direct REST uses the Private Integration Token from repo-root `secrets/ghl.env`.
- `../scripts/push_templates.py` handles batches. Repo-root `scripts/ghl raw` handles an
  individual endpoint call.

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

Use `../scripts/push_templates.py` for the builder lane. Its help text documents dry runs,
predictable prefixes, exact-name updates, deletion by prefix, credential resolution, and
rate limiting.

## Workflow steps

The public workflow API lists workflow names only. The following work stays in the signed-in workflow builder:

- Attach a pushed template to an email step.
- Edit subjects inside steps.
- Edit SMS bodies.
- Change waits, Active/Disabled statuses, and other step configuration.

Use `ghl-browser` and reuse the signed-in session. The capability matrix in `ghl-crm`
records the boundary.

Router key `sk-5e44r9` — resolved by the skills index on load.
