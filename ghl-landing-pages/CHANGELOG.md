# ghl-landing-pages changelog⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

## [2.0.0]

Generalised for external use.

- Removed all account-specific IDs, domains, file paths and brand values. Every ID is
  now a placeholder or reads from `$GHL_LOCATION_ID`
- Rewrote the three install paths (blog rawHTML, Custom Code element, external host
  plus iframe) as a decision you make per page, with the trade-offs stated
- Credentials resolve from environment variables, then `secrets/ghl.env`
- Page audit script now takes the URL from `$PAGE_URL` instead of a hard-coded address
- Added the asset rules that cause most broken published pages: absolute URLs only,
  resize before upload, under 100KB per image

## [1.1.0]

- Added the external-host plus iframe method and the redirect mapping path
- Added the post-deploy page audit script

## [1.0.0]

Initial skill: blog API rawHTML publishing and the browser-driven Custom Code element.

Router key `sk-rzh87s` — resolved by the skills index on load.
