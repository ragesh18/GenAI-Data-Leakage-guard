# app/detection.py

from __future__ import annotations
import re
import math
from typing import List, Dict, Any


# ----------------------------
# Regex patterns for PII/Secrets
# ----------------------------

EMAIL_REGEX = re.compile(
    r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
)

PHONE_REGEX = re.compile(
    r"\b(\+?\d{1,3}[- ]?)?\d{10}\b"
)

AADHAAR_REGEX = re.compile(
    r"\b\d{4}\s?\d{4}\s?\d{4}\b"
)

PASSPORT_REGEX = re.compile(
    r"\b[A-PR-WY][1-9]\d{6}\b",
    re.IGNORECASE,
)

# Common patterns for API keys / tokens (very rough heuristics)
POSSIBLE_KEY_REGEX = re.compile(
    r"\b([A-Za-z0-9+/]{20,}|[A-Za-z0-9_-]{20,})\b"
)

# Rough "source code" hint: things that look like code blocks, braces, etc.
SOURCE_CODE_HINT_REGEX = re.compile(
    r"(def\s+\w+\s*\(|class\s+\w+\s*:|#include\s+<|public\s+class|private\s+static|function\s+\w+\()"
)


def shannon_entropy(s: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not s:
        return 0.0
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    entropy = 0.0
    length = len(s)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy


def _matches_to_findings(
    text: str,
    regex: re.Pattern,
    category: str,
    severity: str,
    description: str,
) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    for m in regex.finditer(text):
        findings.append(
            {
                "category": category,
                "severity": severity,
                "match": m.group(0),
                "start": m.start(),
                "end": m.end(),
                "description": description,
            }
        )
    return findings


def detect_pii(text: str) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    findings += _matches_to_findings(
        text,
        EMAIL_REGEX,
        "pii_email",
        "medium",
        "Possible email address",
    )
    findings += _matches_to_findings(
        text,
        PHONE_REGEX,
        "pii_phone",
        "medium",
        "Possible phone number",
    )
    findings += _matches_to_findings(
        text,
        AADHAAR_REGEX,
        "pii_aadhaar_like",
        "high",
        "Possible Aadhaar-like ID",
    )
    findings += _matches_to_findings(
        text,
        PASSPORT_REGEX,
        "pii_passport_like",
        "high",
        "Possible passport-like ID",
    )
    return findings


def detect_secrets(text: str) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    for m in POSSIBLE_KEY_REGEX.finditer(text):
        candidate = m.group(0)
        if len(candidate) < 16:
            continue
        entropy = shannon_entropy(candidate)
        # Tune this threshold in experiments
        if entropy > 3.5:
            findings.append(
                {
                    "category": "secret_key",
                    "severity": "high",
                    "match": candidate,
                    "start": m.start(),
                    "end": m.end(),
                    "description": f"High-entropy token-like string (entropy={entropy:.2f})",
                }
            )
    return findings


def detect_source_code(text: str) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    for m in SOURCE_CODE_HINT_REGEX.finditer(text):
        findings.append(
            {
                "category": "source_code",
                "severity": "medium",
                "match": m.group(0),
                "start": m.start(),
                "end": m.end(),
                "description": "Possible source code snippet",
            }
        )
    return findings


def analyze_text(text: str) -> List[Dict[str, Any]]:
    """
    Main detection function.

    Returns a list of findings, each with:
        - category
        - severity
        - match
        - start, end
        - description
    """
    findings: List[Dict[str, Any]] = []
    findings.extend(detect_pii(text))
    findings.extend(detect_secrets(text))
    findings.extend(detect_source_code(text))

    
    return findings
'''# Example business-sensitive keywords (very basic)
BUSINESS_SENSITIVE_KEYWORDS = [
    "confidential",
    "internal use only",
    "do not distribute",
    "proprietary",
]
def detect_business_sensitive(text: str) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    lowered_text = text.lower()
    for keyword in BUSINESS_SENSITIVE_KEYWORDS:
        start = 0
        while True:
            start = lowered_text.find(keyword, start)
            if start == -1:
                break
            end = start + len(keyword)
            findings.append(
                {
                    "category": "business_sensitive",
                    "severity": "medium",
                    "match": text[start:end],
                    "start": start,
                    "end": end,
                    "description": f"Business-sensitive keyword: '{keyword}'",
                }
            )
            start = end  # Move past this match
    return findings'''