import ssl
import socket
import joblib
import pandas as pd
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .database import log_scan_to_cloud 

app = FastAPI()

# Enable CORS for Mobile App and Extension communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the AI Model
try:
    model = joblib.load("backend/phish_model.pkl")
    print("AI Security Engine: ONLINE")
except Exception as e:
    model = None
    print(f"Warning: AI Model Offline ({e}). using Simulation Mode.")

class MessageData(BaseModel):
    text: str  # This can be a full WhatsApp message or SMS
    source: str = "mobile_app"

def extract_url_from_text(text):
    """
    REGULAR EXPRESSION: Extracts URLs from within a block of message text.
    Essential for WhatsApp/SMS interception.
    """
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None

def check_ssl(hostname):
    """Layer 2: Real-time SSL Certificate Verification"""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssock.getpeercert()
                return True, "Valid SSL Certificate"
    except Exception:
        return False, "Invalid or Missing SSL Certificate"

def extract_features(url):
    """Layer 1: Lexical Feature Extraction (ML Input)"""
    return {
        "url_length": len(url),
        "dot_count": url.count('.'),
        "has_at": 1 if '@' in url else 0,
        "has_dash": 1 if '-' in url else 0
    }

@app.post("/analyze")
async def analyze_input(data: MessageData):
    """
    UNIVERSAL ENDPOINT: Processes both direct URLs and full messages 
    from WhatsApp, SMS, or Email.
    """
    raw_text = data.text
    
    # Check if input is a full message or just a URL
    url = extract_url_from_text(raw_text) if "http" in raw_text else raw_text
    
    if not url or "." not in url:
        return {"status": "NO_LINK", "risk_score": 0, "reasons": "No suspicious links detected in text."}

    # 1. SSL Analysis
    hostname = url.split("//")[-1].split("/")[0].split(":")[0]
    ssl_valid, ssl_msg = check_ssl(hostname)
    
    # 2. AI Machine Learning Analysis
    features = extract_features(url)
    if model:
        try:
            df = pd.DataFrame([features])
            df = df[["url_length", "dot_count", "has_at", "has_dash"]] 
            prediction = model.predict(df)[0]
            risk_score = model.predict_proba(df)[0][1] * 100
        except:
            prediction, risk_score = 0, 50.0
    else:
        prediction, risk_score = (1, 85.0) if not ssl_valid else (0, 10.0)

    # 3. Final Verdict
    status = "PHISHING" if (prediction == 1 or risk_score > 75) else "SAFE"
    reason = f"{ssl_msg}. AI Risk Analysis: {risk_score:.1f}% suspicious patterns."

    # 4. Cloud Logging (Telemetry for Dashboard)
    log_scan_to_cloud(url, status, risk_score, reason)

    return {
        "status": status,
        "risk_score": round(risk_score, 2),
        "reasons": reason,
        "url": url,
        "intercepted_from": data.source
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)