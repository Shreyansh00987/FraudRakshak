"""
fraudRakshak - FastAPI AI Microservice
Handles message analysis, voice queries, and live scam call copilot evaluations.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from nlp_engine import analyze_scam_message, voice_query_advisor, evaluate_copilot_turn

app = FastAPI(
    title="fraudRakshak AI/NLP Microservice",
    description="Multilingual Scam Shield & Indian IOC Analyzer",
    version="1.0.0"
)

# Enable CORS for frontend and backend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    text: str
    sender: Optional[str] = None


class VoiceQueryRequest(BaseModel):
    query: str


class CopilotEvaluateRequest(BaseModel):
    transcript: List[Dict[str, str]] = []
    current_turn: str
    speaker: str = "scammer"
    scenario: str = "sbi_kyc"


@app.get("/health")
@app.get("/api/nlp/health")
def health_check():
    return {
        "status": "healthy",
        "service": "fraudRakshak-nlp-engine",
        "version": "1.0.0",
        "supported_languages": ["Hinglish", "Hindi", "English"],
        "active_models": ["Indian Phonics Regex Heuristics", "IOC Domain Harvester", "Rule-based Scam Classifier"]
    }


@app.post("/api/nlp/analyze")
def analyze_endpoint(req: AnalyzeRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    try:
        result = analyze_scam_message(req.text, req.sender)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/nlp/voice-query")
def voice_query_endpoint(req: VoiceQueryRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Voice query cannot be empty.")
    try:
        result = voice_query_advisor(req.query)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/nlp/copilot-evaluate")
def copilot_evaluate_endpoint(req: CopilotEvaluateRequest):
    if not req.current_turn or not req.current_turn.strip():
        raise HTTPException(status_code=400, detail="Current turn cannot be empty.")
    try:
        result = evaluate_copilot_turn(req.transcript, req.current_turn, req.scenario)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)
