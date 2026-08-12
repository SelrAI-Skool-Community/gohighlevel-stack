---
name: ghl-calendars-booking
description: Runs GoHighLevel calendars and booking end to end. Creates and configures calendars, sets availability/schedules, finds free slots and books appointments for a contact, reschedules or cancels with notifications, blocks out time, manages calendar groups, and manages resources (rooms/equipment) and bookable services. Use when the user says things like "book a discovery call for this lead", "what slots are free tomorrow", "reschedule that appointment", "cancel their booking", "block out Friday afternoon", "set up a service consultation calendar", "add a room resource", "who's on the calendar this week", "create a round-robin calendar group", "pull today's bookings" or "give me the week's ops brief".
---

# GHL Calendars & Booking⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Runs the calendars domain (59 operations) for a small service business. Calendars cover
discovery calls, service consultations, and team or room availability. This is a domain
playbook under **`ghl-crm`**: read
that skill first for the full ladder, cross-cutting quirks, and safety rules. This file
only adds calendars-specific detail.

## Execution ladder

1. **MCP, optional**: run `claude mcp list` and use the registered GoHighLevel server
   name. Use fixed calendar reads when available. Otherwise search, describe, then
   execute the relevant full-catalog operation.
2. **Direct REST**: use the method and path in `references/operations.md` with the token
   from repo-root `secrets/ghl.env`.
3. **CLI**: use repo-root `scripts/ghl` calendar commands or `scripts/ghl raw` for
   another documented endpoint. REST and CLI work without MCP.

Full op list reorganised by task: `references/operations.md`.

## Core playbooks

### 1. Create and configure a calendar with availability
1. `create-calendar`: name, calendarType, eventType, assign team member(s).
2. `createCalendarSchedule` on the new `calendarId`: weekly hours, timezone, booking
   notice window, buffer time. For team-wide hours instead of per-calendar, run
   `createSchedule` once, then `add-calendar-to-schedule` for each calendar that shares it.
3. `create-event-notification`: at least a confirmation email and a reminder. Service
   consultations should also carry a cancellation notification.
4. Verify: `get-calendar` and `getCalendarSchedule`, confirm hours and notifications saved.

### 2. Find free slots and book an appointment for a contact
1. `get-slots` on the target `calendarId` with `startDate`/`endDate` (epoch ms) and the
   business's `timezone`. Never assume UTC, always pass timezone explicitly.
2. Pick a slot, `create-appointment` with `calendarId`, `contactId`, `locationId`,
   `startTime`/`endTime` (ISO), `title`, `appointmentStatus: "confirmed"`.
3. Verify: `get-appointment` on the returned `eventId`, confirm the exact time landed
   (double-booking shows as a 200 with an overlapping slot, not an error).
4. Tag the contact per ghl-crm's safety rule 5 (e.g. `booked-discovery-call`).

### 3. Reschedule an appointment
1. `get-appointment` to confirm current time/contact before touching it.
2. `edit-appointment` with the new `startTime`/`endTime`. The calendar's own
   `create-event-notification` rules fire the reschedule email/SMS automatically, no
   separate send needed.
3. Verify: `get-appointment` again, confirm new time, `appointmentStatus` unchanged.

### 4. Cancel an appointment
1. `edit-appointment` with `appointmentStatus: "cancelled"`. This preserves the booking
   record and lets the calendar's cancellation notification fire.
2. Only use `delete-event` for genuine junk (test bookings, spam). A hard delete removes
   the row entirely and breaks any downstream reporting that joins on `eventId`.

### 5. Block out a slot (team unavailable, room in use, holiday)
1. `create-block-slot`: `calendarId`, `startTime`/`endTime`, descriptive `title`
   (e.g. "Team offsite", "Room booked, external client").
2. `get-blocked-slots` to verify it now excludes that window from `get-slots` results.
3. To adjust: `edit-block-slot`. To release the time: `delete-event` on the block's
   `eventId` (blocks are events, same delete path as appointments).

### 6. Set up a calendar group (round-robin or bundled booking page)
1. `validate-groups-slug`: confirm the public URL slug is free before committing to it.
2. `create-calendar-group` with that slug.
3. Attach the calendars that should share the group's booking page (group membership is
   set via `update-calendar`/`edit-group` team/calendar fields; run `describe_operation`
   on `edit-group` for the exact field name on this account's schema version).
4. `disable-group` to pull the public page down without deleting history. `delete-group`
   only when the lane is retired for good.

### 7. Manage resources (rooms/equipment) for service consultations
1. `fetch-calendar-resources` on `resourceType: "rooms"` (or `"equipments"`): check what's
   already registered before creating a duplicate.
2. `create-calendar-resource`: name, capacity/quantity, for example
   `Consultation Room A`, capacity 12.
3. Reference the resource when building the service catalog entry (playbook 8) so
   capacity constraints apply to bookings automatically.
4. `update-calendar-resource` / `delete-calendar-resource` as rooms/gear change.

### 8. Book a recurring group service via the services catalog
Use this lane instead of a plain calendar when the business needs capacity limits and a
fixed venue per session (group seats, not 1:1 calls).
1. `create-service-catalog`: name, for example `Saturday Group Service`, with a 90-minute
   duration, $120 price, and capacity 12.
2. `create-service-location`: the venue for that service.
3. `create-service-booking`: books one seat/attendee against a specific service, location,
   and time.
4. Verify: `get-service-booking-by-id`, and `get-service-bookings` filtered by date to
   confirm the session isn't over capacity before confirming more attendees.

### 9. Pull an upcoming-events list for a day/week ops brief
1. `get-calendar-events` **[fixed tool]**: pass the date range and, if scoping to one lane,
   the relevant `calendarId` (discovery calls, service consultations, and team availability
   are usually separate calendars; check `get-calendars` once per install and record the
   IDs so this doesn't need re-discovery every brief).
2. Cross-reference `get-appointment-notes` **[fixed tool]** on any booking that needs
   context before the call/session.
3. For blocks in the same window, `get-blocked-slots`. A clean ops brief separates
   "booked with a contact" from "blocked/unavailable".

## Domain gotchas

- `get-slots` and `create-appointment` both want explicit timezone. GHL will not infer it
  from the location record reliably; pass it every time to avoid off-by-hours bookings.
- Availability lives in two places: the `event-calendar` schedule (per-calendar hours) and
  standalone `schedules` (shared team availability a group of calendars attach to). Don't
  set both and expect them to merge cleanly, pick one model per calendar.
- Notifications are configured per-calendar, not per-appointment. A one-off "don't remind
  this person" ask isn't an API lever; it's a support conversation with the attendee, or a
  cancel-then-manual-note workaround.
- `resourceType` is a path segment (`rooms` / `equipments`), not a query param. Get it
  wrong and the fixed-tool/meta-tool call 404s, not 400s.
- Cancelling via `edit-appointment` status change (not `delete-event`) is what keeps the
  booking visible in reporting and notification history. Default to that.
- Calendar groups and the services catalog are two different bundling mechanisms: groups
  are a public booking page across calendars, services are a capacity-limited session
  type. Don't reach for a group when the ask is really "limit this group service to 12 seats",
  that's services catalog plus resources.

## Browser-only edges

- Visual theming of the public booking widget/page (colors, logo placement, custom CSS,
  embedding the calendar into a funnel page) is page-builder territory, route to
  `ghl-browser`. The calendar's functional settings (hours, notifications, team, slug) are
  all API-writable per above; only the pixel-level look-and-feel is not.
- Nothing else in this domain is browser-only. Calendars is API-FULL per the ghl-crm
  capability matrix.

## Safety rails

Inherits ghl-crm's baseline (no bulk sends without approval, no contact deletes,
deliberate idempotencyKey, verify every write). Adds for this domain:

1. Never `delete-event` or `delete-calendar` on a booking/calendar with real attendee
   history. Cancel via status change instead; hard deletes are for genuine junk only.
2. A cancellation or reschedule reaches a real person by email/SMS automatically once the
   notification rule exists. Treat `edit-appointment` on someone else's confirmed booking
   with the same care as a live send, not a silent data edit.
3. Check capacity (`get-service-bookings` count vs the service's capacity) before
   confirming a group service seat. Overbooking a physical room is a real-world failure, not
   just a data inconsistency.
4. Deleting a calendar group or resource that's still referenced by an active service
   breaks future bookings silently. Check `get-services-catalog`/`get-service-locations`
   for references before removing either.

Router key `sk-3lwfox` — resolved by the skills index on load.
