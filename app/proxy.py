from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any, Optional 

from .detection import analyze_text
from .policy import evaluate_policy
from .logging_utils import log_incident

app = FastAPI(
  title="GenAI Data Leakage Guard",
  description="Local GenAI proxy that inspects prompts for sensitive data."
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
  action: str
  masked_prompt: Optionnal[str]
  findings: List[Finding]
  model_response: Optional[str]
  message: str

@app.get("/health")
def health_check():
  return {"status": "OK"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
  original_prompt = request.prompt
 
  raw_findings: List[Dict[str, Any]] = analyze_text(original_prompt)

  action, processed_prompt = evaluate_policy(original_prompt, raw_findings)

  log_incident(
    prompt=original_prompt,
    action=action,
    findings=raw_findings,
    masked_prompt=processed_prompt if action == "MASK" else None,
  )

  if action == "BLOCK":
    return ChatResponse(
      action=action,
      masked_prompt=None,
      findings=[Finding(**f) for f in raw_findings],
      model_response=None,
      message="Request blocked: Sensitive data detected. Please remove it."
  else:
    simulated_response =(
      "Simulated LLM response to your prompt"
      "[Note: In real deployment, this would be an upstream API call.]"
    )
    return ChatResponse(
      action=action,
      masked_prompt=processed_prompt if action == "MASK" else None,
      findings=[Finding(**f) for f in raw_finding],
      model_response=simulated_repsonse,
      message="Request processed.",
    )

