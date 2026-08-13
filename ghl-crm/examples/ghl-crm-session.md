# Worked example: ghl-crm session⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Real session showing common GHL CRM operations for a small service business.

## Setup

- Location ID: `<YOUR_LOCATION_ID>`
- Connection lane: MCP, using the GoHighLevel server returned by `claude mcp list`
- REST and `scripts/ghl` remain available without MCP
- Total contacts: 3,912

## Example 1: Search contacts by email

```
User: Look up the contact for customer1042@example.com

Claude: [uses the active GHL MCP server's contacts search with email=customer1042@example.com]

Found 1 contact:
- Customer 1042 (customer1042@example.com)
- Tags: prospect, quote-requested
- Last opportunity: "Annual Service Plan, Customer 1042", Won, $18,500
- Last conversation: 3 days ago (SMS reply to follow-up)
```

## Example 2: Create a new contact + add to pipeline

```
User: Add Customer 2048 with customer2048@example.com, tag the record as new-lead, and put it in the Sales Pipeline at stage "New Enquiry".

Claude: [uses the active GHL MCP server's contacts_create-contact operation]
[uses contacts_add-tags with tag="new-lead"]
[uses the opportunity create operation exposed by the same GHL MCP server]

Created:
- Contact: Customer 2048 (ID: 7Xa2Bcd...)
- Tag added: new-lead
- Opportunity: "Annual Service Plan, Customer 2048" in Sales Pipeline, stage "New Enquiry"
```

## Example 3: Send an email (the html-vs-message quirk)

```
User: Send Customer 2048 an email confirming the service consultation.

Claude: [composes message]
[uses the active GHL MCP server's conversations_send-a-new-message operation with:
  type=Email
  contactId=7Xa2Bcd...
  html="<p>Hello,</p><p>Your service consultation is confirmed for Thursday at 10:00.</p><p>Sample Co</p>"
  subject="Service consultation confirmed"
  emailFrom="Sample Co <updates@example.com>"
  userId=<your-ghl-user-id>
]

Sent. Message ID returned: msg_abc123...
```

**Why not `message`?** GHL Email API requires `html` field. SMS uses `message`. Mixing causes 422 errors. See `../SKILL.md`, API quirks.

## Example 4: Pipeline status check

```
User: How many opportunities are in the Sales Pipeline right now, grouped by stage?

Claude: [uses the active GHL MCP server's opportunities_get-pipelines operation]
[uses opportunities_search-opportunity with pipelineId, limit=100]

Sales Pipeline status:
- New Enquiry: 24 opps ($240,000 total value)
- Contacted: 8 ($96,000)
- Quote Sent: 3 ($52,500)
- Won (this month): 7 ($126,000)
- Lost (this month): 4 ($48,000)

Total active: 35 opps, $388,500 value
```

## Example 5: Bulk tag operation

```
User: Find everyone tagged with "quote-sent" and add the tag "follow-up-needed"

Claude: [uses the active GHL MCP server's contact search for the quote-sent tag, paginated]
[loops through the same server's add-tags operation for each contact]

Done. 47 contacts now have both "quote-sent" and "follow-up-needed" tags.
```

## Example 6: When the API can't do it (handoff to ghl-browser)

```
User: Configure the Sales Pipeline stages as New Enquiry, Contacted, Quote Sent, Won, and Lost, in that order.

Claude: GHL API does not support pipeline stage configuration. Handing off to ghl-browser.

[invokes ghl-browser skill, which drives agent-browser]
[navigates to app.gohighlevel.com, then Opportunities, then Pipeline Settings]
[renames the stage and drags it into position]

The Sales Pipeline now uses New Enquiry, Contacted, Quote Sent, Won, and Lost.
Reload the GHL interface to see it.
```

## Common 422 error and how to fix

```
User: Send Customer 1042 an email saying "thanks for the enquiry"

Claude: [accidentally uses message instead of html, gets 422]
Caught 422 Unprocessable. GHL Email needs `html` not `message`. Retrying.

[retries with html="<p>Thanks for the enquiry</p>"]
Sent. Message ID: msg_xyz789...
```

This is the most common GHL API mistake. `../SKILL.md` documents it explicitly.

Router key `sk-1plhl9m` — resolved by the skills index on load.
