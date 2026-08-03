"""
Entry point for the research assistant agent.

This script initializes the agent and demonstrates its capabilities
by answering a series of example questions.
"""

import os

from dotenv import load_dotenv

from agent import Agent
from observability import configure_confident_tracing


def main():
    """Run the research assistant agent with example questions."""
    # Load environment variables from .env file
    load_dotenv()
    configure_confident_tracing()

    # Verify that the API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please copy .env.example to .env and add your OpenAI API key.")
        return

    # Initialize the agent
    agent = Agent()

    # Example questions to demonstrate the agent's capabilities
    example_questions = [
        "What is machine learning and how does it relate to AI?",
        "What is the result of 42 multiplied by 7?",
        "What is Kubernetes and why is it useful?",
    ]

    print("=" * 80)
    print("Research Assistant Agent")
    print("=" * 80)

    for i, question in enumerate(example_questions, 1):
        print(f"\n[Question {i}]")
        print(f"User: {question}")
        print("-" * 80)

        try:
            answer = agent.run(question)
            print(f"Agent: {answer}")
        except ValueError as e:
            print(f"Error: {e}")
            return
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

        print()

    print("=" * 80)


if __name__ == "__main__":
    main()
