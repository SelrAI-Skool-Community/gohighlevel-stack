---
name: ghl-landing-pages
description: Build, edit, and publish GoHighLevel landing pages, funnel pages, sales pages and blog pages programmatically. Use when the user says "build a GHL landing page", "edit my GHL funnel", "publish a new page", "add a form to my landing page", "deploy a landing page", "swap the headline on the funnel", or any GHL page build, edit or deploy operation. Drives three install paths (Blog API rawHTML, browser-driven Custom Code element, external host plus iframe) so it can ship pages even though GHL has no public funnel-page API. Pairs with ghl-browser for UI-only operations and ghl-crm for contact and form wiring.
---

# GHL landing pages⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Build and manage landing pages in GoHighLevel with full HTML control, without the
drag-and-drop builder.

## When to use

- Building a landing page, quote-request page or sales page in GHL
- Editing the copy, styling or structure of an existing page
- Deploying a hand-written HTML page to a GHL-connected domain
- Auditing a live page before you send traffic to it

## The one thing to know first

**GHL has no public API for funnel page content.** You cannot create or edit a funnel
page body with a REST call. Three methods work instead, in this order of preference.

### Method 1 — Blog API with rawHTML (fully programmatic, start here)

The blog endpoints accept a complete HTML document in the `rawHTML` field, including
inline CSS and scripts. Blog posts publish to a live URL on the connected domain, and
you get full create, read, update and delete through the API.

- URL pattern: `yourdomain.com/blog/<url-slug>`
- Requires a blog site to already exist in the location (create one in the UI once)
- Tools: `mcp__ghl__blogs_create-blog-post` / `blogs_update-blog-post`, or the REST
  helper. Anything missing goes through the ghl-crm operation catalogue, blogs domain.

Create a page:

```
blogs_create-blog-post
  body_title:        "Bathroom Renovation Quote"
  body_locationId:   "$GHL_LOCATION_ID"
  body_blogId:       "<from the blogs list call>"
  body_rawHTML:      "<html>...</html>"
  body_status:       "PUBLISHED"
  body_urlSlug:      "renovation-quote"
  body_description:  "Page description used for SEO"
  body_imageUrl:     "https://<your CDN or GHL media URL>"
  body_imageAltText: "Finished bathroom renovation"
  body_categories:   []
  body_author:       "<author id from the authors list call>"
  body_publishedAt:  "2026-01-01T00:00:00.000Z"
```

Update a page:

```
blogs_update-blog-post
  blogId:      "<blog id>"
  requestBody: { rawHTML: "<html>...</html>" }
```

### Method 2 — Custom Code element in the funnel builder (browser lane)

When the page has to live at a funnel URL rather than a blog URL, drive the builder
through the browser. See the ghl-browser skill for the engine and the login flow.

1. Navigate to `app.gohighlevel.com/location/<locationId>/page-builder/<pageId>`
2. Wait 15 to 20 seconds. The builder is a heavy single-page app and loads slowly
3. Add Section → Row → Column → Custom Code element
4. Double-click the Custom Code element to open the editor
5. Paste the full HTML
6. Page Settings → Header Code → paste the CSS override below
7. Save, then publish

CSS override that hides the GHL wrapper and makes your code full-viewport:

```html
<style>
  .hl_page-preview--content > *:not(.custom-code-container) { display: none !important; }
  .custom-code-container {
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh; z-index: 9999;
  }
</style>
```

### Method 3 — External host, GHL loads it

Host the HTML anywhere static (Vercel, Cloudflare Pages, Netlify, S3) and have GHL
point at it. Two ways:

- **Redirect.** Create a GHL redirect mapping a path to the external URL with the
  funnels-domain `create-redirect` operation, `action: "url"`. This is a 301, so the
  address bar changes to the external URL. Fine for internal pages, bad for branding.
- **Iframe injection.** Paste this into the funnel page's Header Tracking Code. The GHL
  page content is hidden and your hosted page fills the viewport, so the address bar
  keeps the GHL domain:

```html
<style>
  body, html { margin:0; padding:0; overflow:hidden; height:100vh }
  #page-builder-container, #page-builder-container > *,
  .hl_page-preview--content, .hl_page-preview--content > * { display:none !important }
  #page-frame {
    display:block !important; position:fixed; top:0; left:0;
    width:100vw; height:100vh; z-index:99999; border:none;
  }
</style>
<iframe id="page-frame" src="https://your-page.example.com"></iframe>
```

Once that is in place you never touch GHL again. Edit the HTML, redeploy to the host,
and the iframe picks up the new version.

**The trade-off, plainly.** Method 1 is the only one a script can do end to end, but
the page lives on a `/blog/` URL. Method 3 gives you the nicest workflow and the
cleanest URL but adds a second thing to host and pay for. Method 2 keeps everything
inside GHL but needs a browser session every time. Pick once per page and write it
down, because a page built one way cannot be edited another way.

## Working on the HTML

Keep the source HTML in your project folder, not in GHL. GHL holds the published copy;
your repo holds the truth.

1. Read and edit the local file with the normal file tools
2. Preview locally: `python3 -m http.server 8888` then open
   `http://localhost:8888/your-page.html`
3. Deploy by whichever of the three methods that page uses

If you deploy to an external host, keep assets alongside the page and copy both:

```bash
mkdir -p /tmp/page-deploy
cp your-page.html /tmp/page-deploy/index.html
cp -r assets /tmp/page-deploy/assets
cd /tmp/page-deploy && npx -y vercel deploy --prod --yes
```

## Assets

- Upload images to the GHL media library with a multipart `POST /medias/upload-file`,
  or to your own CDN. Either way the HTML must reference **absolute** URLs, never
  local paths, or the published page will show broken images
- Resize before uploading. Max 1200px wide for photos, JPEG at about 80% quality
- Target: every image under 100KB, whole page under 200KB
- Resize on a Mac without extra tools: `sips -Z 1200 photo.jpg --out photo.jpg`

## Custom domain

If you host externally and want a branded subdomain:

1. `npx -y vercel domains add pages.yourdomain.com`
2. Vercel returns a CNAME record
3. Add that CNAME wherever your DNS is managed
4. `npx -y vercel domains verify pages.yourdomain.com`
5. If the page is loaded by iframe from GHL, update the iframe `src` to the new domain

## Page audit before you send traffic

Never announce a page you have not looked at. Run this after every deploy, then open
the page yourself on a phone.

```bash
node << 'SCRIPT'
const { chromium } = require('playwright');
const URL = process.env.PAGE_URL;           // set PAGE_URL before running
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);

  const allText = await page.evaluate(() => document.body.innerText);
  const links = await page.evaluate(() => [...document.querySelectorAll('a')]
    .map(a => ({ href: a.href, broken: !a.href || a.href === '#' || a.href.startsWith('javascript:') })));
  const images = await page.evaluate(() => [...document.querySelectorAll('img')]
    .map(i => ({ src: i.src, loaded: i.complete && i.naturalWidth > 0 })));

  console.log('LINKS  :', links.filter(l => l.broken).length, 'broken of', links.length);
  console.log('IMAGES :', images.filter(i => !i.loaded).length, 'broken of', images.length);
  console.log('DASHES :', (allText.match(/[–—]/g) || []).length, 'em/en dashes');

  await page.setViewportSize({ width: 390, height: 844 });
  await page.waitForTimeout(500);
  const overflow = await page.evaluate(() => document.body.scrollWidth > window.innerWidth);
  console.log('MOBILE OVERFLOW:', overflow ? 'YES (fix this)' : 'no');

  await browser.close();
})();
SCRIPT
```

Then check by eye, because the script cannot:

- Every call-to-action button goes where you think it goes. Click one
- The form actually creates a contact in GHL. Submit a test and look for it
- The page reads like your business wrote it, not like a template

## Copy rules that keep a page selling

- One idea per section, one clear next step per page
- Lead with the customer's problem, not your company history
- Use the words your customers use. If they say "reno", do not write "renovation
  solution"
- Avoid filler: "unlock", "leverage", "cutting-edge", "game-changer", "revolutionise",
  "seamless", "empower"
- Never promise an outcome, a refund or a support level you have not agreed to deliver
- Keep jargon out. No API, MCP, terminal or deployment language on a customer page

## Authentication and routing

Route every API call down the ghl-crm ladder: fixed MCP tools first, then the operation
catalogue, then the REST helper (`scripts/ghl`, credentials in `secrets/ghl.env`), then
the browser lane. The capability matrix in `ghl-crm/references/capability-matrix.md` is
the routing truth for what funnels and forms can never do through the API.

Browser sessions, login and two-factor handling all live in the ghl-browser skill. GHL
pages take 10 to 20 seconds to load, so use generous timeouts and never close the
browser mid-run.

Router key `sk-rzh87s` — resolved by the skills index on load.
