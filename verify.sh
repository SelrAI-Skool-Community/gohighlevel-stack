#!/bin/bash
# Checks the GoHighLevel stack is installed and the credentials actually work.
# Run from the repo root:   bash verify.sh
SRC="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"
PASS=0; FAIL=0

ok()   { echo "  PASS  $1"; PASS=$((PASS+1)); }
bad()  { echo "  FAIL  $1"; FAIL=$((FAIL+1)); }

SKILLS="ghl-crm ghl-browser ghl-contacts-pipeline ghl-calendars-booking \
ghl-payments-invoicing ghl-conversation-ai ghl-social-planner ghl-ads-manager \
ghl-landing-pages ghl-email-flows email-sequence-ghl"

echo ""
echo "GoHighLevel stack, verify"
echo ""

# 1. Skills present
missing=""
for s in $SKILLS; do
  [ -f "$SKILLS_DIR/$s/SKILL.md" ] || missing="$missing $s"
done
if [ -z "$missing" ]; then
  ok "all 11 skills installed"
else
  bad "missing skills:$missing  (run: bash install.sh)"
fi

# 2. Credentials present
ENV_FILE="$SRC/secrets/ghl.env"
if [ -n "$GHL_API_KEY" ]; then
  ok "GHL_API_KEY set in the environment"
elif [ -f "$ENV_FILE" ] && ! grep -q "your_token_here" "$ENV_FILE"; then
  ok "secrets/ghl.env filled in"
  # shellcheck disable=SC1090
  . "$ENV_FILE"
else
  bad "no credentials, open secrets/ghl.env and fill in the two values"
fi

# 3. Credentials are not the placeholder
if [ -n "$GHL_LOCATION_ID" ] && [ "$GHL_LOCATION_ID" != "your_location_id_here" ]; then
  ok "location id set"
else
  bad "GHL_LOCATION_ID is still the placeholder"
fi

# 4. The token actually works, this is the check that matters
if [ -n "$GHL_API_KEY" ] && [ "$GHL_API_KEY" != "your_token_here" ]; then
  CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    "${GHL_BASE_URL:-https://services.leadconnectorhq.com}/contacts/?locationId=$GHL_LOCATION_ID&limit=1" \
    -H "Authorization: Bearer $GHL_API_KEY" \
    -H "Version: ${GHL_API_VERSION:-2021-07-28}")
  case "$CODE" in
    200) ok "live API call returned 200, the token works" ;;
    401) bad "401 from GHL, the token is wrong, expired, or missing the contacts scope" ;;
    403) bad "403 from GHL, the token is valid but lacks permission for this location" ;;
    404) bad "404 from GHL, check GHL_LOCATION_ID is the right sub-account" ;;
    000) bad "could not reach GHL, check your internet connection" ;;
    *)   bad "unexpected HTTP $CODE from GHL" ;;
  esac
else
  bad "skipped the live API check, no usable token"
fi

# 5. Safety gate is in place
if [ -x "$SRC/scripts/ghl" ]; then
  OUT=$(GHL_API_KEY=probe "$SRC/scripts/ghl" delete-contact probe 2>&1)
  if echo "$OUT" | grep -q "BLOCKED"; then
    ok "safety gate blocks deletes and sends without confirmation"
  else
    bad "safety gate is NOT blocking destructive commands"
  fi
else
  bad "scripts/ghl missing or not executable"
fi

echo ""
echo "  $PASS passed, $FAIL failed"
echo ""
[ "$FAIL" -eq 0 ] || exit 1
