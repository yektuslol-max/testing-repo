"""
Tracing configuration for DeepEval/Confident AI.

This module centralizes the optional Confident AI API key wiring so the app
can enable export in both local runs and Confident-triggered eval runs.
"""

import os

from deepeval.tracing import trace_manager

_configured = False


def configure_tracing() -> None:
    """Configure DeepEval tracing once per process."""
    global _configured
    if _configured:
        return

    confident_api_key = os.getenv("CONFIDENT_API_KEY")
    if confident_api_key:
        trace_manager.configure(confident_api_key=confident_api_key)

    _configured = True
