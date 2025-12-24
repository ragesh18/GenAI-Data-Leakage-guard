# app/policy.py

from __future__ import annotations
from typing import List, Dict, Any, Tuple


# Simple policy configuration
POLICY = {
    "block_categories": {"secret_key"},
    "mask_categories": {
        "pii_email",
        "pii_phone",
        "pii_aadhaar_like",
        "pii_passport_like",
        "source_code",
    },
    # Severity escalation thresholds (you can make this more complex)
    "high_severity_block": True,
}


def decide_action(findings: List[Dict[str, Any]]) -> str:
    """
    Decide whether to ALLOW, MASK, or BLOCK based on findings.
    """
    if not findings:
        return "ALLOW"

    categories = {f["category"] for f in findings}
    severities = {f.get("severity", "low") for f in findings}

    # Block if secret_key found
    if categories & POLICY["block_categories"]:
        return "BLOCK"

    # Block if high severity and configured so
    if POLICY["high_severity_block"] and ("high" in severities):
        return "BLOCK"

    # Otherwise, mask
    return "MASK"


def mask_text(text: str, findings: List[Dict[str, Any]]) -> str:
    """
    Replace sensitive spans with masked placeholders.
    We replace from right to left so indexes don't shift.
    """
    if not findings:
        return text

    # Only mask categories that are configured to be masked
    maskable = [
        f for f in findings
        if f["category"] in POLICY["mask_categories"]
        or f["category"] in POLICY["block_categories"]
    ]

    # Sort by start index descending
    maskable.sort(key=lambda f: f["start"], reverse=True)

    masked = text
    for f in maskable:
        start = f["start"]
        end = f["end"]
        category = f["category"]
        placeholder = f"[*** MASKED:{category} ***]"
        masked = masked[:start] + placeholder + masked[end:]
    return masked


def evaluate_policy(
    text: str,
    findings: List[Dict[str, Any]]
) -> Tuple[str, str]:
    """
    Given the original text and findings, return:
        (action, processed_text)

    action: "ALLOW", "MASK", or "BLOCK"
    processed_text: either original, masked, or original (on BLOCK we
                    don't modify, we just don't send it to upstream in proxy)
    """
    action = decide_action(findings)
    if action == "ALLOW":
        return "ALLOW", text
    elif action == "MASK":
        return "MASK", mask_text(text, findings)
    else:  # BLOCK
        # We still return original text for logging purposes;
        # proxy will decide not to forward it.
        return "BLOCK", text
