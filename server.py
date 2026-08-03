"""HTTP API for the research assistant."""
from fastapi import FastAPI
from pydantic import BaseModel

from agent import Agent
from tracing import tracing_context

app = FastAPI()
agent = Agent()


class ChatRequest(BaseModel):
    question: str
    testCaseId: str | None = None


@app.post("/chat")
def chat(req: ChatRequest):
    with tracing_context(req.testCaseId):
        return {"answer": agent.run(req.question)}
