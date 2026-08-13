# Moving a GoHighLevel account you already have⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

If you are already paying for GoHighLevel through somebody else, you do not have to start
again. GoHighLevel has a built-in transfer that moves a sub-account from one agency to
another, and your contacts, pipelines, calendars, workflows and funnels go with it.

You cannot start the transfer yourself. Whoever holds your subscription has to send it,
and the receiving side has to accept it. Your job is to ask, and to know what to ask for.

## What you need before you ask

One thing: the **Relationship Number** of the agency you are moving to. It is the 7-digit
code GoHighLevel uses to identify an agency.

For the $25 sub-account this stack is built around, that number is:

```
0-271-499
```

The agency shows in GoHighLevel as **Selr Group**.

## The message to send

Copy this, fill in the one blank, and send it to whoever manages your GoHighLevel
subscription.

```
Hi, I'd like to move my GoHighLevel sub-account to a different agency.

Sub-account name: [YOUR SUB-ACCOUNT NAME]
Receiving agency: Selr Group
Receiving agency Relationship Number: 0-271-499

In GoHighLevel this is: Agency view, Sub-Accounts, Manage Client on my
account, Actions, Transfer Sub-account. Enter the Relationship Number above
and confirm. The receiving agency approves it from their side and the move
completes.

Before you send it, can you confirm two things:

1. Whether my phone numbers are on LeadConnector or on Twilio. If they are
   on LeadConnector on both sides they move across with the account. If
   either side is on Twilio they do not, and we need to arrange those
   separately.
2. That there are no active add-on subscriptions on the account (Dedicated
   IP, WordPress, Yext, WhatsApp), since those do not carry over.

Thanks.
```

## What moves with you

Contacts, conversations, opportunities and appointments, custom fields, custom values,
funnels and websites, calendars, workflows and automations including who is currently
enrolled in them, memberships, and any API keys scoped to that sub-account.

## What breaks and needs redoing

Plan for these. None of them are hard, they are just not automatic.

- **Every third-party connection is disconnected.** Google, Facebook, Instagram,
  QuickBooks and anything else you authorised has to be reconnected on the other side.
- **Phone numbers only move if both agencies use LeadConnector.** If either side runs
  Twilio, the numbers are handled separately and it takes a day or two.
- **Your email sending domain is removed.** The account falls back to the receiving
  agency's default email provider until you set yours up again.
- **A branded custom domain assigned by the old agency is removed.**
- **A Dedicated IP is unassigned** and its subscription ends.
- **Smartlists do not transfer.** Note down any you rely on before the move.
- **Active add-on subscriptions do not carry over**: WordPress hosting, Yext, WhatsApp,
  Dedicated IP.

Screenshot anything you cannot afford to lose before the transfer is sent. Once it moves,
the old agency's settings are gone.

## If they refuse

There is no single button that exports a whole sub-account. Contacts export to CSV from
the contacts list, and that is most of what matters. Funnels, websites, courses and
workflows cannot be exported and would have to be rebuilt.

So it is worth asking properly first. A transfer costs the sending agency nothing and
takes them about a minute.

## Two things that block a transfer outright

- An **Agency Sub-Account**, meaning the agency's own internal account rather than a
  client one, cannot be transferred at all.
- A **HIPAA** sub-account can only move to an agency that already holds the HIPAA
  Compliance add-on.

## After the move

Reconnect your integrations, then come back to the install steps and re-check your two
values rather than assuming they survived:

1. Open your GoHighLevel dashboard and read the location id straight out of the address
   bar. Compare it to `GHL_LOCATION_ID` in `secrets/ghl.env`. If it differs, paste the
   new one in.
2. Run `bash verify.sh`. If check four returns 401, mint a fresh Private Integration
   Token on the new side and paste that in too.

Check four returning 200 is the proof. It means the move landed and the stack is talking
to the right account.

Router key `sk-1kem77e` — resolved by the skills index on load.
