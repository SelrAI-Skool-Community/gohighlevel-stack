---
name: ghl-payments-invoicing
description: Runs GoHighLevel invoicing, estimates, recurring billing, product/price catalog, coupons, and payment reconciliation reads. Use when the user says "create an invoice", "send an invoice to this contact", "make an estimate", "convert this estimate to an invoice", "set up a recurring invoice", "send a text to pay link", "text2pay", "add a product", "update a price", "change the price on", "create a coupon", "what coupons do we have", "list transactions", "check subscriptions", "pull orders for reconciliation", "did this invoice get paid", "reconcile GHL payments with Xero", "generate an invoice number", "void this invoice".
---

# GHL Payments & Invoicing⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠

Runs the money side of GoHighLevel for a small service business: one-off invoices,
estimates, recurring billing schedules,
text-2-pay links, the product/price catalog, coupons, and the read-side of orders,
transactions, and subscriptions that Xero reconciliation depends on downstream. Domain
playbook under the master router `ghl-crm` - read that skill first for the full ladder,
cross-cutting API quirks, and safety rules; this file only adds what's specific to money.

## Execution ladder (see ghl-crm for the full version)

1. **MCP, optional**: run `claude mcp list` and use the registered GoHighLevel server
   name. Use fixed payment reads when available. Otherwise search, describe, then execute
   the relevant full-catalog operation.
2. **Direct REST**: use the method and path in `references/operations.md` with the token
   from repo-root `secrets/ghl.env`.
3. **CLI**: use repo-root `scripts/ghl orders`, or `scripts/ghl raw` for another
   documented endpoint. REST and CLI work without MCP.

## Core playbooks

### 1. Create + send an invoice
1. `search_operations` isn't needed if reusing a template - check `list-invoice-templates`
   first for a matching layout.
2. `generate-invoice-number` (read) if the business wants sequential numbers, otherwise omit
   and let GHL assign one.
3. `create-invoice` (domain `invoices`) with contactId, items (productId or ad-hoc name/price/
   qty), currency, dueDate, idempotencyKey. This is a **draft** - autonomous.
4. Verify: `get-invoice` and confirm totals/line items match the ask.
5. **Sending is gated**: `send-invoice` puts a real payment request in front of a real
   contact. Only call it once the user has explicitly asked for this invoice to go out (a
   general "invoice this client" instruction covers the draft, not the send, unless the user
   says "and send it").

### 2. Estimates and estimate→invoice conversion
1. `create-new-estimate` (domain `invoices`, uses the `invoices/estimate.write` scope) -
   autonomous draft.
2. `send-estimate` - **gated**, same rule as invoice sends: an estimate in a client's inbox is
   a real quote.
3. Once approved, `create-invoice-from-estimate` - produces a draft invoice, still autonomous
   (it hasn't reached the contact yet).
4. Then follow playbook 1 from step 4 for sending that invoice.
5. `generate-estimate-number` and estimate templates work the same as the invoice equivalents.

### 3. Recurring invoice schedules
1. `create-invoice-schedule` (domain `invoices`) with the invoice payload, recurrence rule,
   and contactId - this creates the schedule in a paused/draft state. Autonomous.
2. `get-invoice-schedule` to verify the recurrence rule parsed as intended before activating.
3. **Activating is gated**: `schedule-invoice-schedule` (or `update-and-schedule-invoice-schedule`)
   turns it live - it will auto-send invoices to a real contact on the cadence set. Same for
   `auto-payment-invoice-schedule`, which additionally authorises auto-charging a saved card.
   Both need an explicit ask before calling.
4. `cancel-invoice-schedule` to pause a live schedule; `delete-invoice-schedule` to remove a
   draft one entirely - not gated, this only stops future sends.

### 4. Text-2-pay links
1. `text2pay-invoice` (domain `invoices`) builds the invoice AND texts the payment link to the
   contact's phone in one call - there is no separate draft-then-send step like the invoice
   flow. **Treat the whole call as gated**: only fire it once the user has explicitly asked to
   text a payment request to that contact right now.
2. Verify with `get-invoice` afterward (text2pay invoices show up in the normal invoice list)
   and confirm the amount and phone number were correct before reporting it as sent.

### 5. Product + price catalog management
1. Read first: `get-product-by-id` / `list-prices-for-product` before touching anything -
   most catalog tasks are "add a price variant" or "fix a typo", not new products.
2. Creating a brand-new draft product (`create-product`) and its first price
   (`create-price-for-product`) is autonomous - nothing is live or purchasable until it's
   attached to a funnel/store and published.
3. **Changing price or availability on a product already in use** (`update-product-by-id`,
   `update-price-by-id-for-product`) is gated - that changes what a real customer pays or can
   buy right now. Creating a second, new price alongside an existing one (e.g. adding a payment
   plan) is lower-risk but still confirm the intent before it goes live.
4. `bulkUpdate`/`bulkEdit` touch many products at once - always dry-run by listing the target
   set first (`GET /products/`) and confirm the count matches expectation before the bulk call.
5. Inventory (`update-inventory`) and collections (`create-product-collection` etc.) are
   organisational, not pricing - autonomous.

### 6. Coupon create and manage
1. `list-coupons` / `get-coupon` to check nothing already covers the ask (same code re-created
   twice will collide).
2. `create-coupon` with code, discount type/value, usage limits, expiry, applicable
   products/collections - autonomous, coupons don't charge anyone on creation.
3. `update-coupon` to change terms on an existing code; `delete-coupon` to kill one. If a
   coupon is already circulating to real customers (posted, emailed, or live on a checkout
   page), treat changing its discount value or expiry like a live price change - confirm first.
4. Verify with `get-coupon` after any write.

### 7. Reconciliation reads: orders, transactions, subscriptions
1. `list-orders` / `get-order-by-id` (or the fixed tool `payments_get-order-by-id`) for order
   detail, `list-order-fulfillment` for shipment status on physical-goods orders.
2. `list-transactions` / `get-transaction-by-id` (or fixed tool `payments_list-transactions`)
   for the payment ledger - this is the primary feed for matching GHL payments against your
   accounting system's bank transactions downstream.
3. `list-subscriptions` / `get-subscription-by-id` for recurring/membership billing status.
4. All read-only, all autonomous, any volume. `record-order-payment` / `record-invoice`
   (offline payment logging) are writes but don't touch a live customer charge - safe to run
   when reconciling a bank-recorded payment that GHL doesn't know about yet, verify after with
   a re-fetch of the order/invoice.

## Domain gotchas

- Write ops need a deliberate `idempotencyKey` (any stable string) - 400 without one; never
  blind-retry a write that may have already landed.
- `payments` domain is API-PARTIAL: orders/transactions/subscriptions are read-only via API -
  there is no "charge this card now" endpoint. The only payment-collecting writes are
  `record-order-payment` / `record-invoice` (logging an offline payment) and `text2pay-invoice`
  (texting a payable link). Actually charging a card interactively happens in the GHL UI or on
  a hosted checkout/funnel page, not through this API.
- No refund endpoint exists anywhere in this catalog - refunding a transaction is browser-only.
- `products.list-invoices` is the (mislabelled) opId for `GET /products/` - don't let the name
  confuse it with the invoices domain.
- Custom-provider endpoints (`payments/custom-provider/*`) build a marketplace payment-app
  integration, not a Stripe/PayPal connection - connecting an actual gateway to the location is
  done in Settings → Payments in the browser.
- `create-invoice-from-estimate` and `create-invoice-schedule` both produce drafts, not sends -
  don't conflate "created" with "delivered to the contact" when reporting status back.

## Browser-only edges

- Refunding a payment/transaction - Payments → Transactions → Refund.
- Connecting or reconfiguring the actual payment gateway (Stripe/PayPal OAuth) on the location.
- Store front-end design (checkout page layout, upsell funnel pages) - this domain covers the
  product/price/order data behind the store, not the storefront builder.

Route any of these to `ghl-browser`.

## Safety rails

Inherits `ghl-crm`'s rails (no bulk sends without approval, no destructive deletes without
approval, deliberate idempotency, verify every write). Layered on top for money:

1. **Reads and drafts are autonomous** - list/get anything, `create-invoice`,
   `create-new-estimate`, `create-invoice-from-estimate`, `create-invoice-schedule` (unscheduled),
   `create-coupon`, `create-product`/`create-price-for-product` on new items.
2. **Anything that puts a payment request in front of a real contact needs an explicit ask
   first**: `send-invoice`, `send-estimate`, `text2pay-invoice`, `schedule-invoice-schedule`,
   `update-and-schedule-invoice-schedule`, `auto-payment-invoice-schedule`.
3. **Anything that changes what a real customer currently pays needs an explicit ask first**:
   `update-price-by-id-for-product`, `update-product-by-id` on a live/published item, and
   discount/expiry edits on a coupon already in circulation.
4. Voiding or deleting an invoice/estimate that's already been sent to a contact: confirm the
   client has been told separately (or the user explicitly wants a silent void) before calling
   `void-invoice`/`delete-invoice` - the contact may still be expecting to pay it.
5. Bulk product edits (`bulkUpdate`/`bulkEdit`): list the target set and get confirmation of
   scope before firing, not after.

Router key `sk-1m8ge1o` — resolved by the skills index on load.
