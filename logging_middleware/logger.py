"""Custom structured logger for the notification backend."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from typing import Any


def current_timestamp() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def to_jsonable(value: Any) -> Any:
    """Convert Python objects into JSON-safe values for structured logs."""
    if is_dataclass(value):
        return to_jsonable(asdict(value))

    if isinstance(value, dict):
        return {str(key): to_jsonable(child) for key, child in value.items()}

    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(child) for child in value]

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, BaseException):
        return str(value)

    return value


def write_log(record: dict[str, Any]) -> None:
    """Write a single structured log record without using print or built-in loggers."""
    sys.stdout.write(json.dumps(to_jsonable(record), separators=(",", ":")) + "\n")
    sys.stdout.flush()
