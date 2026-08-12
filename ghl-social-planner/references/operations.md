# GHL Social Planner: operations by business task

49 ops total (43 social-planner + 6 medias), reorganised from the raw v2 catalog slice
by what you're trying to DO rather than by path. `kind` is the v2 catalog's label; some
"write"-kind ops are read requests that happen to use POST for their filter body (see
Domain gotchas in `../SKILL.md`).

## Accounts & connections

- `GET /social-media-posting/{locationId}/accounts`, opId `get-account`, scopes
  socialplanner/account.readonly, kind read. Lists every connected account for the
  location (accountId, platform, display name, status). It may be a fixed MCP operation.
- `GET /social-media-posting/oauth/{locationId}/{platform}/accounts/{accountId}`, opId
  `get-oauth-accounts`, scopes socialplanner/oauth.readonly, kind read. Checks token
  health for one connected account.
- `POST /social-media-posting/oauth/{locationId}/{platform}/accounts/{accountId}`, opId
  `attach-oauth-accounts`, scopes socialplanner/oauth.write, kind write. Reattaches or
  refreshes a token GHL already has a handshake for. Does NOT do the first-time OAuth
  consent (browser-only, see `../SKILL.md`).
- `DELETE /social-media-posting/{locationId}/accounts/{id}`, opId `delete-account`,
  scopes socialplanner/account.write, kind delete. Disconnects an account. Preview the
  impact with the user before running (posts scheduled to it will orphan).

## Posts: single item CRUD

- `POST /social-media-posting/{locationId}/posts`, opId `create-post`, scopes
  socialplanner/post.write, kind write. Creates a post (draft, scheduled, or
  immediate). It may be a fixed MCP operation.
- `PUT /social-media-posting/{locationId}/posts/{id}`, opId `edit-post`, scopes
  socialplanner/post.write, kind write. Edits an existing post. It may be a fixed MCP operation.
- `GET /social-media-posting/{locationId}/posts/{id}`, opId `get-post`, scopes
  socialplanner/post.readonly, kind read. Fetches one post, use it to verify a write.
  It may be a fixed MCP operation.
- `POST /social-media-posting/{locationId}/posts/list`, opId `get-posts`, scopes
  socialplanner/post.readonly, kind write (filter body, read semantics). Lists posts by
  date range, status, or account. It may be a fixed MCP operation.
- `DELETE /social-media-posting/{locationId}/posts/{id}`, opId `delete-post`, scopes
  socialplanner/post.write, kind delete. Removes a single post.

## Posts: bulk delete & CSV import

- `POST /social-media-posting/{locationId}/posts/bulk-delete`, opId
  `bulk-delete-social-planner-posts`, scopes socialplanner/post.write, kind write.
  Deletes many posts at once. Destructive at scale, preview count and date range first.
- `GET /social-media-posting/{locationId}/csv`, opId `get-upload-status`, scopes
  socialplanner/csv.readonly, kind read. Polls parse status of an uploaded CSV batch.
- `GET /social-media-posting/{locationId}/csv/{id}`, opId `get-csv-post`, scopes
  socialplanner/csv.readonly, kind read. Reviews a single parsed row before it commits.
- `PATCH /social-media-posting/{locationId}/csv/{id}`, opId `start-csv-finalize`,
  scopes socialplanner/csv.write, kind write. Commits the parsed batch to the live
  calendar. Review rows first, this is irreversible once posts schedule.
- `DELETE /social-media-posting/{locationId}/csv/{csvId}/post/{postId}`, opId
  `delete-csv-post`, scopes socialplanner/csv.write, kind delete. Drops one bad row from
  a pending batch.
- `DELETE /social-media-posting/{locationId}/csv/{id}`, opId `delete-csv`, scopes
  socialplanner/csv.write, kind delete. Scraps an entire pending CSV batch.
- `POST /social-media-posting/{locationId}/set-accounts`, opId `set-accounts`, scopes
  socialplanner/csv.write, kind write. Maps a CSV's account references to real
  accountIds before or around an import.

## Categories & queues (evergreen recycling)

- `GET /social-media-posting/category/queues/available-categories`, opId
  `fetchAvailableCategories`, scopes socialplanner/category.readonly, kind read. Lists
  evergreen categories available to queue against.
- `POST /social-media-posting/category/queues`, opId `createQueue`, scopes
  socialplanner/category.write, kind write. Creates a new recycling queue.
- `POST /social-media-posting/category/queues/list`, opId `fetchQueues`, scopes
  socialplanner/category.readonly, kind write (filter body, read semantics). Lists
  queues for the location.
- `POST /social-media-posting/category/queues/list/calendar`, opId
  `fetchCalendarList`, scopes socialplanner/category.readonly, kind write. Lists queue
  items rendered on a calendar view.
- `GET /social-media-posting/category/queues/{queueId}`, opId `fetchQueueById`, scopes
  socialplanner/category.readonly, kind read. Fetches one queue's config.
- `PUT /social-media-posting/category/queues/{queueId}`, opId `updateQueue`, scopes
  socialplanner/category.write, kind write. Updates queue config (accounts, category,
  cadence).
- `POST /social-media-posting/category/queues/{queueId}/create/item`, opId
  `createQueueItem`, scopes socialplanner/category.write, kind write. Adds a piece of
  evergreen content to the queue.
- `POST /social-media-posting/category/queues/{queueId}/items`, opId
  `fetchQueueItems`, scopes socialplanner/category.readonly, kind write (filter body,
  read semantics). Lists items currently in a queue.
- `PUT /social-media-posting/category/queues/{queueId}/items/{itemId}`, opId
  `updateQueueItem`, scopes socialplanner/category.write, kind write. Edits a queue
  item.
- `DELETE /social-media-posting/category/queues/{queueId}/items/{itemId}`, opId
  `deleteQueueItem`, scopes socialplanner/category.write, kind delete. Removes an item
  from the queue.
- `POST /social-media-posting/category/queues/{queueId}/items/{itemId}/clone`, opId
  `cloneQueueItem`, scopes socialplanner/category.write, kind write. Duplicates a piece
  of evergreen content that's working.
- `PUT /social-media-posting/category/queues/{queueId}/items/{itemId}/reset`, opId
  `resetQueueItem`, scopes socialplanner/category.write, kind write. Requeues an item
  after it's posted, the core recycling action.
- `POST /social-media-posting/category/queues/{queueId}/slots`, opId `fetchSlots`,
  scopes socialplanner/category.readonly, kind write (filter body, read semantics).
  Checks or generates a queue's posting time slots.
- `DELETE /social-media-posting/category/queues/{postId}/active-post`, opId
  `deleteCurrentActivePostAndScheduleNext`, scopes socialplanner/category.write, kind
  delete. Pulls whatever's live now and immediately promotes the next queued item.
  Publish-adjacent, needs explicit ask (see `../SKILL.md` safety rails).
- `POST /social-media-posting/category/queues/{queueId}/edit/start`, opId
  `startEditSession`, scopes socialplanner/category.write, kind write. Opens a safe
  edit session on a queue's calendar.
- `POST /social-media-posting/category/queues/{queueId}/edit/calendar`, opId
  `fetchEditSessionCalendar`, scopes socialplanner/category.readonly, kind write. Reads
  the calendar inside an open edit session.
- `POST /social-media-posting/category/queues/{queueId}/edit/save`, opId
  `saveEditSession`, scopes socialplanner/category.write, kind write. Commits an edit
  session's changes to the live queue.
- `POST /social-media-posting/category/queues/{queueId}/edit/discard`, opId
  `discardEditSession`, scopes socialplanner/category.write, kind write. Abandons an
  edit session without touching the live queue.

## Categories (legacy, location-level, read-only in this slice)

- `GET /social-media-posting/{locationId}/categories`, opId
  `get-categories-location-id`, scopes socialplanner/category.readonly, kind read.
  Lists legacy location categories. Not the same system as queues, see `../SKILL.md`
  gotchas.
- `GET /social-media-posting/{locationId}/categories/{id}`, opId `get-categories-id`,
  scopes socialplanner/category.readonly, kind read. Fetches one legacy category.

## Tags

- `GET /social-media-posting/{locationId}/tags`, opId `get-tags-location-id`, scopes
  socialplanner/tag.readonly, kind read. Lists tags available at the location.
- `POST /social-media-posting/{locationId}/tags/details`, opId `get-tags-by-ids`,
  scopes socialplanner/tag.readonly, kind write (filter body, read semantics). Resolves
  a set of tag IDs to their details.

## Comments & engagement

- `POST /social-media-posting/comments/{platform}`, opId `create-comment`, scopes
  socialplanner/comments.write, kind write. Replies to a comment on a published post.
- `POST /social-media-posting/comments/{platform}/list`, opId `get-comment-list`,
  scopes socialplanner/comments.readonly, kind write (filter body, read semantics).
  Pulls the comment thread for a post.
- `POST /social-media-posting/comments/{platform}/{id}/like`, opId `create-like`,
  scopes socialplanner/comments.write, kind write. Likes a comment.
- `DELETE /social-media-posting/comments/{platform}/{id}/like`, opId `delete-like`,
  scopes socialplanner/comments.write, kind delete. Unlikes a comment. No
  delete-comment op exists in this pack (see Browser-only edges in `../SKILL.md`).

## Statistics

- `POST /social-media-posting/statistics`, opId `get-statistics`, scopes
  socialplanner/statistics.readonly, kind write (filter body, read semantics). Per-post
  or per-account performance metrics for a date range. It may be a fixed MCP operation
  (`get-social-media-statistics`).

## Media library

- `GET /medias/files`, opId `fetch-media-content`, scopes medias.readonly, kind read.
  Lists the media library (files, folders). Despite the opId name this is the LIST
  endpoint, not a content-fetch of one file.
- `POST /medias/folder`, opId `create-media-folder`, scopes medias.write, kind write.
  Creates a folder to organise a batch of assets.
- `POST /medias/{id}`, opId `update-media-object`, scopes medias.write, kind write.
  Renames, retags, or moves a single asset.
- `PUT /medias/update-files`, opId `bulk-update-media-objects`, scopes medias.write,
  kind write. Renames, retags, or moves many assets at once.
- `DELETE /medias/{id}`, opId `delete-media-content`, scopes medias.write, kind delete.
  Removes a single asset.
- `PUT /medias/delete-files`, opId `bulk-delete-media-objects`, scopes medias.write,
  kind write. Removes many assets at once.

Note: none of the 6 medias ops in this pack is a raw multipart file-upload endpoint.
Before treating a new-asset upload as browser-only, search the registered GoHighLevel MCP
server for `upload media file`. Its full catalog may carry an upload operation this
domain slice does not surface. See `../SKILL.md` playbook 7.
