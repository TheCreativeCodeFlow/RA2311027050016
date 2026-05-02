"""External Log API client for the notification backend."""

from __future__ import annotations

import atexit
import os
import queue
import threading
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from typing import Any

import requests
from dotenv import load_dotenv

LOG_API_URL = "http://20.207.122.201/evaluation-service/logs"
API_TOKEN_ENV = "API_TOKEN"
REQUEST_TIMEOUT_SECONDS = 3
MAX_BUFFERED_FAILURES = 250
MAX_LOG_MESSAGE_CHARS = 48

VALID_STACKS = {"backend", "frontend"}
VALID_LEVELS = {"debug", "info", "warn", "error", "fatal"}
VALID_PACKAGES = {
    "cache",
    "controller",
    "cron_job",
    "db",
    "domain",
    "handler",
    "repository",
    "route",
    "service",
    "auth",
    "config",
    "middleware",
    "utils",
}

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

_log_queue: queue.Queue[dict[str, str] | None] = queue.Queue(maxsize=1000)
_failure_buffer: list[dict[str, Any]] = []
_session = requests.Session()


def current_timestamp() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def to_jsonable(value: Any) -> Any:
    """Convert Python objects into JSON-safe values for internal messages."""
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


def _remember_failure(payload: dict[str, Any], reason: str) -> None:
    """Keep failed log attempts in a bounded in-memory buffer."""
    _failure_buffer.append(
        {
            "timestamp": current_timestamp(),
            "payload": payload,
            "reason": reason,
        }
    )
    if len(_failure_buffer) > MAX_BUFFERED_FAILURES:
        del _failure_buffer[: len(_failure_buffer) - MAX_BUFFERED_FAILURES]


def _validate_payload(stack: str, level: str, package: str, message: str) -> bool:
    """Validate payload fields before attempting to send them."""
    return (
        stack in VALID_STACKS
        and level in VALID_LEVELS
        and package in VALID_PACKAGES
        and isinstance(message, str)
        and bool(message.strip())
    )


def _build_headers() -> dict[str, str] | None:
    """Build Log API headers from environment state."""
    token = os.getenv(API_TOKEN_ENV)
    if not token:
        return None

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _send_log(payload: dict[str, str]) -> None:
    """Send one log payload to the external Log API."""
    headers = _build_headers()
    if headers is None:
        _remember_failure(payload, f"{API_TOKEN_ENV} is missing")
        return

    try:
        response = _session.post(
            LOG_API_URL,
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        if response.status_code >= 400:
            _remember_failure(payload, f"log api status {response.status_code}: {response.text[:200]}")
    except requests.RequestException as exc:
        _remember_failure(payload, str(exc))


def _worker() -> None:
    """Background worker that drains log payloads without blocking core logic."""
    while True:
        payload = _log_queue.get()
        try:
            if payload is None:
                return
            _send_log(payload)
        finally:
            _log_queue.task_done()


_worker_thread = threading.Thread(target=_worker, name="log-api-worker", daemon=True)
_worker_thread.start()


def log(stack: str, level: str, package: str, message: str) -> bool:
    """Validate and enqueue a strict Log API payload."""
    payload = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message[:MAX_LOG_MESSAGE_CHARS],
    }

    if not _validate_payload(**payload):
        _remember_failure(payload, "invalid log payload")
        return False

    try:
        _log_queue.put_nowait(payload)
        return True
    except queue.Full:
        _remember_failure(payload, "log queue full")
        return False


def flush_logs(timeout_seconds: float = 5.0) -> None:
    """Best-effort log flush used at process shutdown."""
    deadline = datetime.now(timezone.utc).timestamp() + timeout_seconds
    while not _log_queue.empty() and datetime.now(timezone.utc).timestamp() < deadline:
        try:
            _log_queue.join()
            break
        except RuntimeError:
            break


def write_log(record: dict[str, Any]) -> None:
    """Compatibility helper for final application events."""
    event = str(record.get("event", "application_event"))
    log("backend", "info", "controller", f"{event}: {to_jsonable(record)}")


atexit.register(flush_logs)
