# **GenAI Data Leakage Guard (DLP Proxy) – Technical Documentation**
*Version 0.1.0*


---

## **1. Introduction**
### **1.1 Purpose**
The **GenAI Data Leakage Guard (DLP Proxy)** is a **local FastAPI-based proxy** that intercepts user prompts before they reach a Generative AI (GenAI) model. It detects, masks, or blocks sensitive information (e.g., PII, API keys, passwords) to prevent accidental data leakage.

### **1.2 Key Features**
| Feature | Description |
|---------|-------------|
| **Sensitive Data Detection** | Regex-based detection of emails, phone numbers, Aadhaar/Passport IDs, API keys, and source code snippets. |
| **Policy-Based Decision Engine** | Configurable rules to **ALLOW**, **MASK**, or **BLOCK** prompts. |
| **Incident Logging** | JSONL logs for auditing detected incidents. |
| **FastAPI Proxy** | RESTful API for seamless integration with GenAI clients. |
| **Local Deployment** | Runs as a standalone service (no cloud dependency). |

### **1.3 Architecture Diagram**
```mermaid
graph TD
    A[User Input] --> B[FastAPI Proxy]
    B --> C{Detection Engine}
    C -->|PII/Secrets Found| D[Policy Engine]
    D -->|ALLOW/MASK/BLOCK| E[Response]
    D --> F[Logging]
    E --> G[GenAI Model]
```

---

## **2. System Architecture**
### **2.1 Core Components**
| Component | File | Responsibility |
|-----------|------|----------------|
| **Detection Engine** | `app/detection.py` | Regex-based pattern matching for sensitive data. |
| **Policy Engine** | `app/policy.py` | Applies security policies (ALLOW/MASK/BLOCK). |
| **Logging** | `app/logging_utils.py` | Stores incidents in `logs/incidents.jsonl`. |
| **FastAPI Proxy** | `app/proxy.py` | REST API endpoint for prompt processing. |
| **Client Demo** | `tests/client_demo.py` | CLI tool to test the proxy. |

### **2.2 Data Flow**
1. **User Input** → Sent to `/chat` endpoint.
2. **Detection** → Regex scans for sensitive patterns.
3. **Policy Evaluation** → Decides ALLOW/MASK/BLOCK.
4. **Logging** → Records incidents for auditing.
5. **Response** → Returns masked/blocked prompt or allows forwarding.

---

## **3. Setup & Installation**
### **3.1 Prerequisites**
- Python 3.8+
- FastAPI (`fastapi`, `uvicorn`)
- Pydantic (`pydantic`)
- Requests (`requests`) for testing

### **3.2 Installation**
```bash
# Clone the repository
git clone https://github.com/your-repo/genai-dlp-guard.git
cd genai-dlp-guard

# Install dependencies
pip install -r tests/req.txt
```

### **3.3 Running the Proxy**
```bash
# Start FastAPI server
uvicorn app.proxy:app --reload
```
- **API Docs**: Open `http://127.0.0.1:8000/docs` for Swagger UI.

### **3.4 Testing with CLI Demo**
```bash
python tests/client_demo.py
```
- Enter prompts to test detection/masking.

---

## **4. API Documentation**
### **4.1 Endpoints**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | `GET` | Health check. |
| `/chat` | `POST` | Process a prompt (detect, mask, or block). |

### **4.2 Request/Response Schema**
#### **Request (`/chat`)**
```json
{
  "prompt": "My email is user@example.com."
}
```

#### **Response (`/chat`)**
```json
{
  "action": "MASK",  // ALLOW/MASK/BLOCK
  "masked_prompt": "[*** MASKED:pii_email ***]",
  "findings": [
    {
      "category": "pii_email",
      "severity": "medium",
      "match": "user@example.com",
      "start": 12,
      "end": 26,
      "description": "Possible email address"
    }
  ],
  "message": "Sensitive data masked."
}
```

### **4.3 Example Calls**
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/chat",
    json={"prompt": "API_KEY=abc123"}
)
print(response.json())
```
**Output:**
```json
{
  "action": "BLOCK",
  "message": "Request blocked: sensitive data detected."
}
```

---

## **5. Detection Logic**
### **5.1 Regex Patterns**
| Pattern | Regex | Example Matches |
|---------|-------|-----------------|
| **Email** | `r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"` | `user@example.com` |
| **Phone** | `r"\b(\+?\d{1,3}[- ]?)?\d{10}\b"` | `+1234567890` |
| **Aadhaar** | `r"\b\d{4}\s?\d{4}\s?\d{4}\b"` | `1234 5678 9012` |
| **API Key** | `r"\b([A-Za-z0-9+/]{20,}|[A-Za-z0-9_-]{20,})\b"` | `AKIAIOSFODNN7EXAMPLE` |
| **Source Code** | `r"(def\s+\w+\s*\(|class\s+\w+\s*:)"` | `def foo():` |

### **5.2 Entropy-Based Detection**
- **Shannon Entropy** (`app/detection.py:shannon_entropy`) measures randomness in strings (e.g., API keys).
- High entropy → Likely a secret.

---

## **6. Policy Engine**
### **6.1 Configuration**
```python
POLICY = {
    "block_categories": {"secret_key"},  # Always block
    "mask_categories": {"pii_email", "pii_phone"},  # Mask these
    "high_severity_block": True  # Block high-severity findings
}
```

### **6.2 Decision Flow**
1. **No Findings** → `ALLOW`.
2. **Secret Key Found** → `BLOCK`.
3. **High Severity** → `BLOCK` (if configured).
4. **Otherwise** → `MASK`.

---

## **7. Logging**
### **7.1 Log Format**
```json
{
  "timestamp": "2025-07-20T12:00:00Z",
  "action": "MASK",
  "prompt": "Email: test@example.com",
  "masked_prompt": "[*** MASKED:pii_email ***]",
  "findings": [
    {
      "category": "pii_email",
      "match": "test@example.com"
    }
  ]
}
```
- Logs stored in `logs/incidents.jsonl`.

---

## **8. Development Guidelines**
### **8.1 Adding New Detection Rules**
1. **Extend `detection.py`**:
   ```python
   NEW_REGEX = re.compile(r"your_pattern")
   def detect_new_pattern(text):
       return _matches_to_findings(text, NEW_REGEX, "new_category", "high", "Description")
   ```
2. **Update `POLICY`** in `policy.py`:
   ```python
   POLICY["mask_categories"].add("new_category")
   ```

### **8.2 Testing**
- Use `tests/client_demo.py` for manual testing.
- Add unit tests for detection logic (e.g., `pytest`).

---

## **9. Deployment**
### **9.1 Local Deployment**
```bash
uvicorn app.proxy:app --host 0.0.0.0 --port 8000
```
- Accessible via `http://<your-ip>:8000`.

### **9.2 Docker (Optional)**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r tests/req.txt
CMD ["uvicorn", "app.proxy:app", "--host", "0.0.0.0", "--port", "8000"]
```
Build & run:
```bash
docker build -t dlp-proxy .
docker run -p 8000:8000 dlp-proxy
```

---

## **10. Troubleshooting**
| Issue | Solution |
|-------|----------|
| **Proxy not responding** | Check `uvicorn` logs for errors. |
| **False positives** | Adjust regex patterns in `detection.py`. |
| **Logs not generated** | Verify `logs/` directory permissions. |

---

## **11. License**
MIT License (see `LICENSE` file).

---
**Contributors**: Ragesh A
**Contact**: offi.rexain@gmail.com | ragesh18

---
This documentation ensures developers can **quickly set up, extend, and deploy** the GenAI DLP Proxy while maintaining security best practices.
