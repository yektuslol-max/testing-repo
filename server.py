"""HTTP API for the research assistant."""
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from agent import Agent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
agent = Agent()


class ChatRequest(BaseModel):
    question: str
    testCaseId: Optional[str] = None


@app.post("/chat")
def chat(req: ChatRequest):
    return {"answer": agent.run(req.question, test_case_id=req.testCaseId)}
