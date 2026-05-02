"""Decorator-based logging middleware."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar

from logging_middleware.logger import current_timestamp, to_jsonable, write_log

P = ParamSpec("P")
R = TypeVar("R")


def log_function(func: Callable[P, R]) -> Callable[P, R]:
    """Log function name, timestamp, inputs, and outputs for every call."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        output = func(*args, **kwargs)
        write_log(
            {
                "function_name": func.__qualname__,
                "timestamp": current_timestamp(),
                "inputs": {"args": to_jsonable(args), "kwargs": to_jsonable(kwargs)},
                "outputs": to_jsonable(output),
            }
        )
        return output

    return wrapper
