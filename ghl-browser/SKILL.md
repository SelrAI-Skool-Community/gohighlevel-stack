---
name: ghl-browser
description: Drives browser-only GoHighLevel work through agent-browser, including workflow, funnel, form, survey, pipeline-stage, and settings tasks. Use when a GHL task has no public API, a signed-in GHL page needs browser control, or a GHL page stalls during automation. Reuses a signed-in session, handles GHL page timing, preserves the user's normal Chrome windows, and routes API-capable work back to ghl-crm.
allowed-tools: Bash(agent-browser:*), Bash(ghl:*), Read, Edit, Write
---

# Browser & GHL Automation Skill⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Use this only when GoHighLevel has no public API for the task.

---

## Decision matrix

```
STEP 1: Check ../ghl-crm/references/capability-matrix.md.
STEP 2: If the task is API-capable, use one of three lanes:
  MCP: run claude mcp list and use the registered GoHighLevel server name.
  REST: call the documented endpoint with the token in repo-root secrets/ghl.env.
  CLI: use repo-root scripts/ghl, including scripts/ghl raw.
STEP 3: If the task is browser-only, reuse the signed-in session with agent-browser.
```

Use internal GHL endpoints only as a last resort because they can change without notice.

---

## Environment: Mac (agent-browser)

### Configuration
agent-browser is the browser CLI used by this skill. Run `agent-browser skills get core
--full` for its command reference.

### Persistent Profile
- agent-browser keeps its own persistent profile, cookies, localStorage, saved passwords, Google login, GHL session all persist across runs
- The user only needs to log in ONCE, sessions persist across daemon restarts
- agent-browser uses its own Chrome-for-Testing binary, it does NOT touch the user's real Chrome profile
- If the daemon won't start or loses connection, self-heal autonomously (see Chrome Safety Rules below), never ask a human

### Chrome Safety Rules (CRITICAL)

1. **NEVER close the user's real Chrome or kill its processes** (`killall`, `pkill`, `kill -9` on `Google Chrome.app`), the user has many tabs open. agent-browser runs its own Chrome-for-Testing, separate from real Chrome.
2. **NEVER close tabs** you didn't open in the user's real browser, the user's tabs are sacred
3. **If agent-browser loses connection or the daemon stalls**: self-heal autonomously, restart the daemon (`agent-browser stop` then re-`open`), and if the binary is missing or broken, reinstall it and continue. Never ask the user to restart anything.
4. **Let agent-browser pages stay open** when done, re-running `open` reuses the warm session.

### Core agent-browser Commands
```
agent-browser open <url>            # Navigate to URL and start the daemon if needed
agent-browser snapshot -i           # Get the interactive tree with @eN refs
agent-browser click @eN             # Click an element from the latest snapshot
agent-browser type @eN "text"       # Type into a field
agent-browser fill @eN "value"      # Fill a form field
agent-browser press <key>           # Press a keyboard key, such as Enter
agent-browser screenshot <path>     # Capture the visual layout
agent-browser eval "<js>"           # Run JavaScript in the page
agent-browser stop                  # Stop the daemon before a clean restart
```

**Preferred approach for reading page content:**
- `agent-browser snapshot -i`, returns structured accessibility tree with clickable @eN refs, fast, no image overhead
- `agent-browser eval "<js>"`, run JS to extract specific data (`document.querySelector(...)`)
- `agent-browser screenshot <path>`, only when you need to SEE the visual layout

---

## GHL Login Flow

### When Login Is Needed
GHL sessions expire. Start by reusing the signed-in agent-browser profile.

### Step-by-Step Login (Mac, agent-browser)

**Step 1: Navigate to GHL**
```
agent-browser open https://app.gohighlevel.com/
```

**Step 2: Check if already logged in**
Run `agent-browser snapshot -i`. If you see the dashboard/sidebar, you're logged in, skip to your task.

**Step 3: Recover the session**
If the login form appears, ask Claude to reopen the saved profile and retry. The bundle's
`secrets/ghl.env` contains API credentials only. Do not store login passwords there.

**Step 4: Handle 2FA (if triggered)**
See next section.

**Step 5: Location selection**
If prompted to select a location, choose "[YOUR BUSINESS NAME]" (`<YOUR_LOCATION_ID>`).

## GHL 2FA Handling (Fully Autonomous)

**HARD RULE: NEVER ask the user for the 2FA code. Retrieve it automatically.**

### Flow
1. GHL presents 2FA screen asking for security code
2. Click **"Send code to email"** (shows `your email`)
3. Click **"Send Security Code"** button
4. Wait 5-10 seconds for email delivery
5. If an email MCP server is installed, run `claude mcp list` and use its registered
   name to search for `from:noreply subject:security code newer_than:1d`.
6. Read the matching email and extract the 6-digit code.
7. Enter the code into the form (snapshot first to get the @eN refs):
   ```
   agent-browser fill @eN "<6-digit code>"   # security code input
   agent-browser click @eN                    # "Verify" or "Submit" button
   ```

### Troubleshooting 2FA
- If email doesn't arrive within 15 seconds, click "Resend code"
- Search the inbox connected to the registered email MCP server
- The code is typically in the email snippet, look for a 6-digit number
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
- Settings/social-media returns empty page, use `/marketing/social-planner` instead
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
5. After creating, read stage IDs through `scripts/ghl pipelines` or the corresponding
   operation on the registered GHL MCP server.

**To reorder/rename stages:**
1. Navigate to pipeline
2. Drag stages to reorder, or click stage name to edit
3. Save changes

### Workflow Management (UI-Heavy)
GHL workflows are visual drag-and-drop. Creating workflows via API is extremely limited.

Publish or disable workflows through the signed-in workflow builder. Verify the final
status after reloading the workflow list.

### Social Media Re-Auth (UI Only)
When social accounts expire (TikTok, YouTube, etc.):
1. Navigate to `/marketing/social-planner` → notification banner has "Re-integrate" button
2. OR: Social Planner → Settings tab → Social Accounts → filter by "Expired"
3. Click "Reconnect" → select the account in the dialog → click "Reconnect" again
4. Complete the OAuth flow in the browser
5. Persistent profile means the social platform login may already be saved

**Known limitation:**
- TikTok Business re-auth via "Continue with Google" fails, Google Workspace blocks automated browsers with `ERR_CONNECTION_CLOSED`. Google's OAuth uses `prompt=select_account` which forces fresh sign-in even with persistent profile.
- **Workaround**: If the account has direct login, use that instead of Google SSO.
- **Best fix**: Drive the OAuth flow with agent-browser in its persistent profile. If an
  email security code is required, use the registered email MCP server.

### Form & Survey Builder (UI Only)
- Navigate to Sites → Forms or Surveys
- These are drag-and-drop builders, not automatable via API
- For reading form submissions, use the API: `ghl form-submissions <formId>`

---

## Troubleshooting

### agent-browser Won't Launch (self-heal, never ask a human)
```bash
# Restart the daemon
agent-browser stop && agent-browser open https://app.gohighlevel.com/

# If the daemon is wedged, check for the process and clear it
ps aux | grep -i agent-browser | grep -v grep

# If the binary is missing or broken, reinstall it, then retry
# (agent-browser is the Vercel Labs Rust CLI, reinstall and continue, do not abort)
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
- Run `claude mcp list` and use the registered GoHighLevel server name.
- A 401 "not authorized for this scope" means the Private Integration Token lacks the
  required scope. Fix it in Settings, Private Integrations.
- MCP is optional. Retry through direct REST or repo-root `scripts/ghl`.

### Timeout on GHL Pages
GHL's SPA is heavy. Give it time, some GHL pages take 10-15 seconds to fully load.

**Typical loading pattern:**
1. `agent-browser open <url>` → page shows "Loading fresh data..." / "Initializing..."
2. Wait 10-15s, then re-run `agent-browser snapshot -i`
3. If the snapshot is still sparse, wait another 10s and snapshot again
4. Workflows page loads inside an **iframe** (`workflow-builder`), agent-browser surfaces iframe elements in the snapshot with their own @eN refs; click them like any other ref.
5. Social Planner loads inline (no iframe), normal refs.
6. GHL may show modals (e.g., "AI Builder Enabled"), dismiss with `agent-browser click @eN` on "Got it" or the close button.

---

## Safety Rules Summary

| Rule | Why |
|------|-----|
| Never close or kill the user's real Chrome | The user may have important tabs open; agent-browser runs its own Chrome-for-Testing |
| Never close tabs you didn't open | The user's tabs are sacred |
| Never ask the user for emailed 2FA codes | Use the registered email MCP server when available |
| Ask Claude to retry browser failures | Restart the daemon and reopen the saved session |
| API first, browser second | MCP, REST, and `scripts/ghl` are available before browser fallback |
| Always check if logged in before login flow | Don't re-login if session is active |

---

## Quick Reference Card

```
# agent-browser, authenticated and persistent
agent-browser open <url>      # navigate
agent-browser snapshot -i     # read page content + get @eN refs
agent-browser click @eN       # interact with elements
agent-browser fill @eN "..."  # fill inputs

# Repo-root GHL CLI helper, API without a browser
scripts/ghl search-contacts "query"
scripts/ghl pipelines
scripts/ghl send-sms <contactId> "message"
scripts/ghl raw GET "/endpoint"

# 2FA, fully autonomous
Run claude mcp list, then use the registered email server to find and read the code.

# GHL URLs (locationId = <YOUR_LOCATION_ID>)
Dashboard:  app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/dashboard
Contacts:   app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/contacts/smart_list/All
Pipelines:  app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/opportunities/list
Workflows:  app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/automation/workflows
Social:     app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/marketing/social-planner
Settings:   app.gohighlevel.com/v2/location/<YOUR_LOCATION_ID>/settings/company
```

Router key `sk-1djxbff` — resolved by the skills index on load.
