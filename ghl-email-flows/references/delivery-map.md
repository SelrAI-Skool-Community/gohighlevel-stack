# Delivery map

## Truth layers

Decide these once, write them down, and never let them drift.

| Layer | Where it lives | The contract |
|---|---|---|
| Copy baseline | The approved copy document or meeting notes | Use the approved words. Do not improve them on the way through |
| Design masters | A folder in your own project repo, one per chain | The builder script and the HTML preserve merge tags and support cloning |
| Review | The rendered previews a human actually looked at | The approved render defines what should be live |
| Delivery | Live GHL workflows, in the location set in `secrets/ghl.env` | This is what customers receive. It gets corrected to match the review, never the reverse |
| Brand | Your colour, type and footer values, held in one place | Load them from that source; never retype a hex code from memory |

The loop is: build → render → a person reviews → an authorised person ships to GHL.
Nobody skips the middle two steps because the copy "only changed slightly".

## Build recipe

1. **Ground the copy.** Take the approved document verbatim. Run the compliance pass:
   no em dashes, no outcome guarantees, no refund or support promises, no invented
   proof. Reviews and testimonials use first names only unless you hold a written
   release
2. **Build from the master.** Clone the chain's builder script rather than starting
   fresh. Preserve `{{contact.first_name}}`, any `{{custom_values.*}}` tags, and
   `{{unsubscribe_link}}`. Apply the locked footer
3. **Host the assets in GHL.** Upload photos, icons and logos with a multipart
   `POST /medias/upload-file` and reference the returned CDN URLs. Local paths and
   `file://` references arrive broken
4. **Review visually.** Render the preview HTML, screenshot it light and dark, and read
   it against the approved copy side by side
5. **Get a yes from a person** before anything touches a live workflow

## SMS and variants

SMS bodies, wait times and Active/Disabled statuses live in workflow steps, which means
the browser lane. Keep documented statuses as they are unless the change is the point.

Match each SMS to the email it sits beside: short lines, one link, and the same ask.
A different ask in the SMS than in the email confuses people into doing neither.

When cloning a chain for a second location, region or season, drive the differences
through custom values rather than by editing copy in five places:

- `<variant>_date_short`
- `<variant>_venue` or `<variant>_service_area`
- `<variant>_maps_link`
- `<variant>_payment_link`
- `<variant>_landing_page`

Swap the naming in subjects and body copy, and keep everything else identical. If two
clones diverge structurally they stop being clones, and you now maintain two chains.

## Campaign craft

The design master gives you the shell, not the sequence.

1. Read the offer or service detail first: what is being sold, at what price, to whom
2. One idea and one call to action per email. Body under 200 words where you can. A PS
   line every time, because it is the second most-read thing in the email
3. Subject lines that state the value plainly beat clever ones often enough that plain
   is the control. Test against it, do not assume you have beaten it
4. Match the arc to the job. A launch: announce, story, close, over about seven days.
   A nurture: lead with the customer's problem and earn the ask

## Release evidence

Do not call a flow shipped without all of this:

- The render matches the approved copy, word for word
- The compliance pass is clean
- Merge tags and custom values survived the build
- Every asset is on a hosted URL and loads
- Both light and dark screenshots were viewed by a person
- The API `previewUrl` for every pushed template was opened and looked at
- Workflow steps were updated in the browser and re-read afterwards
- A test send was opened on a real phone, in dark mode
