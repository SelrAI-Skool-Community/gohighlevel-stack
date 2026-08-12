# Calendars & Booking: operations by business task (59 ops, domain `calendars`)

Use the registered GoHighLevel MCP server, direct REST, or repo-root `scripts/ghl raw`.
Entries marked **[fixed]** may appear as fixed MCP operations. Inspect the operation
schema before a write and supply an `idempotencyKey` when required.

## 1. Calendars (create/read/update/delete the calendar object itself)
- `get-calendars`: `GET /calendars/`, list all calendars for the location
- `create-calendar`: `POST /calendars/`, new calendar (name, calendarType, eventType, widget slug, team members)
- `get-calendar`: `GET /calendars/{calendarId}`, full config of one calendar
- `update-calendar`: `PUT /calendars/{calendarId}`, edit name/slots/team/notifications settings
- `delete-calendar`: `DELETE /calendars/{calendarId}`, irreversible, kills booking history access via this calendar

## 2. Availability / schedules (working hours, timezones, shared team schedules)
- `createSchedule`: `POST /calendars/schedules`, a standalone shared availability schedule (used by calendar groups / team round-robin)
- `getAllSchedules`: `GET /calendars/schedules/search`, list schedules
- `getScheduleById` / `updateSchedule` / `deleteSchedule`: `GET|PUT|DELETE /calendars/schedules/{id}`
- `getCalendarSchedule`: `GET /calendars/schedules/event-calendar/{calendarId}`, the availability rules attached directly to one calendar
- `createCalendarSchedule` / `updateCalendarSchedule`: `POST|PUT /calendars/schedules/event-calendar/{calendarId}`, set weekly hours, date-specific overrides, timezone, buffer/notice windows
- `add-calendar-to-schedule` / `remove-calendar-from-schedule`: `PUT|DELETE /calendars/schedules/{id}/associations/{calendarId}`, attach/detach a calendar to a shared schedule

## 3. Free slots & appointments (the core booking loop)
- `get-slots`: `GET /calendars/{calendarId}/free-slots`, bookable windows for a date range (params: `startDate`/`endDate` epoch ms, `timezone`)
- `create-appointment`: `POST /calendars/events/appointments`, book (calendarId, contactId, locationId, startTime, endTime ISO, title, appointmentStatus)
- `get-appointment`: `GET /calendars/events/appointments/{eventId}`, read one booking
- `edit-appointment`: `PUT /calendars/events/appointments/{eventId}`, reschedule (new startTime/endTime) or change status (confirmed/cancelled/showed/noshow)
- `delete-event`: `DELETE /calendars/events/{eventId}`, hard-delete a booking or block (prefer `edit-appointment` status=cancelled for real bookings, keeps the audit trail)
- `get-calendar-events` **[fixed]**: fast lane for reading a date-range of events across one or more calendars (used for day/week ops briefs)

## 4. Block-out slots (holding time so nothing can be booked)
- `get-blocked-slots`: `GET /calendars/blocked-slots`, list existing blocks for a calendar/date range
- `create-block-slot`: `POST /calendars/events/block-slots`, reserve time (calendarId, startTime, endTime, title)
- `edit-block-slot`: `PUT /calendars/events/block-slots/{eventId}`, move/resize/rename a block
- Removing a block uses `delete-event` above; block slots are events too

## 5. Appointment notes
- `get-appointment-notes` **[fixed]**: read notes on a booking
- `create-appointment-note`: `POST /calendars/appointments/{appointmentId}/notes`
- `update-appointment-note`: `PUT /calendars/appointments/{appointmentId}/notes/{noteId}`
- `delete-appointment-note`: `DELETE /calendars/appointments/{appointmentId}/notes/{noteId}`

## 6. Notifications (booking confirmations, reminders, cancellations)
- `get-event-notification`: `GET /calendars/{calendarId}/notifications`, list configured notifications for a calendar
- `create-event-notification`: `POST /calendars/{calendarId}/notifications`, add an email/SMS notification rule (type: confirmation/reminder/cancellation/reschedule, channel, timing)
- `find-event-notification`: `GET /calendars/{calendarId}/notifications/{notificationId}`
- `update-event-notification` / `delete-event-notification`: `PUT|DELETE /calendars/{calendarId}/notifications/{notificationId}`

## 7. Calendar groups (bundle calendars under one public booking page)
- `get-groups`: `GET /calendars/groups`, list groups
- `create-calendar-group`: `POST /calendars/groups`, new group (name, slug, description)
- `validate-groups-slug`: `POST /calendars/groups/validate-slug`, check a slug is free before creating
- `edit-group`: `PUT /calendars/groups/{groupId}`
- `disable-group`: `PUT /calendars/groups/{groupId}/status`, enable/disable the group's public page without deleting it
- `delete-group`: `DELETE /calendars/groups/{groupId}`

## 8. Resources (rooms, equipment tied to a booking type)
- `fetch-calendar-resources`: `GET /calendars/resources/{resourceType}`, `resourceType` is `equipments` or `rooms`
- `create-calendar-resource`: `POST /calendars/resources/{resourceType}`, new room/equipment (name, capacity, quantity)
- `get-calendar-resource`: `GET /calendars/resources/{resourceType}/{id}`
- `update-calendar-resource`: `PUT /calendars/resources/{resourceType}/{id}`
- `delete-calendar-resource`: `DELETE /calendars/resources/{resourceType}/{id}`

## 9. Services, bookings (the actual reservation against a bookable service)
- `get-service-bookings`: `GET /calendars/services/bookings`, list
- `create-service-booking`: `POST /calendars/services/bookings`
- `get-service-booking-by-id`: `GET /calendars/services/bookings/{bookingId}`
- `update-service-booking`: `PUT /calendars/services/bookings/{bookingId}`
- `delete-service-booking`: `DELETE /calendars/services/bookings/{bookingId}`

## 10. Services, catalog (the service/session type definition, e.g. "Discovery Call", "Group Service Session")
- `get-services-catalog`: `GET /calendars/services/catalog`, list service types
- `create-service-catalog`: `POST /calendars/services/catalog`, new service (name, duration, price, capacity)
- `get-service-catalog-by-id`: `GET /calendars/services/catalog/{serviceId}`
- `update-service-catalog`: `PUT /calendars/services/catalog/{serviceId}`
- `delete-service-catalog`: `DELETE /calendars/services/catalog/{serviceId}`

## 11. Services, locations (venues a service can be delivered at, e.g. consultation room)
- `get-service-locations`: `GET /calendars/services/locations`, list
- `create-service-location`: `POST /calendars/services/locations`
- `get-service-location-by-id`: `GET /calendars/services/locations/{serviceLocationId}`
- `update-service-location`: `PUT /calendars/services/locations/{serviceLocationId}`
- `delete-service-location`: `DELETE /calendars/services/locations/{serviceLocationId}`
