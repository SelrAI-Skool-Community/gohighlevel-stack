# Set up ghl-landing-pages

Paste this into Claude Code:

```text
Set up and verify the ghl-landing-pages skill.

1. Confirm ~/.claude/skills/ghl-landing-pages/SKILL.md, ghl-crm, and ghl-browser exist.
2. Load GHL_API_KEY and GHL_LOCATION_ID from secrets/ghl.env in the GoHighLevel stack repo root.
3. Run `claude mcp list`. If a GoHighLevel MCP server is listed, use its actual registered name. MCP is optional.
4. Without MCP, use direct REST or repo-root `scripts/ghl raw` for blog and redirect operations.
5. Run `bash ~/.claude/skills/ghl-landing-pages/scripts/smoke.sh`.
6. Run a read-only blog-list query. On failure, ask Claude to retry after checking the token scope and location ID.
```

## Page routes

| Page task | Route |
|---|---|
| Create or update a blog page with raw HTML | MCP, direct REST, or `scripts/ghl raw` |
| Add custom HTML to a funnel page | `ghl-browser` |
| Redirect a GHL path to an external page | MCP, direct REST, or `scripts/ghl raw` |

Blog publishing and redirects have REST fallbacks. Funnel page content is browser-only.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Blog MCP operations are missing | Run `claude mcp list`, use the registered GHL server name, or switch to REST or `scripts/ghl raw`, then ask Claude to retry |
| 401 Unauthorized | Check the token and blog scopes in repo-root `secrets/ghl.env`, then ask Claude to retry |
| A published image is broken | Upload it to GHL media or a CDN and use the absolute URL, then retry |
| GHL chrome surrounds the custom HTML | Add the wrapper-hiding CSS from `SKILL.md`, Method 2, then retry |
| The hosted page still shows an old iframe | Hard-refresh the GHL page, then ask Claude to verify it again |
| The page audit finds long dashes | Replace them in the page copy and redeploy |
| An image exceeds 200KB | Resize it before uploading, then rerun the page audit |
