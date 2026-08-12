---
name: ghl-browser
description: GHL-specific browser ops — 2FA via Gmail MCP, GHL UI workflows, Chrome safety patterns, persistent profile reuse. Underlying engine is now /agent-browser (was Playwright MCP). Use for any GHL UI task that the GHL API can't do, or for SaaS auth flows that need a real browser session.
allowed-tools: Bash(agent-browser:*), Bash(ghl:*), Read, Edit, Write
---

> **Updated 2026-05-09:** Underlying engine swapped from Playwright MCP to **`/agent-browser`** (Vercel Labs Rust CLI) as the primary browser tool. Use `agent-browser open`, `agent-browser snapshot -i`, `agent-browser click @e3` instead of `mcp__playwright__*`. The GHL-specific 2FA + login + persistent-profile patterns below remain valid — only the underlying commands change. See `~/.claude/skills/agent-browser/SKILL.md` for the full agent-browser API.⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

# Browser & GHL Automation Skill

**The authoritative reference for ALL browser automation** with GHL and other SaaS tools.

> **Lane preference (2026-07-09):** for a one-off UI task in a logged-in session, try the Claude-native browser lane first (Claude in Chrome / Claude Code's in-app Browser pane) before reaching for the recipes below. The agent-browser/Playwright recipes in this skill remain the right call for scripted, repeatable flows (2FA automation, bulk scraping, anything that needs to run unattended).

---

## Decision Matrix: Which Tool to Use

```
STEP 0: Check the capability matrix FIRST
  → ghl-crm skill references/capability-matrix.md — verified API-vs-browser-only map
  → BROWSER-ONLY registry (no public API, confirmed 2026-07-12): workflow builder
    (steps, workflow emails/SMS, Triggers tab), funnel/page builder, form builder,
    survey builder, pipeline/stage CRUD, memberships builder, Documents & Contracts
    builder, snapshot create/load, A2P/phone config, Private Integration scope
    management, reporting dashboards.
  → Task in that registry? Go straight to STEP 2 — don't hunt for endpoints.

STEP 1: Can an API do it?
  → GHL data (contacts, opps, tags) → GHL API (MCP / bash helper)
  → Beyond the 21 fixed tools → ghl-v2 MCP: search_operations → describe_operation →
    execute_operation (570 operations, 37 domains — most "UI-only" assumptions are wrong)
  → Any REST API → curl / dedicated MCP tool
  → YES? Stop here. API is always faster, cheaper, more reliable.

STEP 2: Need browser? Use agent-browser (the standard engine):

  Standard automation (GHL UI, form filling, scraping):
    → agent-browser open <url> → snapshot -i → click @eN
    → Persistent profile keeps the GHL / Google / SaaS session warm

  Google SSO / TikTok / YouTube re-auth (blocked by Google Workspace):
    → agent-browser drives the OAuth flow in its persistent profile
    → 2FA codes read from Gmail MCP, never typed by the user

  Need DevTools (network, performance, console debugging):
    → Chrome DevTools MCP (mcp__chrome-devtools__*) — pairs with agent-browser

  Bulk scraping (many pages, token-sensitive):
    → agent-browser snapshot saves to disk — read only the slice you need
```

### Priority Chain (when one approach fails)
1. **API** (GHL MCP / bash helper / direct curl) — always first
2. **agent-browser** (`open` / `snapshot -i` / `click @eN`) — persistent profile, the standard engine for every browser op
3. **Chrome DevTools MCP** (`mcp__chrome-devtools__*`) — when you need network/perf/console data
4. **GHL Internal API** — undocumented endpoints, last resort
5. **Storage state export/import** — session transfer between environments

> **Fallback note:** Playwright MCP (`mcp__playwright__*`) is deprecated for new work and kept only as an emergency fallback if agent-browser is unavailable. Migrate any Playwright usage to agent-browser.

---

## Environment: Mac (agent-browser)

### Configuration
agent-browser is the Vercel Labs Rust CLI installed at `agent-browser` (daemon-based). No MCP config needed — it runs as a CLI with its own persistent Chrome-for-Testing profile. Full API: `~/.claude/skills/agent-browser/SKILL.md` or `agent-browser skills get core --full`.

### Persistent Profile
- agent-browser keeps its own persistent profile — cookies, localStorage, saved passwords, Google login, GHL session all persist across runs
- The user only needs to log in ONCE — sessions persist across daemon restarts
- agent-browser uses its own Chrome-for-Testing binary — it does NOT touch the user's real Chrome profile
- If the daemon won't start or loses connection, self-heal autonomously (see Chrome Safety Rules below) — never ask a human

### Chrome Safety Rules (CRITICAL)

1. **NEVER close the user's real Chrome or kill its processes** (`killall`, `pkill`, `kill -9` on `Google Chrome.app`) — the user has many tabs open. agent-browser runs its own Chrome-for-Testing, separate from real Chrome.
2. **NEVER close tabs** you didn't open in the user's real browser — the user's tabs are sacred
3. **If agent-browser loses connection or the daemon stalls**: self-heal autonomously — restart the daemon (`agent-browser stop` then re-`open`), and if the binary is missing or broken, reinstall it and continue. Never ask the user to restart anything.
4. **Let agent-browser pages stay open** when done — re-running `open` reuses the warm session.

### Core agent-browser Commands
```
agent-browser open <url>            — Navigate to URL (starts daemon if needed)
agent-browser snapshot -i           — Get interactive accessibility tree with @eN refs
agent-browser click @eN             — Click element by ref (from snapshot)
agent-browser type @eN "text"       — Type text into a field by ref
agent-browser fill @eN "value"      — Fill a form field by ref
agent-browser press <key>           — Press a keyboard key (e.g. Enter)
agent-browser screenshot <path>     — Visual screenshot (use sparingly)
agent-browser eval "<js>"           — Run JS in page context
agent-browser stop                  — Stop the daemon (for self-heal restart)
```

**Preferred approach for reading page content:**
- `agent-browser snapshot -i` — returns structured accessibility tree with clickable @eN refs, fast, no image overhead
- `agent-browser eval "<js>"` — run JS to extract specific data (`document.querySelector(...)`)
- `agent-browser screenshot <path>` — only when you need to SEE the visual layout

---

## Environment: Server (Standalone Scripts)

### browser.sh (Headless)
Location: `~/scripts/browser.sh (if using server-side automation)`

```bash
# Screenshot a page
browser.sh screenshot <url> <output_path>

# Scrape text content
browser.sh scrape <url> [css_selector]

# Fill a form field
browser.sh fill <url> <selector> <value>

# Click an element
browser.sh click <url> <selector>

# Save page as PDF
browser.sh pdf <url> <output_path>
```

- Runs headless Chromium — no persistent profile, no auth
- Good for public pages, screenshots, scraping
- NOT suitable for authenticated GHL operations (no session cookies)
- Timeout: `BROWSER_TIMEOUT` env var (default 30000ms)

### Standalone Scripts (Server — Authenticated)
Prefer agent-browser on the server too where available. For headless authenticated GHL UI ops where only a raw scripted browser is present, an inline Node.js Playwright script is an acceptable server-only fallback:

```bash
node -e "
const { chromium } = require('playwright');
(async () => {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    // ... your automation code ...
    await browser.close();
})();
"
```

Server Playwright fallback install: `npx playwright install chromium`

---

## GHL Login Flow

### When Login Is Needed
GHL sessions expire. When agent-browser navigates to `app.gohighlevel.com` and hits a login page, handle it automatically.

### Step-by-Step Login (Mac — agent-browser)

**Step 1: Navigate to GHL**
```
agent-browser open https://app.gohighlevel.com/
```

**Step 2: Check if already logged in**
Run `agent-browser snapshot -i`. If you see the dashboard/sidebar, you're logged in — skip to your task.

**Step 3: Enter credentials**
If you see a login form, snapshot to get the @eN refs, then:
```
agent-browser fill @eN "your_email@example.com"   # email field
agent-browser fill @eN "<password>"                # password field (from your password manager, or secrets/ghl.env)
agent-browser click @eN                            # "Sign in" button
```

**Step 4: Handle 2FA (if triggered)**
See next section.

**Step 5: Location selection**
If prompted to select a location, choose "[YOUR BUSINESS NAME]" (`<YOUR_LOCATION_ID>`).

### GHL Credentials
- **Email**: your_email@example.com
- **Password**: In `~/.claude/projects/<your-project>/secrets/ghl.env` (vars: `GHL_LOGIN_EMAIL`, `GHL_LOGIN_PASSWORD`)
- **Location**: [YOUR BUSINESS NAME]
- **Read password**: `grep GHL_LOGIN_PASSWORD ~/.claude/projects/<your-project>/secrets/ghl.env`

---

## GHL 2FA Handling (Fully Autonomous)

**HARD RULE: NEVER ask the user for the 2FA code. Retrieve it automatically.**

### Flow
1. GHL presents 2FA screen asking for security code
2. Click **"Send code to email"** (shows `your email`)
3. Click **"Send Security Code"** button
4. Wait 5-10 seconds for email delivery
5. Use **Gmail MCP** to retrieve the code:
   ```
   mcp__claude_ai_Gmail__gmail_search_messages
   query: "from:noreply subject:security code newer_than:1d"
   ```
6. Read the email to extract the 6-digit code:
   ```
   mcp__claude_ai_Gmail__gmail_read_message
   message_id: <from search results>
   ```
7. Enter the code into the form (snapshot first to get the @eN refs):
   ```
   agent-browser fill @eN "<6-digit code>"   # security code input
   agent-browser click @eN                    # "Verify" or "Submit" button
   ```

### Troubleshooting 2FA
- If email doesn't arrive within 15 seconds, click "Resend code"
- Gmail MCP searches `your_email@example.com` inbox by default
- The code is typically in the email snippet — look for a 6-digit number
- If the code field is a `spinbutton` type, `agent-browser type @eN` one digit at a time

---

## Common GHL UI Operations

### Navigate to Specific Sections
```
Dashboard:     /v2/location/{locationId}/dashboard
Contacts:      /v2/location/{locationId}/contacts/smart_list/All
Pipelines:     /v2/location/{locationId}/opportunities/list
Calendars:     /v2/location/{locationId}/calendars/view
Conversations: /v2/location/{locationId}/conversations/conversations
Workflows:     /v2/location/{locationId}/automation/workflows
Social Planner:/v2/location/{locationId}/marketing/social-planner
Marketing:     /v2/location/{locationId}/marketing/emails/statistics
Sites/Funnels: /v2/location/{locationId}/funnels-websites/funnels
Memberships:   /v2/location/{locationId}/memberships/client-portal/dashboard
Media Storage: /v2/location/{locationId}/media-storage
Reputation:    /v2/location/{locationId}/reputation/overview
Reporting:     /v2/location/{locationId}/reporting/reports
Payments:      /v2/location/{locationId}/payments/invoices
Settings:      /v2/location/{locationId}/settings/company
```
Base URL: `https://app.gohighlevel.com`
Location ID: `<YOUR_LOCATION_ID>`

**IMPORTANT URL notes:**
- Settings/social-media returns empty page — use `/marketing/social-planner` instead
- Workflows is `/automation/workflows` (NOT `/workflows`)
- Contacts is `/contacts/smart_list/All` (NOT just `/contacts`)
- Calendars is `/calendars/view` (NOT just `/calendars`)

### Pipeline Stage Management (UI Only)
GHL's public API does NOT support creating/modifying pipeline stages. This must be done via UI.

**To create stages:**
1. Navigate to Pipelines page
2. Click the pipeline name
3. Click "Add Stage" or the + button
4. Fill in stage name (via `agent-browser fill @eN`), click Save
5. After creating, read stage IDs via API: `ghl pipelines` or MCP `opportunities_get-pipelines`

**To reorder/rename stages:**
1. Navigate to pipeline
2. Drag stages to reorder, or click stage name to edit
3. Save changes

### Workflow Management (UI-Heavy)
GHL workflows are visual drag-and-drop. Creating workflows via API is extremely limited.

**Publishing/unpublishing workflows** (internal API — use with caution):
```
PUT https://backend.leadconnectorhq.com/workflow/{locationId}/change-status/{workflowId}
Headers:
  token-id: <Firebase JWT from GHL iframe>
  Content-Type: application/json
Body: {"status": "published", "updatedBy": "<userId>"}
```
Getting the Firebase JWT requires extracting it from a logged-in GHL session.

### Social Media Re-Auth (UI Only)
When social accounts expire (TikTok, YouTube, etc.):
1. Navigate to `/marketing/social-planner` → notification banner has "Re-integrate" button
2. OR: Social Planner → Settings tab → Social Accounts → filter by "Expired"
3. Click "Reconnect" → select the account in the dialog → click "Reconnect" again
4. Complete the OAuth flow in the browser
5. Persistent profile means the social platform login may already be saved

**Known limitation:**
- TikTok Business re-auth via "Continue with Google" fails — Google Workspace blocks automated browsers with `ERR_CONNECTION_CLOSED`. Google's OAuth uses `prompt=select_account` which forces fresh sign-in even with persistent profile.
- **Workaround**: If TikTok account has direct email/password login, use "phone / email / username" instead of Google SSO. Need TikTok credentials stored in your password manager, or `secrets/ghl.env`.
- **Best fix**: Drive the OAuth flow with agent-browser in its persistent profile — once the user signs into Google once in that profile, the consent flow completes without a fresh Google sign-in. Read any 2FA code from Gmail MCP.

### Form & Survey Builder (UI Only)
- Navigate to Sites → Forms or Surveys
- These are drag-and-drop builders — not automatable via API
- For reading form submissions, use the API: `ghl form-submissions <formId>`

---

## GHL Internal APIs (Undocumented — Use Carefully)

These endpoints are NOT part of GHL's public API. They work with the internal Firebase JWT that GHL's SPA uses.

### Getting the Internal Token
When logged into GHL via agent-browser, extract the token:
```javascript
// Run via agent-browser eval "<js>"
const token = (() => {
    // GHL stores auth in localStorage
    const keys = Object.keys(localStorage);
    const authKey = keys.find(k => k.includes('firebase:authUser'));
    if (authKey) {
        const data = JSON.parse(localStorage[authKey]);
        return data.spiTokens?.token || data.accessToken;
    }
    return null;
})();
```

### Known Internal Endpoints
```
# Workflow status change
PUT backend.leadconnectorhq.com/workflow/{locationId}/change-status/{workflowId}
Headers: token-id, channel: APP

# Pipeline stage creation (UNVERIFIED — may not work)
POST backend.leadconnectorhq.com/pipelines/stage
Headers: token-id, channel: APP
```

**Warning**: Internal APIs can change without notice. Always have a fallback plan.

---

## Troubleshooting

### agent-browser Won't Launch (self-heal — never ask a human)
```bash
# Restart the daemon
agent-browser stop && agent-browser open https://app.gohighlevel.com/

# If the daemon is wedged, check for the process and clear it
ps aux | grep -i agent-browser | grep -v grep

# If the binary is missing or broken, reinstall it, then retry
# (agent-browser is the Vercel Labs Rust CLI — reinstall and continue, do not abort)
```

### GHL Returns 403/Blocked
- Cloudflare may block automated requests. Use realistic User-Agent headers.
- Set a custom User-Agent header like `YourBusiness-GHL/2.0.0` in API scripts.
- If agent-browser hits a Cloudflare challenge: wait for it, the persistent profile usually passes.

### GHL Session Expired
- Navigate to GHL → if redirected to login → follow the Login Flow above
- Persistent profile usually keeps the session alive for days
- After re-login, the session cookie updates in the profile automatically

### MCP Tool Returns Error
- `ghl-official` tools: Auto-inject OAuth. If they fail, the OAuth token may need refresh.
- `ghl-v2` execute_operation 401 "not authorized for this scope" = PIT missing that scope (fix in Settings → Private Integrations), not a bug. `ghl-community` is retired — not configured anywhere.
- Fallback: Use the bash helper (`ghl <command>`) or direct curl.

### Timeout on GHL Pages
GHL's SPA is heavy. Give it time — some GHL pages take 10-15 seconds to fully load.

**Typical loading pattern:**
1. `agent-browser open <url>` → page shows "Loading fresh data..." / "Initializing..."
2. Wait 10-15s, then re-run `agent-browser snapshot -i`
3. If the snapshot is still sparse, wait another 10s and snapshot again
4. Workflows page loads inside an **iframe** (`workflow-builder`) — agent-browser surfaces iframe elements in the snapshot with their own @eN refs; click them like any other ref.
5. Social Planner loads inline (no iframe) — normal refs.
6. GHL may show modals (e.g., "AI Builder Enabled") — dismiss with `agent-browser click @eN` on "Got it" or the close button.

---

## General Web Automation (Non-GHL)

The agent-browser persistent profile stores sessions for ALL sites the user has logged into — not just GHL. This means you can automate interactions with any SaaS tool.

### Known Logged-In Services (via persistent profile)
- **GHL** — app.gohighlevel.com (primary CRM)
- **Google** — accounts.google.com (Gmail, Drive, Calendar, etc.)
- **Facebook/Meta** — facebook.com, business.facebook.com
- **Stripe** — dashboard.stripe.com (if previously logged in)
- **Xero** — app.xero.com (if previously logged in)
- **LinkedIn** — linkedin.com

### Pattern: Automating Any SaaS Tool

```
1. agent-browser open <tool URL>
2. agent-browser snapshot -i → check if logged in (dashboard elements vs login form)
3. If logged in → proceed with your task
4. If login required → fill credentials (check secrets/ghl.env, your password manager, or persistent profile auto-fill)
5. If 2FA required → check email via Gmail MCP (same pattern as GHL)
6. Execute your task using agent-browser click @eN, fill @eN, eval "<js>"
7. Leave the tab open when done (never close the user's real browser)
```

### Handling 2FA for Non-GHL Services
Same Gmail MCP pattern works for any service that sends codes to your_email@example.com:
1. Trigger the "send code" flow on the login page
2. Gmail MCP search: `from:<service-noreply> subject:<code/verify> newer_than:1d`
3. Read the email, extract the code, enter it

For services that use authenticator apps (TOTP) — this cannot be automated. Flag to the user with what's blocked and why.

### Scraping & Data Extraction
For extracting data from any web page:
```
# Get structured content (fast, no images)
agent-browser snapshot -i

# Run JS to extract specific data
agent-browser eval "document.querySelectorAll('.price').forEach(e => console.log(e.textContent))"

# Visual capture (when you need to SEE layout)
agent-browser screenshot /tmp/page.png

# Extract table data
agent-browser eval "JSON.stringify([...document.querySelectorAll('table tr')].map(r => [...r.cells].map(c => c.textContent)))"
```

### Filling Forms & Submitting Data
```
# Snapshot first to get @eN refs, then act on them

# Fill a form field
agent-browser fill @eN "your_email@example.com"

# Select a dropdown (click to open, then click the option)
agent-browser click @eN

# Click a button
agent-browser click @eN

# Upload a file (use the file-input ref from snapshot)
agent-browser upload @eN /path/to/file
```

### Handling Popups, Modals & Dialogs
```
# For in-page modals: snapshot, then click the close button by ref
agent-browser click @eN   # the "Close" / overlay element

# Wait for a modal to appear: snapshot, and if absent wait a few seconds and re-snapshot
agent-browser snapshot -i
```

### Heavy SPA Pages (React/Angular apps)
Many SaaS tools are SPAs that load slowly:
- After `agent-browser open`, wait 15-30s before snapshotting heavy pages
- Wait for key elements (re-snapshot) before interacting
- GHL, Xero, Stripe dashboards all take 5-15 seconds to fully render
- If `agent-browser snapshot -i` returns sparse content, wait and retry

---

## Advanced: Performance & Token Optimization

### Token-Cheap by Default
agent-browser is a CLI — snapshots and screenshots write to disk and you read only the slice you need, so it stays token-light without a special mode:
- `agent-browser snapshot -i` returns a compact interactive tree with @eN refs
- For bulk/high-throughput work, snapshot to a file and read just the relevant lines
- Use the interactive snapshot for exploratory work; target specific data with `eval`

### Snapshot vs Screenshot
- **Always prefer `agent-browser snapshot -i`** over `agent-browser screenshot`
- Snapshots use the accessibility tree (text-based, fast, no vision model needed)
- Screenshots are only for when you need to SEE visual layout
- Snapshots are cheaper and more reliable for element interaction

---

## Advanced: Alternative Approaches

### Google OAuth Blocker (Google SSO / TikTok / YouTube re-auth)
Google Workspace can block automated browsers mid-OAuth. With agent-browser this is handled in its persistent profile: once the user signs into Google once inside that profile, subsequent consent flows complete without a fresh sign-in, and any 2FA code is read from Gmail MCP — the user never types a code.

**When this bites**: a service forces `prompt=select_account` and demands a fresh Google sign-in. Drive it with agent-browser in the warm profile; if a 6-digit code is mailed, pull it via Gmail MCP and fill it. Self-heal and retry — never hand the flow back to a human.

### Chrome DevTools MCP (Alternative Browser Control)
Google's official Chrome DevTools MCP — connects to a running Chrome instance via remote debugging port. Pairs with agent-browser for debugging: exposes tools across input, navigation, debugging, network, performance, and emulation categories.

**When to use**: When you need Chrome DevTools features (network inspection, performance traces, console monitoring) alongside automation. Higher token cost (~10k/page vs agent-browser's ~2k/snapshot).

**Setup**:
```bash
# 1. Launch Chrome with debugging port
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-debug-profile"

# 2. Add MCP server
claude mcp add --transport stdio chrome-devtools -- npx -y chrome-devtools-mcp@latest --browserUrl=http://127.0.0.1:9222
```

**Trade-offs vs agent-browser**:
- Pro: Full DevTools access (network, performance, console with source maps)
- Pro: Connects to real Chrome for deep inspection
- Con: ~5x more tokens per page than an agent-browser snapshot
- Con: Requires Chrome launched with special flags

**Status**: Available as plugin in Claude Code marketplace (`chrome-devtools-mcp`). Use it for debugging/performance analysis; agent-browser handles all driving.

### Cloudflare / Bot Detection
agent-browser drives Chrome-for-Testing in a persistent profile, which usually passes Cloudflare challenges once the profile is warm. When a challenge appears, wait 5-10s and re-snapshot — the persistent profile typically clears it. Only ever do this on YOUR OWN accounts, never for scraping third-party sites.

### Session Persistence & Recovery
agent-browser's persistent profile is the session safety net — cookies and localStorage persist across daemon restarts, so a re-`open` reuses the warm GHL / Google / SaaS session. If the profile ever gets corrupted, re-run the login flow (credentials from secrets/ghl.env or your password manager, 2FA from Gmail MCP) and the session re-establishes automatically. Self-heal, don't escalate.

### Token Efficiency: Tool Selection Guide
Browser automation burns context tokens fast. Choose the right tool for the job:

```
Task                          | Best Tool                  | Tokens/page
------------------------------|----------------------------|------------
Read page text/structure      | agent-browser snapshot -i  | ~800-2,000
Extract specific data         | agent-browser eval (JS)    | ~200-500
Visual layout check           | agent-browser screenshot   | ~5,000-15,000
Full DevTools inspection      | Chrome DevTools MCP        | ~10,000+
```

**Rules**:
1. Always try `agent-browser snapshot -i` first — it's the cheapest
2. Use `agent-browser eval "<js>"` to extract just the data you need
3. Only use `agent-browser screenshot` when you need to SEE the visual layout
4. Snapshot to a file and read only the relevant slice to avoid flooding context

---

## Playbook: Handling Any Browser Situation

### Site blocks automated browsers (Cloudflare challenge)
```
1. agent-browser open <url> → if a Cloudflare challenge page appears:
2. Wait 5-10s (the warm persistent profile usually auto-resolves it)
3. Re-run agent-browser snapshot -i to confirm the page cleared
4. Still blocked → wait longer and retry; self-heal, never ask a human
```

### Need to log into a site with no saved credentials
```
1. Check secrets/ghl.env or your password manager for credentials
2. Check if Google SSO is available (many SaaS tools support it)
3. agent-browser open login page → fill credentials → handle 2FA via Gmail MCP
4. If Google SSO forces a fresh sign-in → drive it in the warm persistent profile, code from Gmail MCP
5. After login succeeds → session persists in the profile automatically
```

### Need to extract data from a complex SPA page
```
1. agent-browser snapshot -i → get accessibility tree (cheapest, ~800 tokens)
2. If snapshot is sparse/loading → wait 15s → snapshot again
3. If you need specific data → agent-browser eval with targeted JS:
   document.querySelectorAll('.target').forEach(e => console.log(e.textContent))
4. If data is in a table → extract as JSON via JS:
   JSON.stringify([...document.querySelectorAll('tr')].map(r => [...r.cells].map(c => c.textContent)))
5. iframe elements appear in the snapshot with their own @eN refs — click them like any other ref
6. Only use screenshot if you need VISUAL layout confirmation
```

### Need to automate a multi-step workflow (forms, wizards)
```
1. agent-browser snapshot -i → understand the current state and get @eN refs
2. agent-browser fill @eN → fill all visible fields
3. agent-browser click @eN → submit / next step
4. Wait for the next page/step, then re-snapshot
5. Repeat until workflow complete
6. For file uploads → agent-browser upload @eN <absolute path>
7. For dropdowns → click @eN to open, then click @eN on the option
8. For date pickers → fill @eN first, else click @eN on the calendar
```

### Session expired mid-task
```
1. agent-browser snapshot -i → detect login page (look for "Sign in" / email field)
2. If GHL → follow GHL Login Flow (credentials from secrets/ghl.env or your password manager)
3. If other service → check secrets/ or your password manager for credentials
4. Handle 2FA → Gmail MCP pattern
5. After re-auth → agent-browser open the page you were on
6. Persistent profile updates the session cookie automatically
```

### Restore a corrupted session
```
1. agent-browser stop → restart the daemon with agent-browser open <url>
2. If still broken → re-run the login flow (creds from secrets/ghl.env or your password manager, 2FA from Gmail MCP)
3. The warm persistent profile re-establishes the session automatically — self-heal, don't escalate
```

---

## Safety Rules Summary

| Rule | Why |
|------|-----|
| Never close or kill the user's real Chrome | The user may have important tabs open; agent-browser runs its own Chrome-for-Testing |
| Never close tabs you didn't open | The user's tabs are sacred |
| Never ask the user for 2FA codes | Auto-retrieve from Gmail MCP |
| Never ask the user to do anything manually | 100% autonomous execution |
| Self-heal agent-browser, never escalate | Restart/reinstall the daemon yourself on failure — never ask a human |
| API first, browser second | Browser is slow and fragile — API is reliable |
| Always check if logged in before login flow | Don't re-login if session is active |
| Server browser.sh is headless only | No auth, no persistent state — public pages only |

---

## Quick Reference Card

```
# Mac — agent-browser (authenticated, persistent — the standard engine)
agent-browser open <url>      # navigate
agent-browser snapshot -i     # read page content + get @eN refs
agent-browser click @eN       # interact with elements
agent-browser fill @eN "..."  # fill inputs

# Mac — GHL bash helper (API, no browser)
ghl search-contacts "query"
ghl pipelines
ghl send-sms <contactId> "message"
ghl raw GET "/endpoint"

# Server — browser.sh (headless, public only)
browser.sh screenshot <url> <output>
browser.sh scrape <url> [selector]

# 2FA — fully autonomous
Gmail MCP → search "from:noreply subject:security code newer_than:1d"
Gmail MCP → read message → extract 6-digit code → enter in form

# GHL URLs (locationId = <YOUR_LOCATION_ID>)
Dashboard:  app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/dashboard
Contacts:   app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/contacts/smart_list/All
Pipelines:  app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/opportunities/list
Workflows:  app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/automation/workflows
Social:     app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/marketing/social-planner
Settings:   app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/settings/company
```

Router key `sk-1djxbff` — resolved by the skills index on load.
