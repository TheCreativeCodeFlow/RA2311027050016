"""Priority scoring for campus notifications."""

from __future__ import annotations

from logging_middleware.middleware import log_execution
from notification_app_be.models.notification import Notification

TYPE_WEIGHTS: dict[str, int] = {
    "placement": 3,
    "result": 2,
    "event": 1,
}


@log_execution(package="domain")
def get_type_weight(notification_type: str) -> int:
    """Return the configured type weight."""
    return TYPE_WEIGHTS[notification_type]


@log_execution(package="domain")
def calculate_priority(notification: Notification, reference_time: float) -> float:
    """Calculate priority = (type_weight * 1000) - time_difference."""
    time_difference = max(0.0, reference_time - notification.timestamp)
    return (get_type_weight(notification.type) * 1000) - time_difference
