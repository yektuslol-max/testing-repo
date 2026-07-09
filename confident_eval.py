"""
Entry point for the Confident PR Eval Gate.

Confident's runner calls ``run(input)`` once per dataset row. Each ``input`` is a
natural language question (a bare string), matching the signature of the research
assistant agent's ``Agent.run(question)`` method, which returns the answer string.
"""

from agent import Agent


def run(input):
    """
    Run the research assistant agent on a single dataset input.

    Args:
        input: A natural language question string from the pinned dataset.

    Returns:
        The agent's answer as a string.
    """
    agent = Agent()
    answer = agent.run(input)
    return str(answer)
