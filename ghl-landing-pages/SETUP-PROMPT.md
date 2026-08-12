# SETUP-PROMPT.md

Paste into Claude Code to install and verify the ghl-landing-pages skill.

```
Install + verify the ghl-landing-pages skill on this machine.

1. Confirm the skill exists at ~/.claude/skills/ghl-landing-pages/.
2. Confirm GHL is connected. Run `claude mcp list` and look for the GHL MCP server.
   If it is missing, run the ghl-connector skill first.
3. Run smoke: bash ~/.claude/skills/ghl-landing-pages/scripts/smoke.sh
4. Confirm the ghl-browser skill is installed (needed for the Custom Code element method).
5. Confirm the ghl-crm skill is installed (pairs for form wiring and contact capture).
6. Once verified, the skill is ready. Trigger phrases include "build a GHL landing page",
   "edit my GHL funnel", "publish a new page", "deploy a sales page",
   "add a form to my landing page".
```

## What this skill drives

| Operation | Path |
|---|---|
| Create a fully programmatic landing page (blog rawHTML) | `blogs_create-blog-post` |
| Update an existing blog-served page | `blogs_update-blog-post` |
| Drop full HTML into a real funnel page | ghl-browser via Custom Code element |
| Host externally, mount in GHL via iframe | Static host deploy + GHL Header Tracking Code |
| Map a path to an external URL | funnels-domain `create-redirect` (301) |
| Run the post-deploy page audit | bundled script in SKILL.md |
| Image resize before deploy | `sips -Z` (built into macOS) |

## Three install paths, when to use which

1. **Blog API rawHTML** — the primary path. Full create/read/update/delete through the
   API. Publishes to `yourdomain.com/blog/<slug>`. Use it for any page where that URL
   pattern is acceptable.
2. **Custom Code element via ghl-browser** — when the page must live inside a real GHL
   funnel: checkout pages, order forms, anything wired to GHL payments. Slow to set up,
   cheap to update afterwards.
3. **External host plus GHL iframe** — host the HTML on a static host and inject one
   `<iframe>` into the GHL Header Tracking Code. Edit and redeploy for instant updates.
   Best when one high-value page will be iterated on a lot.

## Failure modes

| Symptom | Fix |
|---|---|
| GHL blog tools not available | Tools not loaded. Search your tools for `ghl blogs` to load them, or run ghl-connector |
| 401 Unauthorized on blog API | Token expired or missing a scope. Re-mint the token, then check `secrets/ghl.env` |
| Blog post creates but the image is broken | A local asset path was used. Upload to the GHL media library or a CDN and reference the absolute URL |
| Funnel page shows the GHL wrapper around the Custom Code element | Header Code CSS override missing. Paste the `.hl_page-preview--content` rule from SKILL.md, Method 2 |
| Host deploy succeeds but GHL still shows the old page | The iframe is cached. Hard-refresh the GHL page once (Cmd+Shift+R) |
| Page audit reports em dashes | Fix the copy and redeploy |
| Image over 200KB | `sips -Z 1200 path/to/image.jpg --out path/to/image.jpg` |

## Pairs with

- `ghl-browser` — UI-only operations and the persistent browser profile the Custom Code
  element method needs
- `ghl-crm` — wire form submissions on the page to contacts, tags and pipelines
- `ghl-connector` — where the GHL API credentials come from
- `web-accessibility` — accessibility pass on the rendered page
- `ui-ux-pro-max` — design pass before deploy
