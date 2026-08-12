# GoHighLevel stack

Eleven Claude skills that run GoHighLevel from a chat window instead of from the GHL
interface. Ask for what you want in plain English and Claude does the clicking.

This is the whole CRM half of the business: the enquiries, the pipeline, the bookings,
the quotes and invoices, the follow-up emails, the ads and the social posts.

**Start here, in this order.**

1. This page, for what it does and what it cannot do.
2. `ghl-crm/references/capability-matrix.md`, for exactly what the GoHighLevel API can
   and cannot do. Worth reading even if you never install the rest. It will save you
   from hunting for a feature that does not exist.
3. The install section below.

## What is in the box

| Skill | What it does |
|---|---|
| `ghl-crm` | The master skill. Ask it anything GHL and it routes the job to the right place. Start every GHL request here |
| `ghl-contacts-pipeline` | Contacts, tags, custom fields, opportunities and pipeline stages. The core CRM engine |
| `ghl-calendars-booking` | Calendars, availability, appointment booking and reminders |
| `ghl-payments-invoicing` | Invoices, payment links, orders, subscriptions and transaction records |
| `ghl-conversation-ai` | The AI chat and voice agents that answer enquiries out of hours |
| `ghl-email-flows` | Building and shipping the content of email and SMS flows, including the dark-mode check that catches the most common failure |
| `email-sequence-ghl` | Turns "build me a follow-up sequence for X" into a five-email chain, provisioned and paused |
| `ghl-landing-pages` | Landing pages, funnel pages and blog pages, with full HTML control |
| `ghl-social-planner` | Scheduling and publishing social posts through GHL |
| `ghl-ads-manager` | Facebook, Google and LinkedIn ad campaigns connected to GHL |
| `ghl-browser` | The fallback lane. Drives the GHL interface in a real browser for the things the API cannot reach |

## The one thing to understand first

**GoHighLevel's API does not cover everything the interface does.** Some things can only
be done by a browser clicking through the actual GHL screens. The big ones:

- The **workflow builder**. You can create email templates by API, but attaching them to
  a workflow step, editing subjects inside steps, writing SMS bodies and changing wait
  times all need the browser
- The **funnel page builder** and the **form builder**
- **Pipeline stage** creation and reordering

That is not a limitation of this stack, it is a limitation of GoHighLevel. The stack
handles it by having two lanes: the API lane for everything it can reach, and
`ghl-browser` for the rest. The capability matrix in `ghl-crm/references/` is the
authority on which is which. Read it before you assume something is impossible, and
before you assume something is easy.

## Install

You need Claude Code installed, and a GoHighLevel account you are an admin on.

**No GoHighLevel account yet?** There is a sub-account at $25 USD a month, and that tier
carries everything this stack drives: CRM, pipelines, calendars, conversations, social
planner and funnels.

https://buy.stripe.com/8x27sNbwvbXE1zM2Ry0Ny0c

You do not need a higher tier to run any of the eleven skills.

```sh
bash install.sh
```

That copies the eleven skills into `~/.claude/skills/` and creates `secrets/ghl.env`.

Then open `secrets/ghl.env` and fill in two values. The file tells you where to find
each one:

- `GHL_API_KEY` — a Private Integration Token from GHL Settings
- `GHL_LOCATION_ID` — the id in your GHL URL

Then check it actually worked:

```sh
bash verify.sh
```

It must print `5 passed, 0 failed`. The check that matters is the fourth one: it makes a
real call to GoHighLevel with your token. If that says PASS, you are connected. If it
says 401, the token is wrong or is missing a permission scope. If it says 404, the
location id is for a different sub-account.

Restart Claude Code afterwards so it picks up the new skills.

## How to use it

Open Claude Code and ask in normal words:

```
Show me every enquiry from the last week that hasn't been quoted yet.
```

```
Move the Henderson job to Quote Sent and add a note about the tile change.
```

```
Build me a follow-up sequence for quotes that go quiet after five days.
```

```
Who's booked into the showroom next Tuesday?
```

You do not need to know which of the eleven skills does the job. Ask `ghl-crm` and it
routes.

## Safety

Three things are deliberately hard to do by accident.

**Deletes and outbound messages are blocked by default.** The `scripts/ghl` helper
refuses `delete-contact`, `delete-opp`, `remove-tags`, `send-sms` and `send-email`
unless you explicitly confirm. This exists so an automated run cannot text your customer
list. To allow one, run it as `GHL_CONFIRM=yes ghl send-sms ...`.

**Email sequences ship paused.** A new sequence is built, provisioned and then left
switched off. A person opens it, reads it, and turns it on. That person should be
whoever owns the customer relationship.

**Your credentials never leave your machine.** `secrets/ghl.env` is git-ignored. Never
paste a token into a chat, a document or a commit. If one is ever exposed, delete the
Private Integration in GHL Settings and mint a new one; that instantly invalidates the
old token.

## Two habits worth having

**Look at the thing before you call it done.** A test send opened on your own phone
tells you more than any preview. A page you clicked through yourself tells you more than
a passing script. The skills say this repeatedly because it is the difference between
working automation and automation that looks like it works.

**Never invent proof.** No made-up reviews, job numbers, timeframes or prices in
customer-facing copy, ever. If you do not have a real one, write it without.

## When something breaks

Tell Claude what you saw. It has the troubleshooting tables for every skill and the
error-code map for the API. Most failures are one of three things: a token missing a
permission scope (401), the wrong location id (404), or you have asked for something
that is browser-only (no endpoint exists). The capability matrix settles the third one
in about ten seconds.

**One naming quirk to know about.** The skills refer to GHL tools by the names used
where they were written (`ghl-official`, `ghl-v2`). Your machine may have registered the
GoHighLevel connection under a different name. If Claude says it cannot find a GHL tool,
tell it to run `claude mcp list` and use whatever the GHL server is actually called. The
`scripts/ghl` helper and the REST lane work regardless of the MCP name, so nothing is
ever truly blocked by this.
