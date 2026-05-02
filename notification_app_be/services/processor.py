"""Notification processing pipeline."""

from __future__ import annotations

from typing import Any

from logging_middleware.middleware import log_function
from notification_app_be.models.notification import (
    Notification,
    parse_notification,
    reference_time_seconds,
)
from notification_app_be.utils.heap import (
    HeapEntry,
    build_heap_entry,
    push_top_notification,
    top_notifications_descending,
)
from notification_app_be.utils.priority import calculate_priority


@log_function
def parse_valid_notifications(items: list[dict[str, Any]]) -> list[Notification]:
    """Parse valid notifications and skip malformed API records."""
    notifications: list[Notification] = []

    for item in items:
        if "error" in item:
            continue

        try:
            notifications.append(parse_notification(item))
        except ValueError:
            continue

    return notifications


@log_function
def process_stream(notifications: list[Notification], limit: int = 10) -> list[HeapEntry]:
    """Process notifications one-by-one using a bounded min-heap."""
    heap: list[HeapEntry] = []
    reference_time = reference_time_seconds(notifications)

    for notification in notifications:
        priority = calculate_priority(notification, reference_time)
        entry = build_heap_entry(notification, priority)
        push_top_notification(heap, entry, limit)

    return top_notifications_descending(heap)


@log_function
def serialize_ranked_notifications(entries: list[HeapEntry]) -> list[dict[str, Any]]:
    """Serialize heap entries for final Stage 1 output."""
    return [
        {
            "id": entry.notification.id,
            "type": entry.notification.type,
            "timestamp": entry.notification.timestamp,
            "priority": entry.priority,
        }
        for entry in entries
    ]


@log_function
def compute_top_notifications(raw_items: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
    """Parse, rank, and serialize the Top 10 notifications."""
    notifications = parse_valid_notifications(raw_items)
    top_entries = process_stream(notifications, limit)
    return serialize_ranked_notifications(top_entries)
