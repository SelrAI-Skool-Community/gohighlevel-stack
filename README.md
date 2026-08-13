# GoHighLevel stack⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

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

That is a GoHighLevel API limitation. This stack has three ways to reach the API:

1. **MCP lane, optional.** Run `claude mcp list` and use whatever name your machine shows
   for its GoHighLevel server. No fixed MCP name is assumed.
2. **REST lane.** Call GoHighLevel directly with the Private Integration Token in
   `secrets/ghl.env`.
3. **CLI lane.** Use the repo-root `scripts/ghl` helper, which reads the same credentials.

The stack is fully functional without MCP. When the public API has no endpoint, `ghl-browser`
drives the signed-in GHL interface. The capability matrix in
`ghl-crm/references/capability-matrix.md` is the authority on which route applies.

## Install

You need Claude Code installed, and a GoHighLevel account you are an admin on.

**No GoHighLevel account yet?** There is a sub-account at $25 USD a month, 15 days free,
and that tier carries everything this stack drives: CRM, pipelines, calendars,
conversations, social planner and funnels. You do not need a higher tier for any of the
eleven skills.

https://buy.stripe.com/3cI3cx4432n43HU8bS0Ny0i

Full detail, including the scopes to tick: [GET-A-GHL-ACCOUNT.md](GET-A-GHL-ACCOUNT.md).

**Already paying for GoHighLevel through someone else?** You do not have to start again.
GoHighLevel can move a sub-account between agencies and your contacts, pipelines,
calendars, workflows and funnels go with it. The steps, the message to send, and the list
of what breaks in a move: [MOVE-YOUR-ACCOUNT.md](MOVE-YOUR-ACCOUNT.md).

**Fastest path:** open a new Claude Code session and paste the one prompt in
[SETUP-PROMPT.md](SETUP-PROMPT.md). Claude does the clone and the install. Otherwise,
clone this repo and run:

```sh
bash install.sh
```

That copies the eleven skills into `~/.claude/skills/` and creates `secrets/ghl.env`.

Then open `secrets/ghl.env` and fill in two values. The file tells you where to find
each one:

- `GHL_API_KEY`, a Private Integration Token from GHL Settings
- `GHL_LOCATION_ID`, the id in your GHL URL

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
Move enquiry 2048 to Quote Sent and add a note about the revised service scope.
```

```
Build me a follow-up sequence for quotes that go quiet after five days.
```

```
What service consultations are booked next Tuesday?
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

If Claude cannot find a GHL MCP tool, ask Claude to run `claude mcp list` and retry with
the GoHighLevel server name shown there. Direct REST and `scripts/ghl` work regardless.

Router key `sk-1kem77e` — resolved by the skills index on load.
