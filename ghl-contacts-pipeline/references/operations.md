# ghl-contacts-pipeline - operations reference (129 ops)

Reorganised from the raw v2 catalog slice by BUSINESS TASK, not by path. Every op:
`METHOD /path` - opId `...` | scopes: `...` | kind: read/write/delete.

Look up exact params with `describe_operation({operationId, domain})` before calling
`execute_operation` - this file is for finding the right op fast, not full schemas.

## 1. Contact lifecycle & search (7 ops, domain: contacts)

- `POST /contacts/` - opId `create-contact` | scopes: contacts.write | kind: write
- `GET /contacts/{contactId}` - opId `get-contact` | scopes: contacts.readonly | kind: read
- `PUT /contacts/{contactId}` - opId `update-contact` | scopes: contacts.write | kind: write
- `POST /contacts/upsert` - opId `upsert-contact` | scopes: contacts.write | kind: write
- `DELETE /contacts/{contactId}` - opId `delete-contact` | scopes: contacts.write | kind: delete
- `POST /contacts/search` - opId `search-contacts-advanced` | scopes: contacts.readonly | kind: read
- `GET /contacts/search/duplicate` - opId `get-duplicate-contact` | scopes: contacts.readonly | kind: read

## 2. Tags, custom fields & custom values - segmentation (26 ops)

Contact-level tags (domain: contacts):
- `POST /contacts/{contactId}/tags` - opId `add-tags` | scopes: contacts.write | kind: write
- `DELETE /contacts/{contactId}/tags` - opId `remove-tags` | scopes: contacts.write | kind: delete
- `POST /contacts/bulk/tags/update/{type}` - opId `contacts.create-association` | scopes: contacts.write | kind: write (bulk tag add/remove by type)

Location tag definitions (domain: locations):
- `GET /locations/{locationId}/tags` - opId `get-location-tags` | scopes: locations/tags.readonly | kind: read
- `POST /locations/{locationId}/tags` - opId `create-tag` | scopes: locations/tags.write | kind: write
- `GET /locations/{locationId}/tags/{tagId}` - opId `get-tag-by-id` | scopes: locations/tags.readonly | kind: read
- `PUT /locations/{locationId}/tags/{tagId}` - opId `update-tag` | scopes: locations/tags.write | kind: write
- `DELETE /locations/{locationId}/tags/{tagId}` - opId `delete-tag` | scopes: locations/tags.write | kind: delete

Custom field definitions (domain: custom-fields, object-scoped - contacts/opportunities/objects):
- `POST /custom-fields/` - opId `custom-fields.create-custom-field` | scopes: locations/customFields.write | kind: write
- `GET /custom-fields/object-key/{objectKey}` - opId `get-custom-fields-by-object-key` | scopes: locations/customFields.readonly | kind: read
- `GET /custom-fields/{id}` - opId `get-custom-field-by-id` | scopes: locations/customFields.readonly | kind: read
- `PUT /custom-fields/{id}` - opId `custom-fields.update-custom-field` | scopes: locations/customFields.write | kind: write
- `DELETE /custom-fields/{id}` - opId `custom-fields.delete-custom-field` | scopes: locations/customFields.write | kind: delete
- `POST /custom-fields/folder` - opId `create-custom-field-folder` | scopes: locations/customFields.write | kind: write
- `PUT /custom-fields/folder/{id}` - opId `update-custom-field-folder` | scopes: locations/customFields.write | kind: write
- `DELETE /custom-fields/folder/{id}` - opId `delete-custom-field-folder` | scopes: locations/customFields.write | kind: delete

Custom field definitions, location-scoped shorthand (domain: locations):
- `GET /locations/{locationId}/customFields` - opId `get-custom-fields` | scopes: locations/customFields.readonly | kind: read
- `POST /locations/{locationId}/customFields` - opId `locations.create-custom-field` | scopes: locations/customFields.write | kind: write
- `GET /locations/{locationId}/customFields/{id}` - opId `get-custom-field` | scopes: locations/customFields.readonly | kind: read
- `PUT /locations/{locationId}/customFields/{id}` - opId `locations.update-custom-field` | scopes: locations/customFields.write | kind: write
- `DELETE /locations/{locationId}/customFields/{id}` - opId `locations.delete-custom-field` | scopes: locations/customFields.write | kind: delete

Custom values (location-wide merge variables, domain: locations):
- `GET /locations/{locationId}/customValues` - opId `get-custom-values` | scopes: locations/customValues.readonly | kind: read
- `POST /locations/{locationId}/customValues` - opId `create-custom-value` | scopes: locations/customValues.write | kind: write
- `GET /locations/{locationId}/customValues/{id}` - opId `get-custom-value` | scopes: locations/customValues.readonly | kind: read
- `PUT /locations/{locationId}/customValues/{id}` - opId `update-custom-value` | scopes: locations/customValues.write | kind: write
- `DELETE /locations/{locationId}/customValues/{id}` - opId `delete-custom-value` | scopes: locations/customValues.write | kind: delete

## 3. Notes, tasks & appointments - contact activity (17 ops, domain: contacts + locations)

- `GET /contacts/{contactId}/notes` - opId `get-all-notes` | scopes: contacts.readonly | kind: read
- `POST /contacts/{contactId}/notes` - opId `create-note` | scopes: contacts.write | kind: write
- `GET /contacts/{contactId}/notes/{id}` - opId `get-note` | scopes: contacts.readonly | kind: read
- `PUT /contacts/{contactId}/notes/{id}` - opId `update-note` | scopes: contacts.write | kind: write
- `DELETE /contacts/{contactId}/notes/{id}` - opId `delete-note` | scopes: contacts.write | kind: delete
- `GET /contacts/{contactId}/tasks` - opId `get-all-tasks` | scopes: contacts.readonly | kind: read
- `POST /contacts/{contactId}/tasks` - opId `create-task` | scopes: contacts.write | kind: write
- `GET /contacts/{contactId}/tasks/{taskId}` - opId `get-task` | scopes: contacts.readonly | kind: read
- `PUT /contacts/{contactId}/tasks/{taskId}` - opId `update-task` | scopes: contacts.write | kind: write
- `PUT /contacts/{contactId}/tasks/{taskId}/completed` - opId `update-task-completed` | scopes: contacts.write | kind: write
- `DELETE /contacts/{contactId}/tasks/{taskId}` - opId `delete-task` | scopes: contacts.write | kind: delete
- `GET /contacts/{contactId}/appointments` - opId `get-appointments-for-contact` | scopes: contacts.readonly | kind: read
- `POST /locations/{locationId}/recurring-tasks` - opId `create-recurring-task` | scopes: recurring-tasks.write | kind: write
- `GET /locations/{locationId}/recurring-tasks/{id}` - opId `get-recurring-task-by-id` | scopes: recurring-tasks.readonly | kind: read
- `PUT /locations/{locationId}/recurring-tasks/{id}` - opId `update-recurring-task` | scopes: recurring-tasks.write | kind: write
- `DELETE /locations/{locationId}/recurring-tasks/{id}` - opId `delete-recurring-task` | scopes: recurring-tasks.write | kind: delete
- `POST /locations/{locationId}/tasks/search` - opId `task-search` | scopes: locations/tasks.readonly | kind: read (cross-contact task search - the hygiene-sweep workhorse)

## 4. Opportunities & pipeline (12 ops, domain: opportunities)

- `POST /opportunities/` - opId `create-opportunity` | scopes: opportunities.write | kind: write
- `POST /opportunities/upsert` - opId `Upsert-opportunity` | scopes: opportunities.write | kind: write
- `GET /opportunities/{id}` - opId `get-opportunity` | scopes: opportunities.readonly | kind: read
- `PUT /opportunities/{id}` - opId `update-opportunity` | scopes: opportunities.write | kind: write
- `PUT /opportunities/{id}/status` - opId `update-opportunity-status` | scopes: opportunities.write | kind: write
- `DELETE /opportunities/{id}` - opId `delete-opportunity` | scopes: opportunities.write | kind: delete
- `GET /opportunities/search` - opId `search-opportunity` | scopes: opportunities.readonly | kind: read
- `POST /opportunities/search` - opId `search-opportunities-advanced` | scopes: opportunities.readonly | kind: read
- `GET /opportunities/pipelines` - opId `get-pipelines` | scopes: opportunities.readonly | kind: read (pipeline/stage IDs - read only, structure is browser-only)
- `GET /opportunities/lost-reason` - opId `get-lost-reason` | scopes: opportunities.readonly | kind: read
- `POST /opportunities/{id}/followers` - opId `add-followers-opportunity` | scopes: opportunities.write | kind: write
- `DELETE /opportunities/{id}/followers` - opId `remove-followers-opportunity` | scopes: opportunities.write | kind: delete

## 5. Conversations & messaging (20 ops, domain: conversations)

- `POST /conversations/` - opId `create-conversation` | scopes: conversations.write | kind: write
- `GET /conversations/{conversationId}` - opId `get-conversation` | scopes: conversations.readonly | kind: read
- `PUT /conversations/{conversationId}` - opId `update-conversation` | scopes: conversations.write | kind: write
- `DELETE /conversations/{conversationId}` - opId `delete-conversation` | scopes: conversations.write | kind: delete
- `GET /conversations/search` - opId `search-conversation` | scopes: conversations.readonly | kind: read
- `GET /conversations/{conversationId}/messages` - opId `get-messages` | scopes: conversations/message.readonly | kind: read
- `GET /conversations/messages/{id}` - opId `get-message` | scopes: conversations/message.readonly | kind: read
- `POST /conversations/messages` - opId `send-a-new-message` | scopes: conversations/message.write | kind: write
- `POST /conversations/messages/inbound` - opId `add-an-inbound-message` | scopes: conversations/message.write | kind: write
- `POST /conversations/messages/outbound` - opId `add-an-outbound-message` | scopes: conversations/message.write | kind: write
- `PUT /conversations/messages/{messageId}/status` - opId `update-message-status` | scopes: conversations/message.write | kind: write
- `PUT /conversations/messages/{messageId}/attachments` - opId `add-message-attachments` | scopes: conversations/message.write | kind: write
- `DELETE /conversations/messages/{messageId}/schedule` - opId `cancel-scheduled-message` | scopes: conversations/message.write | kind: delete
- `DELETE /conversations/messages/email/{emailMessageId}/schedule` - opId `cancel-scheduled-email-message` | scopes: conversations/message.write | kind: delete
- `GET /conversations/messages/email/{id}` - opId `get-email-by-id` | scopes: conversations/message.readonly | kind: read
- `GET /conversations/messages/{messageId}/locations/{locationId}/recording` - opId `get-message-recording` | scopes: conversations/message.readonly | kind: read
- `GET /conversations/locations/{locationId}/messages/{messageId}/transcription` - opId `get-message-transcription` | scopes: conversations/message.readonly | kind: read
- `GET /conversations/locations/{locationId}/messages/{messageId}/transcription/download` - opId `download-message-transcription` | scopes: conversations/message.readonly | kind: read
- `GET /conversations/messages/export` - opId `export-messages-by-location` | scopes: conversations/message.readonly | kind: read
- `POST /conversations/providers/live-chat/typing` - opId `live-chat-agent-typing` | scopes: conversations/livechat.write | kind: write

## 6. Workflow & campaign enrolment (7 ops)

- `POST /contacts/{contactId}/workflow/{workflowId}` - opId `add-contact-to-workflow` | scopes: contacts.write | kind: write
- `DELETE /contacts/{contactId}/workflow/{workflowId}` - opId `delete-contact-from-workflow` | scopes: contacts.write | kind: delete
- `POST /contacts/{contactId}/campaigns/{campaignId}` - opId `add-contact-to-campaign` | scopes: contacts.write | kind: write
- `DELETE /contacts/{contactId}/campaigns/{campaignId}` - opId `remove-contact-from-campaign` | scopes: contacts.write | kind: delete
- `DELETE /contacts/{contactId}/campaigns/remove-all` - opId `remove-contact-from-every-campaign` | scopes: contacts.write | kind: delete
- `GET /campaigns/` - opId `get-campaigns` | scopes: campaigns.readonly | kind: read
- `GET /workflows/` - opId `get-workflow` | scopes: workflows.readonly | kind: read (name + ID list only - no steps, browser-only to build/edit)

## 7. Trigger links (6 ops, domain: links)

- `POST /links/` - opId `create-link` | scopes: links.write | kind: write
- `GET /links/id/{linkId}` - opId `get-link-by-id` | scopes: links.readonly | kind: read
- `GET /links/` - opId `get-links` | scopes: links.readonly | kind: read
- `GET /links/search` - opId `search-trigger-links` | scopes: links.readonly | kind: read
- `PUT /links/{linkId}` - opId `update-link` | scopes: links.write | kind: write
- `DELETE /links/{linkId}` - opId `delete-link` | scopes: links.write | kind: delete

## 8. Custom objects & records (9 ops, domain: objects)

- `GET /objects/` - opId `get-object-by-location-id` | scopes: objects/schema.readonly | kind: read
- `POST /objects/` - opId `create-custom-object-schema` | scopes: objects/schema.write | kind: write
- `GET /objects/{key}` - opId `get-object-schema-by-key` | scopes: objects/schema.readonly | kind: read
- `PUT /objects/{key}` - opId `update-custom-object` | scopes: objects/schema.write | kind: write (no schema delete - API-permanent once created)
- `POST /objects/{schemaKey}/records` - opId `create-object-record` | scopes: objects/record.write | kind: write
- `GET /objects/{schemaKey}/records/{id}` - opId `get-record-by-id` | scopes: objects/record.readonly | kind: read
- `PUT /objects/{schemaKey}/records/{id}` - opId `update-object-record` | scopes: objects/record.write | kind: write
- `DELETE /objects/{schemaKey}/records/{id}` - opId `delete-object-record` | scopes: objects/record.write | kind: delete
- `POST /objects/{schemaKey}/records/search` - opId `search-object-records` | scopes: objects/record.readonly | kind: read

## 9. Associations & relations (10 ops, domain: associations)

- `GET /associations/` - opId `find-associations` | scopes: associations.readonly | kind: read
- `POST /associations/` - opId `associations.create-association` | scopes: associations.write | kind: write
- `GET /associations/{associationId}` - opId `get-association-by-ID` | scopes: associations.readonly | kind: read
- `PUT /associations/{associationId}` - opId `update-association` | scopes: associations.write | kind: write
- `DELETE /associations/{associationId}` - opId `delete-association` | scopes: associations.write | kind: delete
- `GET /associations/key/{key_name}` - opId `get-association-key-by-key-name` | scopes: associations.readonly | kind: read
- `GET /associations/objectKey/{objectKey}` - opId `get-association-by-object-keys` | scopes: associations.readonly | kind: read
- `POST /associations/relations` - opId `create-relation` | scopes: associations/relation.write | kind: write
- `GET /associations/relations/{recordId}` - opId `get-relations-by-record-id` | scopes: associations/relation.readonly | kind: read
- `DELETE /associations/relations/{relationId}` - opId `delete-relation` | scopes: associations/relation.write | kind: delete

## 10. Followers & business linkage (9 ops)

- `POST /contacts/{contactId}/followers` - opId `add-followers-contact` | scopes: contacts.write | kind: write
- `DELETE /contacts/{contactId}/followers` - opId `remove-followers-contact` | scopes: contacts.write | kind: delete
- `POST /contacts/bulk/business` - opId `add-remove-contact-from-business` | scopes: contacts.write | kind: write
- `GET /contacts/business/{businessId}` - opId `get-contacts-by-businessId` | scopes: contacts.readonly | kind: read
- `GET /businesses/` - opId `get-businesses-by-location` | scopes: businesses.readonly | kind: read
- `POST /businesses/` - opId `create-business` | scopes: businesses.write | kind: write
- `GET /businesses/{businessId}` - opId `get-business` | scopes: businesses.readonly | kind: read
- `PUT /businesses/{businessId}` - opId `update-business` | scopes: businesses.write | kind: write
- `DELETE /businesses/{businessId}` - opId `delete-Business` | scopes: businesses.write | kind: delete

## 11. Location config - templates, channels, timezones (6 ops, domain: locations)

- `GET /locations/search` - opId `search-locations` | scopes: locations.readonly | kind: read
- `GET /locations/{locationId}` - opId `get-location` | scopes: locations.readonly | kind: read
- `GET /locations/{locationId}/conversationChannels/{type}` - opId `get-conversation-channel` | scopes: locations.readonly | kind: read
- `GET /locations/{locationId}/templates` - opId `GET-all-or-email-sms-templates` | scopes: locations/templates.readonly | kind: read
- `DELETE /locations/{locationId}/templates/{id}` - opId `DELETE-an-email-sms-template` | scopes: locations/templates.write | kind: delete (no create/update - GET+DELETE only, see capability matrix)
- `GET /locations/{locationId}/timezones` - opId `get-timezones` | scopes: locations.readonly | kind: read
