"""Notification model and API parsing helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from logging_middleware.middleware import log_execution


@dataclass(frozen=True)
class Notification:
    id: str
    type: str
    timestamp: float


@log_execution(package="domain")
def normalize_timestamp(raw_timestamp: Any) -> float:
    """Normalize supported timestamp shapes to epoch seconds."""
    if isinstance(raw_timestamp, (int, float)):
        timestamp = float(raw_timestamp)
        return timestamp / 1000 if timestamp > 10_000_000_000 else timestamp

    if isinstance(raw_timestamp, str):
        normalized = raw_timestamp.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized).timestamp()

    raise ValueError("notification timestamp is missing or invalid")


@log_execution(package="handler")
def parse_notification(payload: dict[str, Any]) -> Notification:
    """Create a Notification from an API payload."""
    notification_id = payload.get("id") or payload.get("ID")
    raw_type = payload.get("type") or payload.get("Type")
    notification_type = raw_type.lower() if isinstance(raw_type, str) else raw_type
    timestamp = payload.get("timestamp") or payload.get("Timestamp")

    if notification_id is None:
        notification_id = payload.get("notification_id")

    if timestamp is None:
        timestamp = payload.get("created_at") or payload.get("createdAt")

    if not isinstance(notification_id, (str, int)):
        raise ValueError("notification id is missing or invalid")

    if notification_type not in {"placement", "result", "event"}:
        raise ValueError("notification type is missing or invalid")

    return Notification(
        id=str(notification_id),
        type=notification_type,
        timestamp=normalize_timestamp(timestamp),
    )


@log_execution(package="domain")
def reference_time_seconds(notifications: list[Notification]) -> float:
    """Return the recency reference time for a fetched batch."""
    if not notifications:
        return datetime.now(timezone.utc).timestamp()

    return max(notification.timestamp for notification in notifications)
