from karmapash import KarmaPash
from app.providers.groq_provider import GroqProvider


from fastapi import FastAPI
from pydantic import BaseModel


kp = KarmaPash(
    provider=GroqProvider()
)


app = FastAPI(
    title="KarmaPash",
    description="LLM Security Gateway",
    version="0.1.0",
)


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {
        "name": "KarmaPash",
        "status": "online",
        "version": "0.1.0",
    }


@app.post("/scan")
def scan_prompt(request: PromptRequest):
    return kp.scan(request.prompt)


@app.post("/chat")
def chat(request: PromptRequest):
    return kp.chat(request.prompt)