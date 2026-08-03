"""Tracing helpers for Deepeval instrumentation."""

from __future__ import annotations

from typing import Any, Callable, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

try:
    import deepeval.openai  # noqa: F401
    from deepeval.tracing import observe, update_current_span, update_current_trace
except ImportError:
    def observe(*args: Any, **kwargs: Any) -> Callable[[_F], _F]:
        def decorator(func: _F) -> _F:
            return func

        return decorator


    def update_current_span(**kwargs: Any) -> None:
        return None


    def update_current_trace(**kwargs: Any) -> None:
        return None
