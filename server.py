"""HTTP API for the research assistant."""
from fastapi import FastAPI
from pydantic import BaseModel

from dotenv import load_dotenv

from agent import Agent

load_dotenv()

app = FastAPI()
agent = Agent()


class ChatRequest(BaseModel):
    question: str
    testCaseId: str | None = None


@app.post("/chat")
def chat(req: ChatRequest):
    return {"answer": agent.run(req.question, test_case_id=req.testCaseId)}
