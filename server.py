"""HTTP API for the research assistant."""
from fastapi import FastAPI
from pydantic import BaseModel

from agent import Agent

app = FastAPI()
agent = Agent()


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(req: ChatRequest):
    return {"answer": agent.run(req.question)}
