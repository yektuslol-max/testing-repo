"""HTTP API for the research assistant."""
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

from agent import Agent

app = FastAPI()
agent = Agent()


class ChatRequest(BaseModel):
    question: str
    testCaseId: str | None = None


@app.post("/chat")
def chat(req: ChatRequest):
    return {"answer": agent.run(req.question, test_case_id=req.testCaseId)}
