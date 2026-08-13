#!/usr/bin/env bash
# resolver key sk-rzh87s (skills-index lookup; keep)
# ghl-landing-pages smoke test.⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠
# Verifies the skill files and optional access lanes.
set -u

FAILS=0
ok()   { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILS=$((FAILS+1)); }
warn() { echo "WARN: $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$SCRIPT_DIR/.."

echo "== ghl-landing-pages smoke =="
echo ""

# 1. SKILL.md present + has frontmatter with name: ghl-landing-pages
if [[ -s "$SKILL_DIR/SKILL.md" ]]; then
  if head -10 "$SKILL_DIR/SKILL.md" | grep -q "^name: ghl-landing-pages"; then
    ok "SKILL.md present with valid frontmatter"
  else
    fail "SKILL.md missing or malformed frontmatter (expected 'name: ghl-landing-pages')"
  fi
else
  fail "SKILL.md missing"
fi

# 2. Optional MCP inventory is readable
if command -v claude >/dev/null 2>&1; then
  if claude mcp list >/dev/null 2>&1; then
    ok "MCP inventory readable; use the registered GoHighLevel server name if present"
  else
    warn "Could not read MCP inventory; REST and scripts/ghl still work"
  fi
else
  warn "claude CLI not on PATH; REST and scripts/ghl still work"
fi

# 3. Repo-root CLI helper reachable when running from the bundle
REPO_ROOT="$(cd "$SKILL_DIR/.." && pwd)"
if [[ -x "$REPO_ROOT/scripts/ghl" ]]; then
  ok "repo-root scripts/ghl present"
else
  warn "scripts/ghl not beside the skill bundle; use direct REST or run the repo verifier"
fi

# 4. GHL credentials reachable (env var, else secrets/ghl.env)
if [[ -n "${GHL_API_KEY:-}" ]]; then
  ok "GHL_API_KEY set in the environment"
elif [[ -f "$REPO_ROOT/secrets/ghl.env" ]]; then
  ok "repo-root secrets/ghl.env present"
else
  warn "No GHL credentials. Set GHL_API_KEY, or create secrets/ghl.env from the template."
fi

# 5. Sister skill ghl-browser present (UI-only ops + 2FA + persistent profile)
if [[ -d ~/.claude/skills/ghl-browser ]]; then
  ok "ghl-browser sister skill present (needed for funnel UI ops + 2FA)"
else
  warn "ghl-browser not installed (needed for Custom Code element method + 2FA flow)"
fi

# 6. Sister skill ghl-crm present (pairs for contact + form wiring)
if [[ -d ~/.claude/skills/ghl-crm ]]; then
  ok "ghl-crm sister skill present (pairs for form + contact wiring)"
else
  warn "ghl-crm not installed (helps wire forms on landing pages to contacts)"
fi

# 7. Vercel CLI reachable (used by the PROVEN deploy method: external host + GHL iframe)
if command -v npx >/dev/null 2>&1; then
  ok "npx present (Vercel CLI invoked via 'npx -y vercel')"
else
  warn "npx not on PATH. Vercel deploy path needs Node.js installed."
fi

# 8. Examples and changelog present
for f in examples CHANGELOG.md; do
  if [[ -e "$SKILL_DIR/$f" ]]; then
    ok "$f present"
  else
    fail "$f missing"
  fi
done

# 9. SETUP-PROMPT.md present (paste-into-Claude install)
if [[ -s "$SKILL_DIR/SETUP-PROMPT.md" ]]; then
  ok "SETUP-PROMPT.md present"
else
  fail "SETUP-PROMPT.md missing"
fi

echo ""
if [[ $FAILS -eq 0 ]]; then
  echo "SMOKE PASS"
  exit 0
fi
echo "SMOKE FAIL ($FAILS check(s) failed)"
exit 1
