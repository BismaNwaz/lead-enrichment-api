from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

from scraper import fetch_website_text
from enrichment import enrich_company_data
from database import SessionLocal, Lead

app = FastAPI(title="Lead Enrichment API")

class EnrichRequest(BaseModel):
    url: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/enrich")
def enrich_lead(request: EnrichRequest):
    db = SessionLocal()
    existing = db.query(Lead).filter(Lead.url == request.url).first()
    if existing:
        db.close()
        return json.loads(existing.data_json)

    try:
        text = fetch_website_text(request.url)
        data = enrich_company_data(text)
    except Exception as e:
        db.close()
        raise HTTPException(status_code=400, detail=str(e))

    lead = Lead(
        url=request.url,
        company_name=data.get("company_name"),
        industry=data.get("industry"),
        summary=data.get("summary"),
        data_json=json.dumps(data)
    )
    db.add(lead)
    db.commit()
    db.close()
    return data