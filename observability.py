"""Thin compatibility layer for Deepeval tracing."""

from __future__ import annotations

import os
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

try:
    from deepeval.confident.api import set_confident_api_key
    from deepeval.tracing import observe as deepeval_observe
except ImportError:  # pragma: no cover - optional dependency in local dev
    set_confident_api_key = None  # type: ignore[assignment]
    deepeval_observe = None  # type: ignore[assignment]


def configure_confident_tracing() -> None:
    """Load the Confident API key into Deepeval if it is present."""

    api_key = os.getenv("CONFIDENT_API_KEY")
    if not api_key or set_confident_api_key is None:
        return

    try:
        set_confident_api_key(api_key)
    except Exception:
        # Tracing should never block the app path.
        pass


def observe(*args, **kwargs):
    if deepeval_observe is not None:
        return deepeval_observe(*args, **kwargs)

    def decorator(func: F) -> F:
        return func

    if args and callable(args[0]) and not kwargs:
        return args[0]
    return decorator
