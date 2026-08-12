# One-prompt install

Open a new Claude Code session and paste this in:

```
Install the GoHighLevel stack for me, following the install steps in https://github.com/luke-heka/gohighlevel-stack
```

That is the whole install. Claude clones the repo, copies the eleven skills into
`~/.claude/skills/`, creates your credentials file, and stops to ask you for two values.

---

## What Claude is being asked to do

If you would rather drive it yourself, this is the sequence:

1. Clone `https://github.com/luke-heka/gohighlevel-stack` into a folder you will keep.
   The folder stays. It holds your credentials file and the `scripts/ghl` helper.
2. Run `bash install.sh` from the repo root.
3. Open `secrets/ghl.env` and fill in the two required values:
   - `GHL_API_KEY` — a Private Integration Token from GHL Settings > Private Integrations
   - `GHL_LOCATION_ID` — the id in your GHL URL
4. Run `bash verify.sh`. It must print `5 passed, 0 failed`.
   Check four is the one that matters: it makes a real call to GoHighLevel with your
   token. A PASS there means you are connected.
5. Restart Claude Code so the eleven skills load.

## Then check it worked

In a fresh session, ask:

```
How many contacts are in my GHL account?
```

A real number back means the whole chain is live: skill, helper, token, location.

## If verify fails

- `401` — the token is wrong, expired, or was created without the scope for the thing
  you asked for. Mint a new Private Integration with the scopes ticked.
- `403` — the token is valid but is not allowed on that location.
- `404` — `GHL_LOCATION_ID` points at a different sub-account. Recheck the id in your
  GHL URL.
- `could not reach GHL` — network, not credentials.

Tell Claude the exact line that failed. Every skill in the stack carries its own
troubleshooting table and Claude will work the fix from there.
