"""
Research assistant agent with a clear decision loop.

This module implements an agent that answers questions by retrieving relevant context,
deciding whether to use tools, and then synthesizing a final answer using an LLM.
"""

import json
from typing import Any

from deepeval.tracing import observe
from deepeval.tracing.context import update_current_span, update_current_trace

import llm
import retriever
import tools


class Agent:
    """
    A research assistant agent that answers questions using retrieval and LLM reasoning.

    The agent follows a structured loop:
    1. Retrieve relevant documents for the query
    2. Ask the LLM if a tool is needed
    3. Call the tool if requested
    4. Generate a final answer
    """

    def __init__(self):
        """Initialize the agent."""
        self.available_tools = {
            "calculator": tools.calculator,
            "get_current_time": tools.get_current_time,
        }

    @observe(type="agent", name="research_assistant_agent", available_tools=["calculator", "get_current_time"])
    def run(self, question: str, test_case_id: str | None = None) -> str:
        """
        Run the agent to answer a question.

        Args:
            question: The user's question.

        Returns:
            The agent's final answer.
        """
        if test_case_id:
            update_current_trace(test_case_id=test_case_id)

        update_current_span(input=question)

        # Step 1: Retrieve relevant context
        context_docs = retriever.retrieve(question)
        context_str = "\n".join([f"- {doc}" for doc in context_docs]) if context_docs else "No relevant documents found."

        # Step 2: Ask LLM if a tool is needed
        tool_decision_messages = [
            {
                "role": "user",
                "content": f"""You are a research assistant. Based on the user's question and available documents, 
decide if you need to call a tool.

Available tools:
1. calculator(expression) - Evaluates mathematical expressions
2. get_current_time() - Returns the current date and time

Relevant documents:
{context_str}

User question: {question}

Respond with a JSON object containing:
{{"need_tool": true/false, "tool_name": "calculator" or "get_current_time" or null, "tool_input": "..." or null}}

Only set need_tool to true if absolutely necessary.""",
            }
        ]

        tool_decision_response = llm.chat(tool_decision_messages)

        # Parse the tool decision
        tool_name = None
        tool_input = None
        tool_result = None

        try:
            decision = json.loads(tool_decision_response)
            if decision.get("need_tool") and decision.get("tool_name"):
                tool_name = decision["tool_name"]
                tool_input = decision.get("tool_input", "")

                # Step 3: Call the tool if needed
                if tool_name in self.available_tools:
                    tool_result = self.available_tools[tool_name](tool_input)
        except (json.JSONDecodeError, KeyError):
            # If the LLM doesn't return valid JSON, proceed without a tool
            pass

        # Step 4: Generate final answer
        final_messages = [
            {
                "role": "user",
                "content": f"""You are a helpful research assistant. Answer the following question based on the provided context.

Relevant documents:
{context_str}

User question: {question}""",
            }
        ]

        if tool_result:
            final_messages.append(
                {
                    "role": "assistant",
                    "content": f"I decided to use the {tool_name} tool. The result was: {tool_result}",
                }
            )
            final_messages.append(
                {
                    "role": "user",
                    "content": "Based on this tool result, please provide a comprehensive answer to the original question.",
                }
            )

        answer = llm.chat(final_messages)
        return answer
