# ghl-browser changelog

## [1.1.0] - 2026-05-23

Production-grade completion: smoke test + SETUP-PROMPT.

### Added

- `scripts/smoke.sh`: 6-check smoke confirming agent-browser CLI, GHL credentials, Gmail MCP, persistent profile, GHL location ID, and SKILL.md presence.
- `SETUP-PROMPT.md`: paste-into-Claude install + verify prompt.

### Validation

- `bash scripts/smoke.sh` passes 5/5 hard checks (1 warn for GHL_LOCATION_ID placeholder, fixable per-attendee).

### Not touched

- The 719-line SKILL.md body (the canonical reference for ALL browser automation with GHL + other SaaS) unchanged.
- The Decision Matrix, Priority Chain, Login Flow, 2FA Handling, URL catalogue, all preserved.

## [1.0.0] - prior

Initial release: full GHL browser ops reference, agent-browser migration noted at top.
