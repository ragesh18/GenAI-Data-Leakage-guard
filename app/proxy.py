# app/proxy.py

from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from .detection import analyze_text
from .policy import evaluate_policy
from .logging_utils import log_incident

app = FastAPI(
    title="GenAI Data Leakage Guard",
    description="Local GenAI proxy that inspects prompts for sensitive data.",
    version="0.1.0",
)


class ChatRequest(BaseModel):
    prompt: str


class Finding(BaseModel):
    category: str
    severity: str
    match: str
    start: int
    end: int
    description: str


class ChatResponse(BaseModel):
    action: str                 # ALLOW / MASK / BLOCK
    masked_prompt: Optional[str]
    findings: List[Finding]
    model_response: Optional[str]
    message: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    original_prompt = request.prompt

    # 1) Run detection
    raw_findings: List[Dict[str, Any]] = analyze_text(original_prompt)

    # 2) Apply policy
    action, processed_prompt = evaluate_policy(original_prompt, raw_findings)

    # 3) Log incident
    log_incident(
        prompt=original_prompt,
        action=action,
        findings=raw_findings,
        masked_prompt=processed_prompt if action == "MASK" else None,
    )

    # 4) In a real system, here you would forward to your LLM API.
    #    For demo, we just generate a dummy response.
    if action == "BLOCK":
        return ChatResponse(
            action=action,
            masked_prompt=None,
            findings=[Finding(**f) for f in raw_findings],
            model_response=None,
            message="Request blocked: sensitive data detected. Please remove secrets/PII.",
        )
    else:
        # Simulated model response
        simulated_response = (
            "Simulated LLM response to your prompt "
            "(note: in real deployment this would be an upstream API call)."
        )
        return ChatResponse(
            action=action,
            masked_prompt=processed_prompt if action == "MASK" else None,
            findings=[Finding(**f) for f in raw_findings],
            model_response=simulated_response,
            message="Request processed.",
        )
# To run the app, use:
# uvicorn app.proxy:app --host 0.0.0.0 --port 8000