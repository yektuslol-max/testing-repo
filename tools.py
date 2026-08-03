"""
Tool implementations for the research assistant agent.

These tools can be called by the agent to augment its reasoning capabilities.
Each tool has a clear interface and documentation for the agent to understand.
"""

import time
from datetime import datetime

import observability


@observability.observe(type="tool")
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
            result = "Error: Invalid characters in expression"
            observability.update_current_span(
                input=expression,
                output=result,
                metadata={"tool": "calculator"},
            )
            return result

        result = eval(expression, {"__builtins__": {}}, {})
        observability.update_current_span(
            input=expression,
            output=str(result),
            metadata={"tool": "calculator"},
        )
        return str(result)
    except Exception as e:
        result = f"Error evaluating expression: {str(e)}"
        observability.update_current_span(
            input=expression,
            output=result,
            metadata={"tool": "calculator"},
        )
        return result


@observability.observe(type="tool")
def get_current_time() -> str:
    """
    Return the current date and time.

    Returns:
        A formatted string with the current date and time (ISO 8601 format).
    """
    result = datetime.now().isoformat()
    observability.update_current_span(
        input={},
        output=result,
        metadata={"tool": "get_current_time"},
    )
    return result
