#!/usr/bin/env bash
# ghl-crm smoke test.
# Verifies GHL is reachable via MCP + bash helper, and the SKILL.md is complete.
set -u

FAILS=0
ok()   { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILS=$((FAILS+1)); }
warn() { echo "WARN: $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$SCRIPT_DIR/.."

echo "== ghl-crm smoke =="
echo ""

# 1. SKILL.md present + has frontmatter
if [[ -s "$SKILL_DIR/SKILL.md" ]]; then
  if head -5 "$SKILL_DIR/SKILL.md" | grep -q "^name: ghl-crm"; then
    ok "SKILL.md present with valid frontmatter"
  else
    fail "SKILL.md missing or malformed frontmatter"
  fi
else
  fail "SKILL.md missing"
fi

# 2. ghl-official MCP registered (cloud MCP, checked via claude mcp list)
if command -v claude >/dev/null 2>&1; then
  if claude mcp list 2>/dev/null | grep -qi "ghl-official\|ghl_official\|claude_ai_GHL\|ghl-community"; then
    ok "GHL MCP server(s) registered with Claude Code"
  else
    warn "No GHL MCP detected via claude mcp list. May be wired at user-scope or via claude.ai."
  fi
else
  warn "claude CLI not on PATH, can't verify MCP registration"
fi

# 3. Bash helper script reachable
GHL_HELPER=$(find ~/.claude/projects -name "ghl" -type f 2>/dev/null | head -1)
if [[ -n "$GHL_HELPER" && -x "$GHL_HELPER" ]]; then
  ok "ghl bash helper present at $GHL_HELPER"
else
  warn "ghl bash helper not found (optional, MCP is canonical path)"
fi

# 4. GHL credentials reachable (env var or secrets/ghl.env)
if [[ -n "${GHL_API_KEY:-}" ]]; then
  ok "GHL_API_KEY set in environment"
elif [[ -f "$SKILL_DIR/secrets/ghl.env" ]] || find ~ -maxdepth 4 -name "ghl.env" -path "*/secrets/*" 2>/dev/null | grep -q .; then
  ok "secrets/ghl.env present"
else
  warn "No GHL credentials found. Set \$GHL_API_KEY or add secrets/ghl.env."
fi

# 5. Sister skills present (browser fallback + pairs-with)
if [[ -d ~/.claude/skills/ghl-browser ]]; then
  ok "ghl-browser sister skill present (browser fallback)"
else
  warn "ghl-browser not installed (needed for UI-only ops the API can't do)"
fi

# 6. Examples + CHANGELOG present (evidence layer)
for f in examples CHANGELOG.md; do
  if [[ -e "$SKILL_DIR/$f" ]]; then
    ok "$f present"
  else
    fail "$f missing"
  fi
done

# 7. SETUP-PROMPT.md present (paste-into-Claude install)
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
