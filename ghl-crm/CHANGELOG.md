# ghl-crm changelog

## [1.1.0] - 2026-05-25

Production-grade completion: cook to lift from Needs work (2.8) to Promising (~4.2). Same SKILL.md body content, just adds the missing evidence + setup layer.

### Added

- `scripts/smoke.sh`: 7-check smoke (SKILL.md frontmatter, GHL MCP registration via `claude mcp list`, bash helper presence, GHL credentials reachable, ghl-browser sister skill, examples/ + CHANGELOG.md present, SETUP-PROMPT.md present).
- `SETUP-PROMPT.md`: paste-into-Claude install + verify + failure-modes table.
- `examples/ghl-crm-session.md`: 6 worked transcripts (contact search, contact create + pipeline assign, email send showing the html-vs-message quirk, pipeline status check, bulk tag op, handoff to ghl-browser for UI-only ops).

### Changed

- `SKILL.md` frontmatter description rewritten. Was 8 words ("GoHighLevel CRM management. Contacts, pipelines, calendars, messaging, workflows."). Now 75 words with concrete trigger phrases ("search GHL contacts", "create a GHL contact", "update opportunity", "send GHL SMS", "send GHL email", "find contact in GHL", "GHL pipeline status", "schedule a GHL appointment", "GHL workflow"). Names both MCP servers (ghl-official + ghl-community) and pairs-with sister skill (/ghl-browser).

### Why

kit-doctor flagged trigger_fidelity=2 and evidence=1. Both are mechanical fixes — the SKILL.md body has 279 lines of high-quality API reference, just no machine-checkable evidence layer.

### Validation

- `bash scripts/smoke.sh` runs without crash, produces PASS/WARN/FAIL per check.
- `python3 ~/.claude/skills/kit-doctor/scripts/audit.py ~/.claude/skills/ghl-crm --pretty` returns Promising avg 4.2 (was Needs work 2.8). Production once the kit-index supplies the differentiation cross-check.

### Not touched

- 279-line SKILL.md body (API quirks, MCP server tables, payment notes, social auth notes, browser fallback ref) unchanged.
- ghl-browser sister skill unchanged.
- GHL credentials unchanged.

## [1.0.0] - prior

Initial release. Two-MCP strategy (ghl-official + ghl-community) with bash helper fallback. Documented every common API quirk encountered in real-world GHL operations.
