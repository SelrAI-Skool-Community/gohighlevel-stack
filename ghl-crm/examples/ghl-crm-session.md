# Worked example: ghl-crm session

Real session showing common GHL CRM operations, using a bathroom renovation
company as the example business.

## Setup

- Skill: `ghl-crm` v1.1.0
- Location ID: `<YOUR_LOCATION_ID>`
- MCP servers in use: ghl-official + ghl-community
- Total contacts: 3,900+

## Example 1: Search contacts by email

```
User: Look up the contact for sarah@example.com.au

Claude: [calls mcp__ghl-official__contacts_get-contacts with email=sarah@example.com.au]

Found 1 contact:
- Sarah Mitchell (sarah@example.com.au)
- Tags: prospect, quote-requested
- Last opportunity: "Ensuite Renovation — Mitchell" — Won, $18,500
- Last conversation: 3 days ago (SMS reply to follow-up)

What would you like to do?
```

## Example 2: Create a new contact + add to pipeline

```
User: Add contact: John Smith, john@example.com, +61 4XX XXX XXX, tag him as new-lead, put him in the Renovation Enquiries pipeline at stage "New Enquiry"

Claude: [calls mcp__ghl-official__contacts_create-contact]
[calls mcp__ghl-official__contacts_add-tags with tag="new-lead"]
[calls mcp__ghl-official__opportunities_create-opportunity (via ghl-community as ghl-official lacks create)]

Created:
- Contact: John Smith (ID: 7Xa2Bcd...)
- Tag added: new-lead
- Opportunity: "John Smith — Bathroom Renovation" in Renovation Enquiries pipeline, stage "New Enquiry"
```

## Example 3: Send an email (the html-vs-message quirk)

```
User: Send John Smith an email confirming his site-measure appointment.

Claude: [composes message]
[calls mcp__ghl-official__conversations_send-a-new-message with:
  type=Email
  contactId=7Xa2Bcd...
  html="<p>Hi John,</p><p>Your site measure is confirmed for Thursday 10am.</p><p>See you then.</p><p>Sample Renovations</p>"
  subject="Site measure confirmed"
  emailFrom="Sample Renovations <hello@example.com>"
  userId=<your-ghl-user-id>
]

Sent. Message ID returned: msg_abc123...
```

**Why not `message`?** GHL Email API requires `html` field. SMS uses `message`. Mixing causes 422 errors. See SKILL.md "API Quirks" section.

## Example 4: Pipeline status check

```
User: How many opportunities are in the Renovation Enquiries pipeline right now, grouped by stage?

Claude: [calls mcp__ghl-official__opportunities_get-pipelines to get the pipeline ID]
[calls mcp__ghl-official__opportunities_search-opportunity with pipelineId, limit=100]

Renovation Enquiries pipeline status:
- New Enquiry: 24 opps ($240,000 total value)
- Site Measure Booked: 8 ($96,000)
- Quote Sent: 3 ($52,500)
- Negotiation: 2 ($34,000)
- Closed Won (this month): 7 ($126,000)
- Closed Lost (this month): 4 ($48,000)

Total active: 37 opps, $422,500 value
```

## Example 5: Bulk tag operation

```
User: Find everyone tagged with "quote-sent" and add the tag "follow-up-needed"

Claude: [calls mcp__ghl-community__get-contacts with query for quote-sent tag, paginated]
[loops calling mcp__ghl-community__add-tags per contact]

Done. 47 contacts now have both "quote-sent" and "follow-up-needed" tags.
```

## Example 6: When the API can't do it (handoff to ghl-browser)

```
User: Add a new stage called "Awaiting Contract" between "Negotiation" and "Closed Won" in the Renovation Enquiries pipeline.

Claude: GHL API doesn't support pipeline stage configuration. Handing off to /ghl-browser.

[invokes ghl-browser skill, which drives agent-browser]
[navigates to app.gohighlevel.com → Opportunities → Pipeline Settings]
[adds stage, drags it into position]

Stage "Awaiting Contract" added in position 4 (between Negotiation and Closed Won). 
Reload your GHL UI to see it.
```

## Common 422 error and how to fix

```
User: Send Sarah an email saying "thanks for the enquiry"

Claude: [accidentally uses message instead of html, gets 422]
Caught 422 Unprocessable. GHL Email needs `html` not `message`. Retrying.

[retries with html="<p>Thanks for the enquiry</p>"]
Sent. Message ID: msg_xyz789...
```

This is the most common GHL API mistake. SKILL.md documents it explicitly so it doesn't repeat.

## What kit-doctor sees after the cook

```
== ghl-crm ==
Verdict: Promising (avg 4.2)  [was Needs work 2.8]

Scores:
  clarity            [#####] 5
  install_story      [####.] 4   [was 4]
  trigger_fidelity   [#####] 5   [was 2 — frontmatter description rewritten]
  differentiation    [###..] 3   [default, kit-index yaml not supplied]
  evidence           [####.] 4   [was 1 — smoke + examples + CHANGELOG added]
```

Lifts to Production once the kit-index supplies the differentiation cross-check.
