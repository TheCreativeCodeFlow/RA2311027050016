# Priority Notification System - Stage 1 Design

## Scope

This Stage 1 solution is a Python backend-only implementation. It fetches notifications from:

```text
http://20.207.122.201/evaluation-service/notifications
```

It does not use a database, hardcoded notifications, or any frontend/UI.

## Flow

```text
main.run
  -> fetch_notifications
  -> extract_notification_items
  -> compute_top_notifications
  -> parse_valid_notifications
  -> process_stream
  -> calculate_priority
  -> push_top_notification
  -> top_notifications_descending
  -> emit_final_output
```

## Priority

```text
priority = (type_weight * 1000) - time_difference

placement = 3
result = 2
event = 1
```

`time_difference` is measured against the newest timestamp in the fetched batch. This keeps recency stream-relative and ensures newer notifications receive higher priority.

## Heap Strategy

The processor uses Python `heapq` as a bounded min-heap with maximum size 10.

- If fewer than 10 items exist, the notification is pushed.
- Once the heap has 10 items, only notifications with higher priority than the heap minimum replace it.
- The complete input list is not repeatedly sorted.
- The final output sorts only the bounded heap of at most 10 records.

## Edge Cases

- Duplicate timestamps are valid.
- Same priority is tied by notification id.
- Empty or small datasets return the available notifications.
- API errors or invalid API response shapes return an empty final ranking after structured error logging.

## Logging

All application functions use the reusable `@log_function` middleware. Each log entry includes:

- function name
- timestamp
- inputs
- outputs

The project does not use direct `print` statements.
