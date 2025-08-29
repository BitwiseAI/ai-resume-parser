from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from ..models.schemas import ParseRequest, ParseResult
from ..services.parser import parse_resume_job
from ..storage.db import save_run, list_runs
from ..core.config import AUTH_TOKEN, MODEL_NAME

router = APIRouter()

def _check_auth(authorization: Optional[str]):
    if AUTH_TOKEN and authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/parse", response_model=ParseResult)
def parse(req: ParseRequest, authorization: Optional[str] = Header(default=None)):
    _check_auth(authorization)
    data = parse_resume_job(req.resume_text, req.job_text, model=req.model, temperature=req.temperature)
    obj = ParseResult(**data)
    save_run(req.resume_text, req.job_text, obj.skills, obj.score, obj.reasons, req.model or MODEL_NAME)
    return obj

@router.get("/runs")
def runs(limit: int = 50, authorization: Optional[str] = Header(default=None)):
    _check_auth(authorization)
    return {"items": list_runs(limit=limit)}
