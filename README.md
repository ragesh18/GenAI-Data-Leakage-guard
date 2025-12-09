# 🛡️ GenAI Data Leakage Guard
A local GenAI Data Loss Prevention (DLP) proxy that detects, masks, and blocks sensitive information in AI prompts to prevent accidental data leakage.
---




## 📌 Problem Statement

With the rapid adoption of Generative AI tools (ChatGPT, Claude, Gemini, etc.), users may unknowingly paste sensitive information such as:

- API keys and credentials  
- Passwords and secrets  
- Personal Identifiable Information (PII)  
- Source code or confidential business data  

Directly into GenAI tools.

Traditional Data Loss Prevention (DLP) solutions focus on email, files, or web uploads, but modern security requires **DLP for GenAI prompts**.

There is a need for a **local mechanism** that inspects prompts *before* they reach a GenAI system and prevents data leakage.

---

## 🎯 Project Objective

The main goal of this project is to build a **GenAI Data Leakage Guard** that:

- Acts as a **proxy** between the user and GenAI
- Detects sensitive data inside prompts
- Applies security policies:
  - **ALLOW**
  - **MASK**
  - **BLOCK**
- Logs all sensitive events for audit and analysis

---

## 🔍 What This Project Detects

- ✅ Email addresses  
- ✅ Phone numbers  
- ✅ Aadhaar-like / Passport-like IDs (pattern based)  
- ✅ High-entropy secrets & API keys  
- ✅ Source-code-like patterns  

---

## 🧠 How It Works (High Level)
```User enters a prompt```
        --> 
```Client (client_demo.py)```
        -->
```GenAI DLP Guard (FastAPI Proxy)```
        -->
```Detection Engine```
        -->
```Policy Engine```
     -->
```Decision Taken`
(ALLOW / MASK / BLOCK)```
        -->
``` Response returned to user```



## 📂 Project Structure

```
genai-dlp-guard/
├── app/
│   ├── proxy.py             # Main DLP proxy API
│   ├── detection.py         # PII, secret, and code detection logic
│   ├── policy.py            # Allow / Mask / Block decisions
│   ├── logging_utils.py     # Incident logging
├── logs/
│   └── incidents.jsonl      # Logged DLP incidents
├── data/
│   └── synthetic_prompts.csv
├── tests/                   # (Optional) Detection tests
├── client_demo.py           # Simple client to send prompts
├── requirements.txt
└── README.md
```

---

## ⚙️ Technologies Used

| Component | Technology |
|--------|-----------|
| Programming Language | Python |
| Backend Framework | FastAPI |
| API Server | Uvicorn |
| Detection Technique | Regex + Entropy Analysis |
| Logging | JSON Lines |
| Platform | Linux / Ubuntu |

---

## ✅ Requirements

- Python **3.9 or later**
- pip
- Virtual environment support

Python dependencies (via `requirements.txt`):
- fastapi  
- uvicorn  
- pydantic  
- requests  

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ragesh18/GenAI-Data-Leakage-guard.git

cd genai-dlp-guard
```
### 2️⃣ Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3️⃣ Install Required Packages
```bash
pip3 install -r requirements.txt
```

## ▶️ Running the Project
  - Step 1: Start the DLP Proxy Server
```bash
uvicorn app.proxy:app --reload
```
Expected output:
```nginx
Uvicorn running on http://127.0.0.1:8000
```
  - Step 2: Check Server Status
Open in browser:
```bash
http://localhost:8000/health
```
Response:
```bash
{"status":"ok"}
```
- Step 3: Use API Documentation
Open:
```bash
http://localhost:8000/docs
```
  - **Select POST /chat**
  - **Click Try it out**

Example input:
```json
{
  "prompt": "My email is user@gmail.com please help me"
}
```
- Step 4 (Optional): Use Client Demo
In a new terminal:
```bash
source venv/bin/activate
python client_demo.py
```
You can type prompts interactively.

---

Example Results
## ✅ Allowed Prompt
```pgsql
Explain SQL Injection.
```
**Result**: Prompt allowed and response returned.

## ⚠️ Masked Prompt
```kotlin
My email is test@gmail.com
```
**Result**: Email masked before processing.

## ❌ Blocked Prompt
```vbnet
My API key is sk-123456SECRET
```
**Result**: Prompt blocked and warning shown.

## 📄 Logging & Auditing
All detected incidents are stored in:
```bash
logs/incidents.jsonl
```
Each log entry includes:
  - Timestamp
  - Action taken (ALLOW / MASK / BLOCK)
  - Detection category
  - Prompt snippet (partial text)

---
    
## ✅ Advantages

- Prevents accidental data leakage to GenAI tools

- Implements real-world DLP concepts

- Works locally (privacy-friendly)

- Simple and extendable architecture

- Ideal for academic and cybersecurity projects

## ⚠️ Limitations

- Rule-based detection may cause false positives

- Text prompts only

- GenAI response is simulated

- Not production-hardened
