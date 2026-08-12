---
name: ghl-conversation-ai
description: Runs GoHighLevel's Conversation AI stack, covering knowledge bases, chat and voice AI agents, agent actions/goals, the embeddable chat widget, and brand boards/voices. Use when the user says things like "set up an AI chat agent for the site", "train the GHL knowledge base off our website", "build a voice AI agent for inbound calls", "add FAQs to the knowledge base", "clone the chat widget onto the new funnel", "check the AI agent's call logs", "review how the chatbot answered that lead", "set up a brand voice so the AI sounds like us", "crawl our site into the AI", "the AI agent isn't answering leads, fix it", "give the voice agent a booking action", "why did the bot say that to a lead".
---

# GHL Conversation AI⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Runs GoHighLevel's most under-used lane: the AI chat and voice agents that can
answer leads 24/7 across web chat, SMS, social DMs, and phone calls, grounded in a trained
knowledge base and a consistent brand voice. This is a DOMAIN PLAYBOOK under `ghl-crm`.
Read that skill first for the full ladder, quirks, and safety rules; this file only adds
what's specific to Conversation AI.

## Execution ladder (see `ghl-crm` for the full version)

1. **ghl-official** has no fixed tools for this domain, so go straight to ghl-v2.
2. **ghl-v2 meta-tools**: `search_operations {query, domains:["knowledge-base","voice-ai","chat-widget","brand-boards"]}`, then `describe_operation` for the exact body schema, then `execute_operation` with a deliberate `idempotencyKey` on every write.
3. No MCP client handy: `ghl-crm/scripts/ghl_v2_call.py execute_operation '{...}'`.

Full op table, organised by task: `references/operations.md`.

## Core playbooks

### 1. Build a knowledge base from a website crawl and FAQs
Goal: give an agent a grounded, accurate source of truth before it talks to a single lead.
1. `createKnowledgeBase`, named for the brand/offer it serves (e.g. "Sample Bathrooms Co, main site").
2. `discoverWebsite` with the KB id plus the root URL. Kicks off the crawler.
3. Poll `getCrawlingStatusForLatestOperation` until it reports done.
4. `getAllWebsiteUrlsDataByKnowledgeBase`, reviewing the discovered URL list before training; drop anything stale (old pricing pages, dead campaigns).
5. `trainDiscoveredUrls` with the selected URL ids. Crawling does NOT auto-train; this step is separate and required.
6. `create` (FAQs) for anything the site doesn't say in plain language: objections, policy answers, "how does X work" questions the agent will get asked but the site buries.
7. Verify: `getKnowledgeBaseById` plus `list` (faqs), confirming counts match what was trained.

### 2. Create a Conversation AI (chat) agent and wire it to channels
Goal: an agent that answers web chat, SMS, and social DMs consistently.
1. `voice-ai.create-agent` with the KB id attached, the channels it should answer (chat/SMS/social), and its prompt/personality.
2. `voice-ai.create-action` for each real job it needs to do beyond answering questions: book a call, tag a hot lead, hand off to a human.
3. `patch-agent` to attach a brand voice (playbook 5) once one exists.
4. Verify: `voice-ai.get-agent`, confirming KB, actions, and channels all show attached, then send it a real test message on each wired channel.

### 3. Voice AI agent setup and call-log review
Goal: an inbound phone line answered by AI, with a real escalation path.
1. `voice-ai.create-agent` with the voice channel configured, and a phone number attached per the location's phone-system setup.
2. `voice-ai.create-action` for a live-transfer/escalation action. Never ship a voice agent without one; a caller must always be able to reach a human.
3. Run a real test call end to end (ask it something in-scope, then something it should escalate).
4. `get-call-logs` filtered by date to review a batch, then `getCallLog` on any call worth listening to for QA. Transcript and recording detail live here.
5. Verify: escalated calls actually landed in the right place (check the destination, not just that the agent said it would transfer).

### 4. Deploy or clone the chat widget onto a new funnel/site
Goal: reuse a proven widget config instead of rebuilding branding/behaviour each time.
1. `listChatWidget`, finding the widget that's already dialled in (branding, greeting, agent binding).
2. `cloneChatWidget` from that widget's id rather than creating from scratch.
3. `patchChatWidget` for anything that needs to differ (greeting copy, which agent it's bound to, position).
4. Verify: `getChatWidget`, confirming the clone points at the right agent, then embed the snippet on the target page (browser-only, see below).

### 5. Brand board and brand voice, so every agent sounds consistent
Goal: one tone of voice the AI writes in everywhere, not a different personality per agent.
1. `createBrandBoard` if the location doesn't have one yet.
2. `create-brand-voice` with the actual tone rules (not generic "friendly and professional", the specific words, banned phrases, sentence rhythm the brand uses).
3. `set-default-brand-voice`. This becomes what new agents inherit unless overridden.
4. Verify: `getBrandBoardsByLocation` / `list-brand-voices`, confirming it saved, then re-pull one live agent reply and check it actually reads in that voice.

### 6. Review AI agent conversations for quality
Goal: catch a bad answer before it costs a lead, not after.
1. Voice agents: `get-call-logs` for the period, then `getCallLog` on flagged calls for transcript and recording.
2. Chat/SMS/social agents: message content lives in the `conversations` domain, not here; use `ghl-crm` / `mcp__ghl-official__conversations_search-conversation` plus `_get-messages` to pull the actual transcript.
3. Pattern-match: the same wrong answer twice means the knowledge base is missing or wrong, not a one-off. Fix the KB (playbook 1) or add an FAQ, don't just re-prompt the agent.
4. If an agent is giving out information nobody verified (pricing, dates, guarantees), pull that content into the KB/FAQ from a real source immediately. Never leave a live agent citing unverified facts.

### 7. Manage agent actions/goals (booking, transfer, data capture)
Goal: keep an agent's job list current as the business's process changes.
1. `get-action` (or list via the agent's config) to see what's currently wired.
2. `voice-ai.update-action` to change a goal's trigger condition or destination (e.g. a new booking calendar id).
3. `voice-ai.delete-action` only after confirming nothing live still depends on it (check the agent config first).

## Domain gotchas

- **Crawl then train are two separate steps.** `discoverWebsite` only builds the candidate URL list; nothing is trained until `trainDiscoveredUrls` runs against selected ids. A crawl that "did nothing" usually means training was skipped.
- **One agent object, all channels.** The API domain is still named `voice-ai` for historical reasons, but `/voice-ai/agents/{agentId}` is the single object behind chat, SMS, social DM, and phone. Don't look for a separate `/conversation-ai/agents` path; it doesn't exist.
- **Default brand voice is location-wide.** `set-default-brand-voice` changes what every agent inherits unless it has an explicit override, so check how many active agents rely on the default before changing it.
- **FAQ delete opId is inconsistently named** (`knowledge-base.delete` instead of a `delete-faq`-style id), a naming quirk in the catalog, not a functional gap.
- **`agent-studio`** (create/execute/promote agent workflows) is named in the `ghl-crm` capability matrix as living in this domain but is not one of the 43 ops in this pack. Run `search_operations` for it before assuming it needs the browser lane.

## Browser-only edges

- **Embedding the widget snippet into a funnel/website page** is browser-only. Page content read/write belongs to the `funnels` domain, which is BROWSER-ONLY per the capability matrix. Create/clone/configure the widget here via API, then route the actual paste-into-page step to `ghl-browser`.
- Everything else in this domain (knowledge base, agents, actions, call logs, widget config, brand boards/voices) is API-FULL. Nothing else in Conversation AI needs the browser lane.

## Safety rails

Inherit `ghl-crm`'s rules (no bulk sends without approval, no contact deletes, deliberate `idempotencyKey`, verify every write). On top of those:

1. **Never delete a knowledge base, trained URLs, or an agent that's live** without confirming no active channel still depends on it. That's an instant drop to zero coverage on real inbound leads.
2. **Never ship a voice or chat agent without a working escalation/handoff action.** A lead or caller must always be able to reach a human path.
3. **Never let an agent state a fact nobody verified** (price, guarantee, availability, policy). Pull it from a real source into the KB/FAQ first, or flag it TBC. Same rule as everywhere else: no fabricated facts.
4. **Changing the default brand voice or a shared knowledge base affects every agent that inherits it.** Treat it like a shared-infra change, not a single-agent edit.
5. Activating a NEW voice agent onto a real, published phone number is a production change (it starts taking real calls). Treat it the same as any other "going live" moment: verify the escalation path works before leaving it unattended.

Router key `sk-03gy0y` — resolved by the skills index on load.
