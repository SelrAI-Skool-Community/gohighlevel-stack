# Ad Manager operations, by business task

Domain: `ad-publishing` (95 ops). All scopes are `adPublishing.readonly` (read) or
`adPublishing.write` (write/delete). Use `describe_operation {operationId, domain:
"ad-publishing"}` for the exact param/body schema before the first use of any op. Several
opId names don't match their path 1:1 (see SKILL.md gotchas).

## 1. Connection and account audit

| Task | Method / Path | opId | Kind |
|---|---|---|---|
| Facebook app connection status | GET `/ad-publishing/facebook/integration` | `fb-get-integration` | read |
| Connect Facebook (after browser OAuth) | POST `/ad-publishing/facebook/integration` | `fb-create-integration` | write |
| Disconnect Facebook | DELETE `/ad-publishing/facebook/integration` | `fb-delete-integration` | delete |
| List Facebook ad accounts | GET `/ad-publishing/facebook/ad-accounts` | `fb-get-ad-accounts` | read |
| Get one Facebook ad account | GET `/ad-publishing/facebook/ad-accounts/{adAccountId}` | `fb-get-ad-account` | read |
| Remove a Facebook ad account | DELETE `/ad-publishing/facebook/ad-accounts/{adAccountId}` | `fb-delete-ad-account` | delete |
| Connected Facebook Pages | GET `/ad-publishing/facebook/pages` | `fb-get-pages` | read |
| Set default Page | PUT `/ad-publishing/facebook/page/default` | `fb-set-default-page` | write |
| Remove a Page | DELETE `/ad-publishing/facebook/page` | `fb-delete-page` | delete |
| Instagram accounts linked to a Page | GET `/ad-publishing/facebook/page/{pageId}/instagram` | `fb-get-instagram-accounts` | read |
| Connected pixels | GET `/ad-publishing/facebook/pixels` | `fb-get-pixels` | read |
| Create/update a pixel | PUT `/ad-publishing/facebook/pixels` | `fb-upsert-pixel` | write |
| Current FB user identity | GET `/ad-publishing/facebook/me` | `fb-get-current-user` | read |
| Connected business entity | GET `/ad-publishing/facebook/entity` | `fb-get-entity` | read |
| Google connection status | GET `/ad-publishing/google/integration` | `google-get-integration` | read |
| Connect Google | POST `/ad-publishing/google/integration` | `google-create-integration` | write |
| List Google ad accounts | GET `/ad-publishing/google/ad-accounts` | `google-get-ad-accounts` | read |
| Get one Google ad account | GET `/ad-publishing/google/ad-accounts/{adAccountId}` | `google-get-ad-account-details` | read |
| Remove a Google ad account | DELETE `/ad-publishing/google/ad-accounts/{adAccountId}` | `google-delete-ad-account` | delete |
| Current Google user identity | GET `/ad-publishing/google/me` | `google-get-current-user` | read |
| Connected Google entity | GET `/ad-publishing/google/entity` | `google-get-entity` | read |
| LinkedIn connection status | GET `/ad-publishing/linkedin/integration` | `li-get-integration` | read |
| Connect LinkedIn | POST `/ad-publishing/linkedin/integration` | `li-create-integration` | write |
| List LinkedIn ad accounts | GET `/ad-publishing/linkedin/ad-accounts` | `li-get-ad-accounts` | read |
| Get one LinkedIn ad account | GET `/ad-publishing/linkedin/ad-account` | `li-get-ad-account-details` | read |
| Remove LinkedIn ad account | DELETE `/ad-publishing/linkedin/ad-account` | `li-delete-ad-account` | delete |
| Current LinkedIn user identity | GET `/ad-publishing/linkedin/me` | `li-get-current-user` | read |

## 2. Campaign build and launch, Facebook/Instagram

| Task | Method / Path | opId | Kind |
|---|---|---|---|
| Create/update a campaign (draft) | PUT `/ad-publishing/facebook/campaigns` | `fb-upsert-campaign` | write |
| Get a campaign | GET `/ad-publishing/facebook/campaign/{campaignId}` | `fb-get-campaign` | read |
| Delete a campaign | DELETE `/ad-publishing/facebook/campaigns/{campaignId}` | `fb-delete-campaign` | delete |
| Duplicate a campaign | POST `/ad-publishing/facebook/campaigns/{campaignId}/duplicate` | `fb-duplicate-campaign` | write |
| **Publish (first activation)** | POST `/ad-publishing/facebook/campaigns/{campaignId}/publish` | `fb-publish-campaign` | write, gated |
| Publishing progress | GET `/ad-publishing/facebook/campaigns/{campaignId}/publishing-progress` | `fb-get-campaign-publishing-progress` | read |
| Create/update an ad set (draft) | PUT `/ad-publishing/facebook/adsets` | `fb-upsert-adset` | write |
| Delete an ad set | DELETE `/ad-publishing/facebook/adsets/{adSetId}` | `fb-delete-adset` | delete |
| Duplicate an ad set | POST `/ad-publishing/facebook/adsets/{adSetId}/duplicate` | `fb-duplicate-adset` | write |
| Create/update an ad (draft) | PUT `/ad-publishing/facebook/ads` | `fb-upsert-ad` | write |
| Delete an ad | DELETE `/ad-publishing/facebook/ads/{adId}` | `fb-delete-ad` | delete |
| Duplicate an ad | POST `/ad-publishing/facebook/ads/{adId}/duplicate` | `fb-duplicate-ad` | write |
| Targeting/interest search | GET `/ad-publishing/facebook/targeting/search` | `fb-search-targeting` | read |

## 3. Campaign build and launch, Google

| Task | Method / Path | opId | Kind |
|---|---|---|---|
| Create/update a campaign (draft) | PUT `/ad-publishing/google/ads` | `google-upsert-campaign` | write |
| Get a campaign | GET `/ad-publishing/google/ads/{adId}` | `google-get-campaign-by-id` | read |
| **Publish (activation)** | POST `/ad-publishing/google/ads/{adId}/publish` | `google-publish-ad` | write, gated |
| Keyword ideas | POST `/ad-publishing/google/keyword-ideas` | `google-get-keyword-ideas` | read (POST body) |
| Target interests | GET `/ad-publishing/google/target-interests` | `google-get-target-interests` | read |
| Targeting search | GET `/ad-publishing/google/targeting/search` | `google-search-targeting` | read |

## 4. Campaign build and launch, LinkedIn

| Task | Method / Path | opId | Kind |
|---|---|---|---|
| Create/update a campaign group (draft) | PUT `/ad-publishing/linkedin/ads` | `li-upsert-campaign-group` | write |
| Get a campaign group | GET `/ad-publishing/linkedin/ads/{adId}` | `li-get-campaign-group` | read |
| **Publish (activation)** | POST `/ad-publishing/linkedin/ads/{adId}/publish` | `li-publish-campaign-group` | write, gated |
| Update ad status (pause/resume/archive) | PATCH `/ad-publishing/linkedin/{adId}/status` | `li-update-ad-status` | write, resume gated |
| Targeting search | GET `/ad-publishing/linkedin/targeting/search` | `li-search-targeting` | read |

## 5. Pause / resume / duplicate (Facebook only has dedicated lifecycle ops)

| Task | Method / Path | opId | Kind |
|---|---|---|---|
| Pause a campaign | POST `/ad-publishing/facebook/campaigns/{campaignId}/pause` | `fb-pause-campaign` | write, safe |
| Resume a campaign | POST `/ad-publishing/facebook/campaigns/{campaignId}/resume` | `fb-resume-campaign` | write, gated |
| Pause an ad set | POST `/ad-publishing/facebook/adsets/{adSetId}/pause` | `fb-pause-adset` | write, safe |
| Resume an ad set | POST `/ad-publishing/facebook/adsets/{adSetId}/resume` | `fb-resume-adset` | write, gated |
| Pause an ad | POST `/ad-publishing/facebook/ads/{adId}/pause` | `fb-pause-ad` | write, safe |
| Resume an ad | POST `/ad-publishing/facebook/ads/{adId}/resume` | `fb-resume-ad` | write, gated |

Google has no dedicated pause/resume op. Status is a field inside `google-upsert-campaign`;
re-run the upsert with the same ID and a new status. LinkedIn uses `li-update-ad-status`
for every post-publish status change.

## 6. Reporting and analytics (all read-only, no approval needed)

| Task | Method / Path | opId |
|---|---|---|
| Facebook account-level reporting | GET `/ad-publishing/facebook/reporting` | `fb-get-reporting` |
| Facebook campaign reporting | GET `/ad-publishing/facebook/reporting/campaign/{campaignId}` | `fb-get-campaign-reporting` |
| Facebook saved report list | GET `/ad-publishing/facebook/reporting/list` | `fb-get-reporting-list` |
| Google account-level reporting | GET `/ad-publishing/google/reporting` | `google-get-reporting` |
| Google campaign reporting | GET `/ad-publishing/google/reporting/campaign/{campaignId}` | `google-get-campaign-reporting` |
| Google saved report list | GET `/ad-publishing/google/reporting/list` | `google-get-reporting-list` |
| Google conversion goals | GET `/ad-publishing/google/conversion-goals` | `google-get-conversion-goals` |
| Google conversions (list) | GET `/ad-publishing/google/conversions` | `google-get-conversions` |
| Google conversion detail | GET `/ad-publishing/google/conversions/{conversionId}` | `google-get-conversion-by-id` |
| Create/update a conversion action | PUT `/ad-publishing/google/conversions` | `google-upsert-conversion` |
| Delete a conversion action | DELETE `/ad-publishing/google/conversions/{conversionId}` | `google-delete-conversion` |
| LinkedIn account-level analytics | GET `/ad-publishing/linkedin/reporting` | `li-get-ad-analytics` |
| LinkedIn campaign group reporting | GET `/ad-publishing/linkedin/reporting/campaign-group/{campaignGroupId}` | `li-get-campaign-group-reporting` |
| LinkedIn saved report list | GET `/ad-publishing/linkedin/reporting/list` | `li-get-reporting-list` |

## 7. Audiences and segments

| Task | Method / Path | opId | Kind |
|---|---|---|---|
| List Facebook custom audiences | GET `/ad-publishing/facebook/custom-audience` | `fb-get-custom-audiences` | read |
| Get one custom audience | GET `/ad-publishing/facebook/custom-audience/{audienceId}` | `fb-get-custom-audience-by-id` | read |
| Create/update a custom audience | PUT `/ad-publishing/facebook/custom-audience/{audienceId}` | `fb-update-custom-audience` | write |
| Delete a custom audience | DELETE `/ad-publishing/facebook/custom-audience/{audienceId}` | `fb-delete-custom-audience` | delete |
| Add a member | PUT `/ad-publishing/facebook/custom-audience/{audienceId}/member` | `fb-add-custom-audience-member` | write |
| Remove a member | DELETE `/ad-publishing/facebook/custom-audience/{audienceId}/member` | `fb-remove-custom-audience-member` | delete |
| Batch update members | PUT `/ad-publishing/facebook/custom-audience/{audienceId}/member/batch` | `fb-batch-update-audience-members` | write |
| List Google audiences | GET `/ad-publishing/google/audiences` | `google-get-audiences` | read |
| Create/update a Google audience | PUT `/ad-publishing/google/audiences` | `google-upsert-audience` | write |
| Get one Google audience | GET `/ad-publishing/google/audiences/{audienceId}` | `google-get-audience-by-id` | read |
| List Google segments | GET `/ad-publishing/google/segments` | `google-get-segments` | read |
| Create/update a Google segment | PUT `/ad-publishing/google/segments` | `google-upsert-segment` | write |
| Delete a Google segment | DELETE `/ad-publishing/google/segments/{segmentId}` | `google-delete-segment` | delete |
| Get one Google segment | GET `/ad-publishing/google/segments/{segmentId}` | `google-get-segment-by-id` | read |
| Upload a Customer Match list | POST `/ad-publishing/google/segments/offline-user-list-job` | `google-create-offline-user-list-job` | write |

LinkedIn has no audience-management endpoint in this catalog. `li-search-targeting` only
covers interest/company facets, not custom lists. Route those tasks to the LinkedIn
Campaign Manager UI or `ghl-browser`.

## 8. Platform-native lead forms (not GHL's own form builder)

| Task | Method / Path | opId | Kind |
|---|---|---|---|
| List Facebook conversation (Messenger) forms | GET `/ad-publishing/facebook/conversation-forms` | `fb-get-conversation-forms` | read |
| Create a conversation form | POST `/ad-publishing/facebook/conversation-forms` | `fb-create-conversation-form` | write |
| Get one Facebook lead form | GET `/ad-publishing/facebook/lead-form/{leadFormId}` | `fb-get-lead-form` | read |
| List a Page's lead forms | GET `/ad-publishing/facebook/page/{pageId}/forms` | `fb-get-page-lead-forms` | read |
| Create a Page lead form | POST `/ad-publishing/facebook/page/{pageId}/forms` | `fb-create-page-lead-form` | write |
| List LinkedIn lead forms | GET `/ad-publishing/linkedin/{accountId}/forms` | `li-get-lead-forms` | read |
| Create a LinkedIn lead form | POST `/ad-publishing/linkedin/{accountId}/form` | `li-create-lead-form` | write |

## 9. Creative assets

Facebook and LinkedIn ads reference creative by URL from the shared `medias` domain
(outside ad-publishing). Upload there, then pass the URL in `fb-upsert-ad` or the
LinkedIn campaign group body. Google keeps a dedicated store in this domain:

| Task | Method / Path | opId | Kind |
|---|---|---|---|
| List Google assets | GET `/ad-publishing/google/assets` | `google-get-assets` | read |
| Create/update Google assets | POST `/ad-publishing/google/assets` | `google-upsert-assets` | write |
