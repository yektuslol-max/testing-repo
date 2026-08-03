"""HTTP API for the research assistant."""
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel

from agent import Agent

load_dotenv()

app = FastAPI()
agent = Agent()


class ChatRequest(BaseModel):
    question: str
    n: str | int | None = None


@app.post("/chat")
def chat(req: ChatRequest):
    return {"answer": agent.run(req.question, test_case_id=req.n)}
