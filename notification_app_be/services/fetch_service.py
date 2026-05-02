"""HTTP fetch service for Stage 1 notification input."""

from __future__ import annotations

import os
from typing import Any

import requests

from logging_middleware.middleware import log_function

API_URL = "http://20.207.122.201/evaluation-service/notifications"
MAX_ERROR_BODY_CHARS = 500
API_TOKEN_ENV = "API_TOKEN"


@log_function
def extract_notification_items(payload: Any) -> list[dict[str, Any]]:
    """Extract notification objects from supported API response shapes."""
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict):
        candidate = payload.get("notifications") or payload.get("data") or payload.get("items")
        if not isinstance(candidate, list):
            raise ValueError("API response does not contain a notification list")
        items = candidate
    else:
        raise ValueError("API response must be a list or object")

    return [item for item in items if isinstance(item, dict)]


@log_function
def build_api_error_payload(exc: requests.RequestException) -> dict[str, Any]:
    """Build a safe structured API error payload."""
    response = exc.response

    return {
        "error": str(exc),
        "status_code": response.status_code if response is not None else None,
        "response_body": response.text[:MAX_ERROR_BODY_CHARS] if response is not None else None,
    }


@log_function
def fetch_notifications(url: str = API_URL, timeout_seconds: int = 10) -> list[dict[str, Any]]:
    """Fetch notifications from the evaluation API with graceful failure handling."""
    try:
        access_token = os.getenv(API_TOKEN_ENV)
        if not access_token:
            return [
                {
                    "error": f"{API_TOKEN_ENV} is missing from environment",
                    "status_code": None,
                    "response_body": None,
                }
            ]

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, timeout=timeout_seconds, headers=headers)
        response.raise_for_status()
        return extract_notification_items(response.json())
    except requests.RequestException as exc:
        return [build_api_error_payload(exc)]
    except ValueError as exc:
        return [{"error": str(exc), "status_code": None, "response_body": None}]
