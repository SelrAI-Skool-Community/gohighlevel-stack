# Worked example: ghl-landing-pages session⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

An end-to-end run across all three page-install paths. Company names, IDs and domains
are examples. Assume `GHL_LOCATION_ID` and `GHL_API_KEY` are set.

---

## 1. Publish a new page through the blog API

```
User: Build me a landing page for the service consultation offer and publish it.
```

Claude checks which blog site and author exist in the location:

```
blogs_get-blogs  locationId=$GHL_LOCATION_ID
→ [{ _id: "<blogId>", name: "Main site" }]

blogs_get-all-blog-authors-by-location  locationId=$GHL_LOCATION_ID
→ [{ _id: "<authorId>", name: "Sample Co" }]
```

Claude drafts the HTML locally, previews it at `http://localhost:8888`, then publishes:

```
blogs_create-blog-post
  body_title:        "Service Consultation Quote"
  body_locationId:   $GHL_LOCATION_ID
  body_blogId:       "<blogId>"
  body_rawHTML:      "<html>...</html>"
  body_status:       "PUBLISHED"
  body_urlSlug:      "service-consultation-quote"
  body_description:  "Book a 45-minute service consultation and receive a written quote."
  body_imageUrl:     "https://cdn.example.com/service-team.jpg"
  body_imageAltText: "Service team preparing for a consultation"
  body_author:       "<authorId>"
```

Result:

- Live at `yourdomain.com/blog/service-consultation-quote`
- Audit run with `PAGE_URL=https://yourdomain.com/blog/service-consultation-quote`:
  0 broken links, 0 broken images, 0 em dashes, no mobile overflow
- A test form submission created a contact in GHL, verified by searching for it

---

## 2. Update the copy on a published page

```
User: Change the headline to lead with the 45-minute consultation, not the price.
```

Claude edits the local HTML, reruns the local preview, then:

```
blogs_update-blog-post
  blogId:      "<blogId>"
  requestBody: { rawHTML: "<html>...</html>" }
```

Then re-runs the audit and opens the live URL to confirm the new headline rendered.

**Note:** the update call replaces the whole `rawHTML`. Always edit the local source
file and push the full document. Never hand-patch what is live.

---

## 3. Put a hand-built page inside a real funnel

```
User: The checkout page needs to look like our own design, not the GHL builder.
```

The checkout page is wired to GHL payments, so it has to stay a funnel page. That rules
out the blog method. Claude picks the iframe approach because the page will be iterated
on:

1. Deploy the HTML to a static host, giving `https://checkout-page.example.com`
2. In GHL: Funnel → the checkout page → Settings → Header Tracking Code
3. Paste the iframe injection block from `../SKILL.md`, Method 3, with `src` set to that URL
4. Save, publish, hard-refresh the live page

Result:

- The GHL funnel URL is unchanged, so payment wiring and tracking still work
- The page renders the custom design full-viewport
- Future edits are: edit the HTML, redeploy to the host. GHL is never touched again

---

## 4. Point a clean path at an external page

```
User: I want yourdomain.com/quote to go to the hosted quote page.
```

```
execute_operation
  operationId: "create-redirect"
  locationId:  $GHL_LOCATION_ID
  path:        "/quote"
  target:      "https://checkout-page.example.com"
  action:      "url"
```

Result: `yourdomain.com/quote` 301-redirects. The address bar changes to the external
URL. If that matters for branding, use the iframe method from section 3 instead.

---

## What went wrong along the way

- **First publish showed a broken image.** The HTML referenced `assets/service-team.jpg`,
  a local path. Fixed by uploading to the media library and using the absolute URL
- **The Custom Code element was framed by GHL chrome** until the Header Code CSS
  override was pasted
- **A redeploy appeared to do nothing.** The GHL page had cached the iframe. One
  hard-refresh fixed it

Router key `sk-rzh87s` — resolved by the skills index on load.
