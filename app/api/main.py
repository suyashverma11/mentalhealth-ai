from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="MentalHealth-Detector-MVP", version="0.1")

class TextInput(BaseModel):
    text: str

class AnalyzeResult(BaseModel):
    risk_level: str
    score: Optional[float]
    highlights: List[str]
    rationale: str

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "mentalhealth-detector",
        "version": "0.1"
    }

@app.post("/analyze", response_model=AnalyzeResult)
async def analyze(payload: TextInput):
    text = payload.text.strip()

    if len(text) < 5:
        raise HTTPException(
            status_code=400,
            detail="Text too short to analyze."
        )

    # Day-1 simple heuristic model
    lowered = text.lower()
    keywords = ["sad", "tired", "hopeless", "anxious", "panic", "worthless"]
    highlights = [w for w in keywords if w in lowered]

    score = 0.0
    if highlights:
        score = min(1.0, 0.1 * len(highlights))

    if score >= 0.3:
        risk = "High"
    elif score >= 0.1:
        risk = "Medium"
    else:
        risk = "Low"

    justification = (
        "Heuristic analysis detected the following indicators: "
        + (", ".join(highlights) if highlights else "none")
    )

    return {
        "risk_level": risk,
        "score": score,
        "highlights": highlights,
        "rationale": justification
    }
