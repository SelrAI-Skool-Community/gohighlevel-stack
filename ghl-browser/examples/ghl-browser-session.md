# Worked example: ghl-browser session⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Three concrete examples of browser-only GHL work.

## Example 1: Rename a pipeline stage

```text
User: Configure the Sales Pipeline stages as New Enquiry, Contacted, Quote Sent, Won, and Lost.

Claude checks the capability matrix, reuses the signed-in browser session, opens
Opportunities, then Pipeline Settings, sets the five stages in order, and reloads the pipeline.

Verified stages: New Enquiry, Contacted, Quote Sent, Won, Lost.
```

## Example 2: Recover from a stalled page

```text
User: Add the Quote Request form to the service page.

Claude opens the funnel builder. The page is still blank after 20 seconds, so Claude
reopens it through agent-browser, takes a fresh interactive snapshot, and continues.

The form is saved, the live page is reloaded, and a test submission creates one contact.
```

## Example 3: Hand off API-capable work

```text
User: Move enquiry 2048 to Quote Sent.

Claude checks the capability matrix and sees that moving an opportunity between existing
stages is API-capable. It uses ghl-crm through the available MCP, REST, or scripts/ghl
lane, then fetches the opportunity again.

Verified: enquiry 2048 is now in Quote Sent.
```

Router key `sk-1djxbff` — resolved by the skills index on load.
