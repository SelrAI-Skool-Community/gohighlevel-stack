# Set up ghl-browser

Paste this into Claude Code:

```text
Set up and verify the ghl-browser skill.

1. Confirm ~/.claude/skills/ghl-browser/SKILL.md exists.
2. Confirm the agent-browser CLI is installed with `agent-browser --version`.
3. Reuse an existing signed-in GHL browser session. Do not place login credentials in secrets/ghl.env.
4. Run `bash ~/.claude/skills/ghl-browser/scripts/smoke.sh`.
5. Ask Claude to retry if the browser daemon stalls or the session needs reopening.
```

Use this skill only for work listed as browser-only in
`../ghl-crm/references/capability-matrix.md`. API-capable work uses the optional MCP lane,
direct REST, or repo-root `scripts/ghl`.
