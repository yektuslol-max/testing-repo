# Research Assistant Agent

A minimal but realistic Python AI agent application that demonstrates a structured decision loop for answering questions.

## Overview

The agent implements a three-step process:

1. **Retrieval** — Fetches relevant context from an in-memory knowledge base using keyword matching
2. **Tool Decision** — Uses an LLM to decide if external tools are needed (calculator, current time)
3. **Synthesis** — Generates a final answer based on context and any tool results

This is a clean example of an agent architecture suitable for adding observability instrumentation.

## Project Structure

```
├── llm.py           # OpenAI Chat Completions API wrapper
├── retriever.py     # Keyword-based document retrieval (mock RAG)
├── tools.py         # Callable tools: calculator, get_current_time
├── agent.py         # Agent class with the main orchestration loop
├── main.py          # Runnable entry point
├── requirements.txt # Dependencies: openai, python-dotenv
├── .env.example     # Environment configuration template
└── README.md        # This file
```

## Setup

### Prerequisites

- Python 3.10 or later
- An OpenAI API key (get one at https://platform.openai.com/api-keys)

### Installation

1. Clone this repository and navigate to the project directory:
   ```bash
   cd testing-repo
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-...
   ```

## Running the Agent

Execute the main script to see the agent in action:

```bash
python main.py
```

The agent will answer three example questions and display the reasoning process.

## Design Notes

- **Tracing** — The agent is instrumented with [DeepEval](https://www.confident-ai.com) tracing. The LLM, retriever, tool, and agent components each emit a span, so a run can be inspected step by step in Confident AI (see [Observability](#observability)).
- **Clean Module Boundaries** — Each module has a single responsibility and can be tested independently.
- **Realistic Structure** — The agent loop mimics real-world agent implementations with explicit decision points.
- **Mock Data** — Uses a hard-coded knowledge base and mock tools for reproducibility without external dependencies.

## Example Interaction

```
[Question 1]
User: What is machine learning and how does it relate to AI?
Agent: Machine learning is a subset of artificial intelligence that enables systems to learn from data...

[Question 2]
User: What is the result of 42 multiplied by 7?
Agent: The result of 42 multiplied by 7 is 294.

[Question 3]
User: What is Kubernetes and why is it useful?
Agent: Kubernetes is an open-source container orchestration platform...
```

## Observability

This app is traced with [DeepEval](https://www.confident-ai.com) native tracing:

- `llm.py` uses `deepeval.openai.OpenAI`, a drop-in replacement that emits an
  **LLM span** for every chat completion.
- `retriever.retrieve`, the tools in `tools.py`, and `Agent.run` are wrapped with
  `@observe` as **retriever**, **tool**, and **agent** spans respectively.

To send traces to Confident AI, set `CONFIDENT_API_KEY` in your `.env`
(get one from your Confident AI account, then copy `.env.example` to `.env`):

```
CONFIDENT_API_KEY=...
```

Without the key the app still runs normally; traces simply are not uploaded.

## Future Enhancements

This codebase is designed to be extended with:

- Tracing and observability (OpenTelemetry, Datadog, etc.)
- Logging frameworks
- Performance monitoring
- Agent evaluation frameworks
- Vector database integration for retrieval
