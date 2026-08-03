"""Optional deepeval tracing helpers."""

from typing import Any, Callable, TypeVar

try:
    from deepeval.openai import OpenAI as TracedOpenAI
    from deepeval.tracing import observe, update_current_span, update_current_trace
except ImportError:
    from openai import OpenAI as TracedOpenAI

    F = TypeVar("F", bound=Callable[..., Any])

    def observe(*_args: Any, **_kwargs: Any):
        def decorator(func: F) -> F:
            return func

        return decorator

    def update_current_span(**_kwargs: Any) -> None:
        return None

    def update_current_trace(**_kwargs: Any) -> None:
        return None
