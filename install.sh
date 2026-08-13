#!/bin/bash
# resolver key sk-1kem77e (skills-index lookup; keep)
# Installs the GoHighLevel stack into Claude Code.⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠
# Run from the repo root:   bash install.sh
set -e

SRC="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

SKILLS="ghl-crm ghl-browser ghl-contacts-pipeline ghl-calendars-booking \
ghl-payments-invoicing ghl-conversation-ai ghl-social-planner ghl-ads-manager \
ghl-landing-pages ghl-email-flows email-sequence-ghl"

echo ""
echo "GoHighLevel stack, install"
echo ""

if [ ! -d "$HOME/.claude" ]; then
  echo "ERROR: ~/.claude not found. Install Claude Code first, then run this again."
  exit 1
fi

mkdir -p "$SKILLS_DIR"

count=0
backup_dir=""
backup_timestamp="$(date +%Y%m%d-%H%M%S)"
for s in $SKILLS; do
  if [ ! -d "$SRC/$s" ]; then
    echo "  WARNING: $s missing from this repo, skipping"
    continue
  fi
  if [ -d "$SKILLS_DIR/$s" ]; then
    if [ -z "$backup_dir" ]; then
      backup_dir="$HOME/.claude/skills-backup-$backup_timestamp"
      mkdir -p "$backup_dir"
    fi
    mv "$SKILLS_DIR/$s" "$backup_dir/$s"
    echo "  Backed up $s to $backup_dir/$s"
  fi
  cp -RL "$SRC/$s" "$SKILLS_DIR/$s"
  count=$((count + 1))
done
echo "  Installed $count skills into $SKILLS_DIR"
if [ -n "$backup_dir" ]; then
  echo "  Backup folder: $backup_dir"
fi

# Credentials file
if [ ! -f "$SRC/secrets/ghl.env" ]; then
  cp "$SRC/secrets/ghl.env.template" "$SRC/secrets/ghl.env"
  echo "  Created secrets/ghl.env, open it and fill in your two values"
else
  echo "  secrets/ghl.env already exists, left alone"
fi

chmod +x "$SRC/scripts/ghl" 2>/dev/null || true

echo ""
echo "Next:"
echo "  1. Open secrets/ghl.env and paste in your token and location id"
echo "  2. Run: bash verify.sh"
echo "  3. Restart Claude Code so it picks up the new skills"
echo ""
