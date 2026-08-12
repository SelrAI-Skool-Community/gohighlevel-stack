# ghl-payments-invoicing - operation catalog (103 ops, reorganised by business task)

Source domains: `invoices` (37), `products` (27), `payments` (22), `store` (17). Use the
registered GoHighLevel MCP server, direct REST, or repo-root `scripts/ghl raw`. The domain
field below is used by full-catalog MCP operations.

## 1. Invoice lifecycle (create → send → collect → close)

- `GET /invoices/` - `invoices.list-invoices` | invoices.readonly | read
- `POST /invoices/` - `create-invoice` | invoices.write | write
- `GET /invoices/generate-invoice-number` - `generate-invoice-number` | invoices.readonly | read
- `GET /invoices/{invoiceId}` - `get-invoice` | invoices.readonly | read
- `PUT /invoices/{invoiceId}` - `update-invoice` | invoices.write | write
- `POST /invoices/{invoiceId}/send` - `send-invoice` | invoices.write | write - **sends to the real contact, gated**
- `POST /invoices/{invoiceId}/record-payment` - `record-invoice` | invoices.write | write - logs an offline/manual payment
- `POST /invoices/{invoiceId}/void` - `void-invoice` | invoices.write | write
- `DELETE /invoices/{invoiceId}` - `delete-invoice` | invoices.write | delete
- `GET /invoices/settings` - `get-invoice-settings` | invoices.readonly | read
- `POST /invoices/text2pay` - `text2pay-invoice` | invoices.write | write - **creates + texts a payable link, gated**

## 2. Invoice templates

- `GET /invoices/template` - `list-invoice-templates` | invoices/template.readonly | read
- `POST /invoices/template` - `create-invoice-template` | invoices/template.write | write
- `GET /invoices/template/{templateId}` - `get-invoice-template` | invoices/template.readonly | read
- `PUT /invoices/template/{templateId}` - `update-invoice-template` | invoices/template.write | write
- `DELETE /invoices/template/{templateId}` - `delete-invoice-template` | invoices/template.write | delete

## 3. Estimates & estimate→invoice conversion

- `GET /invoices/estimate/list` - `list-estimates` | invoices/estimate.readonly | read
- `POST /invoices/estimate` - `create-new-estimate` | invoices/estimate.write | write
- `GET /invoices/estimate/number/generate` - `generate-estimate-number` | invoices/estimate.readonly | read
- `PUT /invoices/estimate/{estimateId}` - `update-estimate` | invoices/estimate.write | write
- `POST /invoices/estimate/{estimateId}/send` - `send-estimate` | invoices/estimate.write | write - **sends to the real contact, gated**
- `POST /invoices/estimate/{estimateId}/invoice` - `create-invoice-from-estimate` | invoices/estimate.write | write - produces a draft invoice, not sent yet
- `DELETE /invoices/estimate/{estimateId}` - `delete-estimate` | invoices/estimate.write | delete
- `GET /invoices/estimate/template` - `list-estimate-templates` | invoices/estimate.readonly | read
- `POST /invoices/estimate/template` - `create-estimate-template` | invoices/estimate.write | write
- `GET /invoices/estimate/template/preview` - `preview-estimate-template` | invoices/estimate.readonly | read
- `PUT /invoices/estimate/template/{templateId}` - `update-estimate-template` | invoices/estimate.write | write
- `DELETE /invoices/estimate/template/{templateId}` - `delete-estimate-template` | invoices/estimate.write | delete

## 4. Recurring invoice schedules

- `GET /invoices/schedule` - `list-invoice-schedules` | invoices/schedule.readonly | read
- `POST /invoices/schedule` - `create-invoice-schedule` | invoices/schedule.write | write - draft schedule, not live yet
- `GET /invoices/schedule/{scheduleId}` - `get-invoice-schedule` | invoices/schedule.readonly | read
- `PUT /invoices/schedule/{scheduleId}` - `update-invoice-schedule` | invoices/schedule.write | write
- `POST /invoices/schedule/{scheduleId}/schedule` - `schedule-invoice-schedule` | invoices/schedule.write | write - **activates recurring sends, gated**
- `POST /invoices/schedule/{scheduleId}/updateAndSchedule` - `update-and-schedule-invoice-schedule` | invoices/schedule.write | write - **activates recurring sends, gated**
- `POST /invoices/schedule/{scheduleId}/auto-payment` - `auto-payment-invoice-schedule` | invoices/schedule.write | write - **turns on auto-charging a saved card, gated**
- `POST /invoices/schedule/{scheduleId}/cancel` - `cancel-invoice-schedule` | invoices/schedule.write | write
- `DELETE /invoices/schedule/{scheduleId}` - `delete-invoice-schedule` | invoices/schedule.write | delete

## 5. Product + price catalog management

- `GET /products/` - `products.list-invoices` | products.readonly | read
- `POST /products/` - `create-product` | products.write | write
- `PUT /products/{productId}` - `update-product-by-id` | products.write | write - **price/availability change on a live product, gated**
- `DELETE /products/{productId}` - `delete-product-by-id` | products.write | delete
- `GET /products/{productId}` - `get-product-by-id` | products.readonly | read
- `POST /products/bulk-update` - `bulkUpdate` | products.write | write
- `POST /products/bulk-update/edit` - `bulkEdit` | products.write | write
- `GET /products/{productId}/price` - `list-prices-for-product` | products/prices.readonly | read
- `POST /products/{productId}/price` - `create-price-for-product` | products/prices.write | write
- `GET /products/{productId}/price/{priceId}` - `get-price-by-id-for-product` | products/prices.readonly | read
- `PUT /products/{productId}/price/{priceId}` - `update-price-by-id-for-product` | products/prices.write | write - **live price change, gated**
- `DELETE /products/{productId}/price/{priceId}` - `delete-price-by-id-for-product` | products/prices.write | delete
- `GET /products/inventory` - `get-list-inventory` | products/prices.readonly | read
- `POST /products/inventory` - `update-inventory` | products/prices.write | write
- `GET /products/collections` - `get-product-collection` | products/collection.readonly | read
- `POST /products/collections` - `create-product-collection` | products/collection.write | write
- `GET /products/collections/{collectionId}` - `get-product-collection-id` | products/collection.readonly | read
- `PUT /products/collections/{collectionId}` - `update-product-collection` | products/collection.write | write
- `DELETE /products/collections/{collectionId}` - `delete-product-collection` | products/collection.write | delete
- `GET /products/reviews` - `get-product-reviews` | products.readonly | read
- `GET /products/reviews/count` - `get-reviews-count` | products.readonly | read
- `PUT /products/reviews/{reviewId}` - `update-product-review` | products.write | write
- `POST /products/reviews/bulk-update` - `bulk-update-product-review` | products.write | write
- `DELETE /products/reviews/{reviewId}` - `delete-product-review` | products.write | delete
- `POST /products/store/{storeId}` - `update-store-status` | products.write | write
- `POST /products/store/{storeId}/priority` - `update-display-priority` | products.write | write
- `GET /products/store/{storeId}/stats` - `get-product-store-stats` | products.readonly | read

## 6. Coupons

- `GET /payments/coupon/list` - `list-coupons` | payments/coupons.readonly | read
- `GET /payments/coupon` - `get-coupon` | payments/coupons.readonly | read
- `POST /payments/coupon` - `create-coupon` | payments/coupons.write | write
- `PUT /payments/coupon` - `update-coupon` | payments/coupons.write | write
- `DELETE /payments/coupon` - `delete-coupon` | payments/coupons.write | delete

## 7. Orders, transactions, subscriptions (reconciliation reads)

- `GET /payments/orders` - `list-orders` | payments/orders.readonly | read
- `GET /payments/orders/{orderId}` - `get-order-by-id` | payments/orders.readonly | read (may be a fixed MCP operation)
- `GET /payments/orders/{orderId}/fulfillments` - `list-order-fulfillment` | payments/orders.readonly | read
- `POST /payments/orders/{orderId}/fulfillments` - `create-order-fulfillment` | payments/orders.write | write
- `POST /payments/orders/{orderId}/record-payment` - `record-order-payment` | payments/orders.collectPayment | write - logs an offline/manual payment against an order
- `GET /payments/transactions` - `list-transactions` | payments/transactions.readonly | read (may be a fixed MCP operation)
- `GET /payments/transactions/{transactionId}` - `get-transaction-by-id` | payments/transactions.readonly | read
- `GET /payments/subscriptions` - `list-subscriptions` | payments/subscriptions.readonly | read
- `GET /payments/subscriptions/{subscriptionId}` - `get-subscription-by-id` | payments/subscriptions.readonly | read

No refund endpoint exists in this catalog slice - issuing a refund on a transaction is
browser-only (Payments → Transactions → Refund in the GHL UI).

## 8. Custom payment providers & integration whitelabel (rare, marketplace-app-only)

- `GET /payments/custom-provider/connect` - `fetch-config` | payments/custom-provider.readonly | read
- `POST /payments/custom-provider/connect` - `create-config` | payments/custom-provider.write | write
- `POST /payments/custom-provider/disconnect` - `disconnect-config` | payments/custom-provider.write | write
- `POST /payments/custom-provider/provider` - `create-integration` | payments/custom-provider.write | write
- `DELETE /payments/custom-provider/provider` - `delete-integration` | payments/custom-provider.write | delete
- `PUT /payments/custom-provider/capabilities` - `custom-provider-marketplace-app-update-capabilities` | payments/custom-provider.write | write
- `GET /payments/integrations/provider/whitelabel` - `list-integration-providers` | payments/integration.readonly | read
- `POST /payments/integrations/provider/whitelabel` - `create-integration provider` | payments/integration.write | write

These build a marketplace payment-processor integration. They do NOT connect Stripe/PayPal
in the location's Settings → Payments screen - that connection is browser-only (OAuth on the
gateway's own site).

## 9. Store shipping & settings

- `GET /store/shipping-carrier` - `list-shipping-carriers` | store/shipping.readonly | read
- `POST /store/shipping-carrier` - `create-shipping-carrier` | store/shipping.write | write
- `GET /store/shipping-carrier/{shippingCarrierId}` - `get-shipping-carriers` | store/shipping.readonly | read
- `PUT /store/shipping-carrier/{shippingCarrierId}` - `update-shipping-carrier` | store/shipping.write | write
- `DELETE /store/shipping-carrier/{shippingCarrierId}` - `delete-shipping-carrier` | store/shipping.write | delete
- `GET /store/shipping-zone` - `list-shipping-zones` | store/shipping.readonly | read
- `POST /store/shipping-zone` - `create-shipping-zone` | store/shipping.write | write
- `GET /store/shipping-zone/{shippingZoneId}` - `get-shipping-zones` | store/shipping.readonly | read
- `PUT /store/shipping-zone/{shippingZoneId}` - `update-shipping-zone` | store/shipping.write | write
- `DELETE /store/shipping-zone/{shippingZoneId}` - `delete-shipping-zone` | store/shipping.write | delete
- `GET /store/shipping-zone/{shippingZoneId}/shipping-rate` - `list-shipping-rates` | store/shipping.readonly | read
- `POST /store/shipping-zone/{shippingZoneId}/shipping-rate` - `create-shipping-rate` | store/shipping.write | write
- `GET /store/shipping-zone/{shippingZoneId}/shipping-rate/{shippingRateId}` - `get-shipping-rates` | store/shipping.readonly | read
- `PUT /store/shipping-zone/{shippingZoneId}/shipping-rate/{shippingRateId}` - `update-shipping-rate` | store/shipping.write | write
- `DELETE /store/shipping-zone/{shippingZoneId}/shipping-rate/{shippingRateId}` - `delete-shipping-rate` | store/shipping.write | delete
- `GET /store/store-setting` - `get-store-settings` | store/setting.readonly | read
- `POST /store/store-setting` - `create-store-setting` | store/setting.write | write
