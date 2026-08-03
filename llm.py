"""
Thin wrapper over the OpenAI Chat Completions API.

This module provides a simple interface to call OpenAI's chat models.
The OPENAI_API_KEY environment variable must be set to use this module.
"""

import os
from typing import Any

from deepeval.openai import OpenAI


def chat(messages: list[dict[str, str]]) -> str:
    """
    Send a list of messages to the OpenAI Chat Completions API and return the response.

    Args:
        messages: A list of message dictionaries with 'role' and 'content' keys.
                 Example: [{"role": "user", "content": "What is 2+2?"}]

    Returns:
        The text content of the assistant's response.

    Raises:
        ImportError: If the openai package is not installed.
        ValueError: If OPENAI_API_KEY is not set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content
