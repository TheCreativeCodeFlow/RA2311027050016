"""Decorator-based logging middleware."""

from __future__ import annotations

from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from logging_middleware.logger import MAX_LOG_MESSAGE_CHARS, log

P = ParamSpec("P")
R = TypeVar("R")


def _fit_message(message: str) -> str:
    """Fit a message within the Log API message limit."""
    return message[:MAX_LOG_MESSAGE_CHARS]


def log_execution(package: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Log function entry, exit, and exceptions using strict Log API fields."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            function_name = func.__qualname__
            log(
                "backend",
                "info",
                package,
                _fit_message(f"enter {function_name}"),
            )

            try:
                output = func(*args, **kwargs)
            except Exception as exc:
                log("backend", "error", package, _fit_message(f"exception {function_name}: {exc}"))
                raise

            log("backend", "info", package, _fit_message(f"exit {function_name}"))
            return output

        return wrapper

    return decorator


def log_function(func: Callable[P, R]) -> Callable[P, R]:
    """Backward-compatible default middleware for existing functions."""
    return log_execution(package="service")(func)
