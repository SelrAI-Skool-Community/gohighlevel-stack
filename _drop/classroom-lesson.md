Lesson title: GoHighLevel stack

Category: 🔧 Weekly Builds

---

## 📋 COPY THIS FIRST

```
Install the GoHighLevel stack for me, following the install steps in https://github.com/luke-heka/gohighlevel-stack
```

Paste it into a new Claude Code session and press enter. That's the whole install.

🎥 The video above shows a full run, start to finish.

---

## ❓ What this fixes

Your CRM holds the enquiries, the pipeline, the bookings, the invoices and the follow-up, and every one of those jobs means clicking through a different screen. So the follow-up slips, the pipeline goes stale, and the quote sits unsent.

This build puts all of it behind a chat window. You ask for what you want in plain English and Claude does the clicking.

## 📦 What you get

✅ Eleven skills: contacts and pipeline, calendars and booking, payments and invoicing, conversation AI, email flows, sequence builder, landing pages, social planner, ads manager, the browser lane, and a master skill that routes any request to the right one

✅ A capability matrix naming exactly what the GoHighLevel API can and cannot do, so you stop hunting for features that do not exist

✅ A browser lane for the workflow builder, funnel builder and form builder, the three big things no API reaches

✅ A verify script that makes a real call to your account and prints 5 passed, 0 failed

🔒 Deletes and outbound sends are blocked unless you confirm them. New email sequences are provisioned switched off, so a run cannot text your customer list.

---

## 🛠 Step by step

1️⃣ Open a new Claude Code session

2️⃣ Copy the prompt at the top of this page, paste it in, press enter

3️⃣ Claude clones the repo, copies the eleven skills into your skills folder, and stops to ask you for two values: a Private Integration Token from GHL Settings, and the location id out of your GHL URL

4️⃣ Restart Claude Code so the skills load, then ask it "how many contacts are in my GHL account?"

## ✅ How you know it worked

`bash verify.sh` prints `5 passed, 0 failed`. Check four is the one that counts: it makes a real call to GoHighLevel with your own token.

## 🩹 If it stalls

Tell Claude "retry the install". It self-heals.

## 💳 No GoHighLevel account yet

You need your own GoHighLevel sub-account for any of this to run. There is one at $25 USD
a month, and that tier is all this stack needs: CRM, pipelines, calendars, conversations,
social planner and funnels.

https://buy.stripe.com/8x27sNbwvbXE1zM2Ry0Ny0c
