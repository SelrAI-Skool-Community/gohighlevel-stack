---
name: email-sequence-ghl
description: Use when someone says "build me a 5-email sequence for X", "set up the nurture for Y", "follow up the quotes that went quiet", or needs a complete welcome, nurture and close sequence provisioned in GoHighLevel. Drafts the copy, pushes the templates through the API, builds the workflow in the browser, and ships it PAUSED for a human to approve. Route a single one-off email to a general email skill, and non-GHL automation to that platform's own skill.
version: 2.0
tags: email-sequence, ghl, automation, workflow-builder, nurture
---

# Email sequences in GoHighLevel⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

One sentence in, a five-email sequence goes live in GHL with the right trigger, the
right delays and the right exit conditions. It ships **paused** every time, so a person
decides when real customers start receiving it.

## When to use

- A new enquiry source needs a follow-up chain
- Quotes are going out and going quiet, and nobody is chasing them
- An existing GHL workflow has stale copy and needs rebuilding
- A seasonal or promotional push needs a short campaign

## When not to use

- A single one-off email. Just write it
- Transactional email (receipt, password reset, booking confirmation). Build those in
  the GHL UI directly, where the transactional templates live
- Anything outside GHL. Use that platform's own skill

## Step 1 — Brief intake, four questions

Ask these before drafting anything. Do not guess the answers.

1. **What is this sequence for?** The service, the offer, or the moment in the job.
   Examples: a new renovation enquiry, a quote that has not been answered, a finished
   job asking for a review, a maintenance reminder a year on
2. **What starts it?** Form fill, page visit, manual tag, pipeline stage change, or a
   paid deposit
3. **What is the one thing it should make happen?** Book the site visit? Accept the
   quote? Leave a review? One goal, not three
4. **What is the strongest proof you have?** A named past job, a photo set, a real
   review. If there is no real proof point, say so and write without one

## Step 2 — The five-email shape

This is the default. Change it when the brief says something different.

| # | Email | Delay | Job it does |
|---|---|---|---|
| 1 | Welcome | Immediate | Confirm what they asked for and what happens next |
| 2 | Proof | +1 day | One real job, what it involved, how it turned out |
| 3 | Objection | +3 days | Answer the single biggest reason people hesitate |
| 4 | How it works | +5 days | Walk through your actual process, step by step |
| 5 | Close | +7 days | A direct ask and a clear, honest deadline |

For a quote-chase sequence, compress it: immediate, +2 days, +5 days, +10 days, and a
final one at +21 days that closes the loop politely either way.

## Step 3 — Draft the copy

Each email needs:

- **Subject line**, under 50 characters, no em dashes
- **Preheader**, under 80 characters, saying something the subject does not
- **Body**, 150 to 300 words. Shorter beats longer. One idea per email
- **One call to action.** Reply, book, read, or call. Never two
- **Footer** with your business's legal postal address and a working unsubscribe link

Write the way you talk to a customer standing in your showroom. Concrete beats clever.

## Step 4 — Check it before it goes near GHL

Every email, no exceptions:

- No em dashes. Grep for `—` and `–` and fix what you find
- No filler words: elevate, harness, leverage, seamless, unlock, revolutionise
- **No promise you have not agreed to keep.** No guaranteed outcomes, no refund terms,
  no support levels, no timeframes you cannot hit. This is the one that creates real
  liability, and it is the easiest to write by accident
- **Never invent a testimonial, a review, a number or a past job.** If you do not have
  a real one, write the email without it
- Every email has a different subject and preheader. Five variations of the same line
  reads as automation, because it is

## Step 5 — Provision in GHL, two lanes

The workflow builder has **no public API**. See the capability matrix in
`ghl-crm/references/capability-matrix.md`. So provisioning splits:

**Lane A — templates, through the API, automatic.** Push each drafted email as a GHL
email template using the builder endpoints (`POST /emails/builder`, then
`/emails/builder/data`; `updatedBy` is required and the call fails silently-ish
without it). Open every returned `previewUrl` and look at it. Full recipe in the
ghl-email-flows skill.

**Lane B — the workflow itself, through the browser.** See ghl-browser for the engine.

1. Create a workflow named `<purpose>-nurture-<yyyy-mm-dd>`
2. Set the trigger from question 2 of the brief
3. Add five email actions with the delays from the table, attaching the Lane A templates
4. Tag on entry: `nurture-<purpose>-active`
5. Set the exit conditions, and do not skip this step:
   - They bought or accepted → exit, tag `converted-<purpose>`
   - They replied → exit, and assign the contact to a real person to answer
   - They unsubscribed → exit (GHL handles this, but confirm it is on)

## Step 6 — Ship it paused

**Never enable a sequence automatically.** The workflow ships paused, and you report:

- The workflow name and where to find it
- The trigger condition in plain English
- The five subject lines
- The exit conditions

Then a person opens it, reads it, and turns it on. That person is whoever owns the
customer relationship, not whoever ran the build.

## Step 7 — Keep a copy

Save the finished sequence as a markdown file in your own project folder, one file per
sequence, named for the purpose and the date. Next time you need something similar you
edit a known-good chain instead of starting from nothing.

## Hard rules

- **Ships paused. Every time.** Going live is a human decision
- **Never invent proof.** No fabricated reviews, job numbers, timeframes or prices
- **Unsubscribe link and a real postal address in every email.** Australian Spam Act
  applies to commercial email, and the fines are real
- **Never promise an outcome, a refund or a support level** that has not been agreed
- **Exit conditions are not optional.** A sequence with no "stop on convert" keeps
  emailing people who already said yes, which is the fastest way to look careless

## Common mistakes

1. **Turning it on to "see if it works".** It works on real customers. Test with your
   own address on the list first
2. **One subject line, five emails.** Reads as a robot
3. **Chasing on a fixed clock regardless of what the customer did.** If they replied,
   the sequence should have stopped
4. **Writing five emails about you.** Four about them, one about you, roughly

Router key `sk-1m0wshd` — resolved by the skills index on load.
