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
git clone https://github.com/your-username/genai-dlp-guard.git
cd genai-dlp-guard

 
