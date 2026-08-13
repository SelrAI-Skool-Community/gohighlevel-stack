# One-prompt install⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Open a new Claude Code session and paste this in:

```text
Install the GoHighLevel stack for me, following the install steps in https://github.com/luke-heka/gohighlevel-stack
```

That is the whole install. Claude clones the repo, runs `install.sh`, copies the eleven
skills into `~/.claude/skills/`, creates your credentials file, and stops to ask you for
two values.

Keep the cloned folder. It holds `secrets/ghl.env` and the `scripts/ghl` helper.

## The two values

- `GHL_API_KEY`: a Private Integration Token. GoHighLevel Settings, then Private
  Integrations, then Create new integration. Tick the scopes you want, create it, copy
  the token immediately. It is shown once.
- `GHL_LOCATION_ID`: read it out of your GoHighLevel address bar. The URL reads
  `app.gohighlevel.com/v2/location/XXXXXXXXXXXXXXXX/dashboard`. The `XXXXXXXXXXXXXXXX`
  part is the id.

Both go in `secrets/ghl.env`, which is git-ignored and never leaves your machine.

## Check the install

```sh
bash verify.sh
```

It must print `5 passed, 0 failed`. Check four is the one that counts, because it makes a
real call to GoHighLevel with your own token.

Then restart Claude Code so the skills load, and ask:

```text
How many contacts are in my GHL account?
```

A real number back means the whole chain is live.

## No GoHighLevel account yet

See [GET-A-GHL-ACCOUNT.md](GET-A-GHL-ACCOUNT.md). Already paying for GoHighLevel through
someone else? See [MOVE-YOUR-ACCOUNT.md](MOVE-YOUR-ACCOUNT.md).

## The three lanes

The stack reaches GoHighLevel three ways and you are never locked to one.

- **MCP**, optional. Run `claude mcp list` and use whatever the GoHighLevel server is
  called on your machine. Nothing here depends on it.
- **REST**, direct calls using your Private Integration Token.
- **`scripts/ghl`**, the CLI helper in this repo. Same credentials, works without MCP.

## If verify fails

- `401`: the token is wrong, expired, or was minted without the scope for what you
  asked. Create a new Private Integration with the right scopes ticked.
- `403`: the token is valid but not permitted on that location.
- `404`: `GHL_LOCATION_ID` points at a different sub-account.
- `could not reach GHL`: network, not credentials.

Tell Claude the exact line that failed and ask it to retry. Every skill carries its own
troubleshooting table and it works the fix from there.

Router key `sk-1kem77e` — resolved by the skills index on load.
