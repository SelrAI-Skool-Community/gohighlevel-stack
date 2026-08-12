# SETUP-PROMPT.md

Paste into Claude Code to install + verify the ghl-calendars-booking skill.

```
Install + verify the ghl-calendars-booking skill on this machine.

1. Confirm the skill exists at ~/.claude/skills/ghl-calendars-booking/ (symlink into the kit's GHL connector pack).
2. Confirm the master router is installed: ~/.claude/skills/ghl-crm/ — this skill is a domain
   playbook under it and inherits its ladder, quirks, and safety rails.
3. Confirm MCP servers: run `claude mcp list` and check ghl-official AND ghl-v2 are connected.
   Missing? Follow ghl-crm/SETUP-PROMPT.md step 2.
4. Dry test: load the ghl-calendars-booking skill and run calendars, booking, rooms, showroom consultations with a read-only call
   (any playbook step 1). Expect real data back, no 401.
5. Ready. Trigger phrases include "what slots are free tomorrow", "book a discovery call", "pull today's bookings".
```

## Notes

- Full operation list by business task: `references/operations.md` in this skill.
- Browser-only edges route to /ghl-browser; the capability matrix in ghl-crm references is the truth.
- No MCP client (cron/server)? Use `ghl-crm/scripts/ghl_v2_call.py` with the same operationIds.
