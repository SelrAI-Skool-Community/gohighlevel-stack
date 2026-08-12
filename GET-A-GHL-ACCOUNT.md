# Getting the GoHighLevel account this stack drives

Every skill in this bundle talks to one GoHighLevel sub-account. If you already have one,
skip to [Moving an account you already have](MOVE-YOUR-ACCOUNT.md). If you do not, this
page is the whole path.

## The account

$25 USD a month, with the first 15 days free.

https://buy.stripe.com/3cI3cx4432n43HU8bS0Ny0i

Checkout shows it as **Standard**, US$25.00 per month, billed by Selr Group. Nothing is
charged on the day you sign up.

That tier carries everything the eleven skills drive:

- Contacts, custom fields and tags
- Opportunities and pipelines
- Calendars, availability and appointment booking
- Conversations, SMS and email
- Workflows and automations
- Funnels, landing pages and forms
- Social planner
- Invoices and payment links

You do not need a higher tier for any skill in this stack. If a skill ever needs
something the tier does not include, it says so in its own troubleshooting table rather
than failing silently.

## What happens after you subscribe

1. Your sub-account is created and you get login details for it.
2. Log in and go to Settings, then Private Integrations, then Create new integration.
3. Tick the scopes for the areas you want to drive. Contacts, opportunities, calendars,
   conversations, payments and social planner covers the stack.
4. Create it and copy the token straight away. GoHighLevel shows it once.
5. Look at your browser address bar. It reads
   `app.gohighlevel.com/v2/location/XXXXXXXXXXXXXXXX/dashboard`. The `XXXXXXXXXXXXXXXX`
   part is your location id.

Paste both values into `secrets/ghl.env` in this repo. Run `bash verify.sh`. When check
four returns 200, you are connected.

## Two things worth knowing before you pay

**The 15 days are free and the subscription is monthly.** You can run the whole stack
inside the trial and decide afterwards.

**Your token stays on your machine.** `secrets/ghl.env` is git-ignored and never leaves
your computer. If a token is ever exposed, delete that Private Integration in GoHighLevel
Settings and create a new one. The old token dies the moment you do.

## If checkout does not load

Ask Claude to open the link and read the page back to you. If the page loads for Claude
and not for you, it is a browser extension or a content blocker, not the link.
