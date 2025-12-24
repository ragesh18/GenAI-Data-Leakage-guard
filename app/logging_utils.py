# app/logging_utils.py

from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
INCIDENT_LOG_FILE = LOG_DIR / "incidents.jsonl"


def log_incident(
    prompt: str,
    action: str,
    findings: List[Dict[str, Any]],
    masked_prompt: str | None = None,
) -> None:
    """
    Append an incident log entry to logs/incidents.jsonl
    """
    entry: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "prompt": prompt,
        "masked_prompt": masked_prompt,
        "findings": findings,
    }
    with INCIDENT_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
