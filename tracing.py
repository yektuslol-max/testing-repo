"""Best-effort tracing hooks for the research assistant."""

from __future__ import annotations

import contextlib
import contextvars
import importlib
import os
from typing import Any, Callable, TypeVar

T = TypeVar("T")
CONFIDENT_API_KEY = os.getenv("CONFIDENT_API_KEY")

_trace_test_case_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "trace_test_case_id", default=None
)


def _load_observe():
    """Load deepeval's observe decorator if it is available."""
    try:
        deepeval_tracing = importlib.import_module("deepeval.tracing")
    except Exception:
        return None

    observe = getattr(deepeval_tracing, "observe", None)
    return observe if callable(observe) else None


_OBSERVE = _load_observe()


def _call_optional_setter(test_case_id: str | None) -> None:
    """Attempt to propagate the test case id to a tracing backend."""
    if _OBSERVE is None:
        return

    module = importlib.import_module("deepeval.tracing")
    setter_names = (
        "set_test_case_id",
        "set_test_case",
        "set_current_test_case_id",
        "update_test_case_id",
    )
    for name in setter_names:
        setter = getattr(module, name, None)
        if callable(setter):
            try:
                setter(test_case_id)
                return
            except TypeError:
                continue


@contextlib.contextmanager
def tracing_context(test_case_id: str | None = None):
    """Bind request-scoped trace metadata for the current execution."""
    token = _trace_test_case_id.set(test_case_id)
    _call_optional_setter(test_case_id)
    try:
        yield
    finally:
        _trace_test_case_id.reset(token)
        _call_optional_setter(None)


def current_test_case_id() -> str | None:
    """Return the active test case id, if one was provided by the caller."""
    return _trace_test_case_id.get()


def trace_span(span_type: str, name: str | None = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorate a function with deepeval tracing when available."""

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        if _OBSERVE is None:
            return fn

        candidates: list[dict[str, Any] | None] = [
            {"name": name, "span_type": span_type},
            {"name": name, "type": span_type},
            {"span_type": span_type},
            {"type": span_type},
            None,
        ]

        for kwargs in candidates:
            try:
                if kwargs is None:
                    return _OBSERVE(fn)
                cleaned = {key: value for key, value in kwargs.items() if value is not None}
                return _OBSERVE(**cleaned)(fn)
            except TypeError:
                continue
            except Exception:
                continue

        return fn

    return decorator
