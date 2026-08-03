"""
Confident PR Eval Gate entry point.

Confident's runner calls ``run(input)`` once per dataset row. Each ``input`` is
a single natural-language question (a bare string), which is exactly what the
research assistant agent expects. We invoke the agent and return its answer as a
string.
"""

from agent import Agent
from observability import configure_confident_tracing

# Instantiate once and reuse across dataset rows.
configure_confident_tracing()
_agent = Agent()


def run(input):
    """Run the research assistant agent on a single dataset input.

    Args:
        input: A single dataset row's input. For this dataset it is a bare
            question string.

    Returns:
        The agent's answer as a string.
    """
    answer = _agent.run(input)
    return answer if isinstance(answer, str) else str(answer)
