"""Bounded min-heap for Top 10 notification ranking."""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field

from logging_middleware.middleware import log_execution
from notification_app_be.models.notification import Notification


@dataclass(order=True)
class HeapEntry:
    priority: float
    id: str
    notification: Notification = field(compare=False)


@log_execution(package="utils")
def build_heap_entry(notification: Notification, priority: float) -> HeapEntry:
    """Create a heap entry with priority and id tie-breaker."""
    return HeapEntry(priority=priority, id=notification.id, notification=notification)


@log_execution(package="utils")
def should_replace_min(heap: list[HeapEntry], candidate: HeapEntry) -> bool:
    """Return whether a candidate outranks the current heap minimum."""
    return bool(heap) and (candidate.priority, candidate.id) > (heap[0].priority, heap[0].id)


@log_execution(package="utils")
def push_top_notification(heap: list[HeapEntry], entry: HeapEntry, limit: int = 10) -> list[HeapEntry]:
    """Maintain a bounded min-heap of the top notifications."""
    if len(heap) < limit:
        heapq.heappush(heap, entry)
        return heap

    if should_replace_min(heap, entry):
        heapq.heapreplace(heap, entry)

    return heap


@log_execution(package="utils")
def top_notifications_descending(heap: list[HeapEntry]) -> list[HeapEntry]:
    """Return final Top 10 in descending rank order."""
    return sorted(heap, key=lambda entry: (entry.priority, entry.id), reverse=True)
