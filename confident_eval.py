"""
Confident PR Eval Gate entry point.

Confident's runner calls `run(input)` once per dataset row. Each `input` is a
bare question string (matching the dataset shape), which we pass straight to the
research assistant agent and return its answer as a string.
"""

from agent import Agent

# Instantiate the agent once and reuse it across dataset rows.
_agent = Agent()


def run(input):
    """
    Answer a single dataset input with the research assistant agent.

    Args:
        input: A user question. The pinned dataset provides bare question
            strings, so it is passed directly to the agent.

    Returns:
        The agent's answer as a string.
    """
    answer = _agent.run(input)
    return answer if isinstance(answer, str) else str(answer)
