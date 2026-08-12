# Conversation AI operations, by business task

43 ops from the v2 catalog, domain-tagged `knowledge-base`, `voice-ai`, `chat-widget`,
`brand-boards`. Reorganised below by business task. Use the registered GoHighLevel MCP
server, direct REST, or repo-root `scripts/ghl raw`. Supply an `idempotencyKey` when the
operation schema requires it.

GHL's product is branded "Conversation AI" (chat, SMS, social messaging, voice all answered by
the same AI employee), but the underlying API domain is still named `voice-ai`. There is
no separate `/conversation-ai/*` path. One agent object (`/voice-ai/agents/{agentId}`)
covers every channel; which channel(s) it answers is set in the create/patch body, not by
a different endpoint family.

## 1. Knowledge base, create and manage

| Task | Method / path | opId | scopes | kind |
|---|---|---|---|---|
| List KBs | `GET /knowledge-bases/` | `listAllKnowledgeBasesPaginated` | knowledge-bases.readonly | read |
| Create KB | `POST /knowledge-bases/` | `createKnowledgeBase` | knowledge-bases.write | write |
| Get KB by id | `GET /knowledge-bases/{knowledgeBaseId}` | `getKnowledgeBaseById` | knowledge-bases.readonly | read |
| Update KB | `PUT /knowledge-bases/{id}` | `updateKnowledgeBase` | knowledge-bases.write | write |
| Delete KB | `DELETE /knowledge-bases/{knowledgeBaseId}` | `deleteKnowledgeBase` | knowledge-bases.write | delete |

## 2. Knowledge base, website crawler (train from the website)

| Task | Method / path | opId | scopes | kind |
|---|---|---|---|---|
| Discover URLs from a site | `POST /knowledge-bases/crawler` | `discoverWebsite` | knowledge-bases.write | write |
| Check crawl status | `GET /knowledge-bases/crawler/status` | `getCrawlingStatusForLatestOperation` | knowledge-bases.readonly | read |
| List discovered URLs + data | `GET /knowledge-bases/crawler` | `getAllWebsiteUrlsDataByKnowledgeBase` | knowledge-bases.readonly | read |
| Train selected URLs into the KB | `POST /knowledge-bases/crawler/train` | `trainDiscoveredUrls` | knowledge-bases.write | write |
| Remove trained URLs | `DELETE /knowledge-bases/crawler` | `deleteTrainedUrlsForKnowledgeBase` | knowledge-bases.write | delete |

## 3. Knowledge base, FAQs

| Task | Method / path | opId | scopes | kind |
|---|---|---|---|---|
| List FAQs | `GET /knowledge-bases/faqs` | `list` | knowledge-bases.readonly | read |
| Create FAQ | `POST /knowledge-bases/faqs` | `create` | knowledge-bases.write | write |
| Update FAQ | `PUT /knowledge-bases/faqs/{id}` | `update` | knowledge-bases.write | write |
| Delete FAQ | `DELETE /knowledge-bases/faqs/{id}` | `knowledge-base.delete` | knowledge-bases.write | delete |

## 4. Conversation AI / Voice AI agents (the unified agent object)

| Task | Method / path | opId | scopes | kind |
|---|---|---|---|---|
| List agents | `GET /voice-ai/agents` | `get-agents` | voice-ai-agents.readonly | read |
| Create agent | `POST /voice-ai/agents` | `voice-ai.create-agent` | voice-ai-agents.write | write |
| Get agent | `GET /voice-ai/agents/{agentId}` | `voice-ai.get-agent` | voice-ai-agents.readonly | read |
| Patch agent (config, channels, KB, prompt) | `PATCH /voice-ai/agents/{agentId}` | `patch-agent` | voice-ai-agents.write | write |
| Delete agent | `DELETE /voice-ai/agents/{agentId}` | `voice-ai.delete-agent` | voice-ai-agents.write | delete |

## 5. Agent actions / goals (booking, transfer, escalation, data capture)

| Task | Method / path | opId | scopes | kind |
|---|---|---|---|---|
| Create action | `POST /voice-ai/actions` | `voice-ai.create-action` | voice-ai-agent-goals.write | write |
| Get action | `GET /voice-ai/actions/{actionId}` | `get-action` | voice-ai-agent-goals.readonly | read |
| Update action | `PUT /voice-ai/actions/{actionId}` | `voice-ai.update-action` | voice-ai-agent-goals.write | write |
| Delete action | `DELETE /voice-ai/actions/{actionId}` | `voice-ai.delete-action` | voice-ai-agent-goals.write | delete |

## 6. Voice AI dashboard, call logs (QA a voice agent)

| Task | Method / path | opId | scopes | kind |
|---|---|---|---|---|
| List call logs | `GET /voice-ai/dashboard/call-logs` | `get-call-logs` | voice-ai-dashboard.readonly | read |
| Get one call log (transcript/recording detail) | `GET /voice-ai/dashboard/call-logs/{callId}` | `getCallLog` | voice-ai-dashboard.readonly | read |

## 7. Chat widget (deploy/clone onto a funnel or site)

| Task | Method / path | opId | scopes | kind |
|---|---|---|---|---|
| List widgets | `GET /chat-widget/list` | `listChatWidget` | chat-widget.readonly | read |
| Get widget | `GET /chat-widget/data/{locationId}/{id}` | `getChatWidget` | chat-widget.readonly | read |
| Create widget | `POST /chat-widget/` | `createChatWidget` | chat-widget.write | write |
| Clone widget | `POST /chat-widget/clone` | `cloneChatWidget` | chat-widget.write | write |
| Update widget (full) | `PUT /chat-widget/data/{locationId}/{id}` | `updateChatWidget` | chat-widget.write | write |
| Patch widget (partial) | `PATCH /chat-widget/data/{locationId}/{id}` | `patchChatWidget` | chat-widget.write | write |
| Delete widget | `DELETE /chat-widget/{locationId}/{id}` | `chat-widget.delete` | chat-widget.write | delete |

## 8. Brand boards (design kit)

| Task | Method / path | opId | scopes | kind |
|---|---|---|---|---|
| List boards for location | `GET /brand-boards/{locationId}` | `getBrandBoardsByLocation` | brand-boards/design-kit.readonly | read |
| Get board | `GET /brand-boards/{locationId}/{id}` | `getBrandBoardById` | brand-boards/design-kit.readonly | read |
| Create board | `POST /brand-boards/` | `createBrandBoard` | brand-boards/design-kit.write | write |
| Update board | `PATCH /brand-boards/{locationId}/{id}` | `updateBrandBoard` | brand-boards/design-kit.write | write |
| Delete board | `DELETE /brand-boards/{locationId}/{id}` | `deleteBrandBoard` | brand-boards/design-kit.write | delete |

## 9. Brand voices (tone the AI agent writes in)

| Task | Method / path | opId | scopes | kind |
|---|---|---|---|---|
| List brand voices | `GET /brand-boards/locations/{locationId}/brand-voices` | `list-brand-voices` | brand-boards/voices.readonly | read |
| Get brand voice | `GET /brand-boards/locations/{locationId}/brand-voices/{brandVoiceId}` | `get-brand-voice` | brand-boards/voices.readonly | read |
| Create brand voice | `POST /brand-boards/locations/{locationId}/brand-voices` | `create-brand-voice` | brand-boards/voices.write | write |
| Update brand voice | `PATCH /brand-boards/locations/{locationId}/brand-voices/{brandVoiceId}` | `update-brand-voice` | brand-boards/voices.write | write |
| Set as default | `POST /brand-boards/locations/{locationId}/brand-voices/{brandVoiceId}/default` | `set-default-brand-voice` | brand-boards/voices.write | write |
| Delete brand voice | `DELETE /brand-boards/locations/{locationId}/brand-voices/{brandVoiceId}` | `delete-brand-voice` | brand-boards/voices.write | delete |

## Not in this pack

`agent-studio` (create/execute/promote agent workflows) is named in the ghl-crm capability
matrix as part of this domain but did not surface as ops in this 43-op slice. If a task
needs it, run `search_operations {query:"agent studio"}` before assuming it's browser-only.
Actual chat message content (the transcript a chat/SMS/social agent produced) lives in the
`conversations` domain, not here; see `ghl-crm` for MCP, REST, and CLI routes.
