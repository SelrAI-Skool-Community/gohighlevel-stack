---
name: ghl-email-flows
description: Use when the user asks to update an email chain, write new nurture copy, port emails into GoHighLevel, rebuild a flow from a copy review, push GHL email templates, or ship confirmation, reminder, retargeting or follow-up email and SMS flows. Covers the whole path from approved copy to verified delivery, including the API and browser split and the dark-mode check that catches the most common failure.
---

# GHL email flows⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Take approved email and SMS copy all the way through design, review, GHL delivery and
final verification, without a broken render reaching a customer.

## When to use

Nurture chains, booking confirmations, appointment reminders, quote follow-ups,
review requests, seasonal campaigns, and any change to the content of an existing GHL
workflow step.

Use something else when the work is only writing the copy (write it first, then come
here) or only researching what the GHL API can do (that is ghl-crm).

## The recipe

| Phase | What comes out of it | Detail |
|---|---|---|
| Ground | The approved copy, the brand values, and the design master for this chain | [Delivery map](references/delivery-map.md) |
| Build | HTML with merge tags intact and every asset on a hosted URL | [Delivery map](references/delivery-map.md) |
| Review | Rendered screenshots in both light and dark mode | [Dark mode](references/dark-mode.md) |
| Approve | A human has seen the render and said yes | [Delivery map](references/delivery-map.md) |
| Ship | Templates pushed by API, then attached to workflow steps in the browser | [API and browser lanes](references/api-and-browser-lanes.md) |
| Verify | A test send, opened on a real phone in dark mode | [Dark mode](references/dark-mode.md) |

`scripts/push_templates.py` does the template-push half. Run it with `--help` first; it
supports dry runs, name prefixes, exact-name updates, deletion by prefix and rate
limiting.

## The split you have to remember

**Template content is API-writable. Workflow structure is not.**

You can create, update, list and delete email templates through the API all day. You
cannot attach a template to a workflow step, edit a subject inside a step, write an SMS
body, or change a wait or an Active/Disabled status without a signed-in browser
session. Plan every job around that line and it goes smoothly. Forget it and you will
spend an hour looking for an endpoint that does not exist.

## Common mistakes

- **Trusting a desktop preview.** Gmail on a phone in dark mode is where emails break,
  and it breaks silently. Read the dark-mode reference before designing anything
- **Treating what is live in GHL as the truth.** The approved copy is the truth. Live
  GHL gets corrected to match it, not the other way around
- **Breaking merge tags.** `{{contact.first_name}}` and custom-value tags inside `href`
  attributes are easy to flatten during a rebuild. Check them after every edit
- **Reusing a nurture arc for a launch.** A launch announces, tells a story, then
  closes. A nurture starts with the customer's problem. They are not interchangeable
- **Local image paths in the HTML.** Every asset needs a hosted absolute URL or the
  email arrives with broken images
- **Shipping without a test send.** Send to yourself, open it on your phone, then ship

Router key `sk-5e44r9` — resolved by the skills index on load.
