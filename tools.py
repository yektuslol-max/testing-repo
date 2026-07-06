"""
Tool implementations for the research assistant agent.

These tools can be called by the agent to augment its reasoning capabilities.
Each tool has a clear interface and documentation for the agent to understand.
"""

import time
from datetime import datetime

from deepeval.tracing import observe, update_current_span


@observe(type="tool")
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression and return the result.

    Args:
        expression: A mathematical expression as a string (e.g., "2 + 2 * 3").

    Returns:
        A string containing the result or an error message.

    Note:
        Only basic arithmetic operations are supported for safety.
    """
    try:
        # Validate that the expression only contains safe characters
        safe_chars = set("0123456789+-*/(). ")
        if not all(c in safe_chars for c in expression):
            return f"Error: Invalid characters in expression"

        result = eval(expression, {"__builtins__": {}}, {})
        output = str(result)
    except Exception as e:
        output = f"Error evaluating expression: {str(e)}"

    update_current_span(input={"expression": expression}, output=output)
    return output


@observe(type="tool")
def get_current_time() -> str:
    """
    Return the current date and time.

    Returns:
        A formatted string with the current date and time (ISO 8601 format).
    """
    output = datetime.now().isoformat()
    update_current_span(input={}, output=output)
    return output
