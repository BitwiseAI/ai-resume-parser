import logging
from fastapi import APIRouter, Header, HTTPException, BackgroundTasks
from typing import Optional
from ..models.schemas import ParseRequest, ParseResult, BatchParseRequest, BatchParseResult
from ..services.parser import parse_resume_job
from ..storage.db import save_run, list_runs, get_cached
from ..core.config import AUTH_TOKEN, MODEL_NAME

router = APIRouter()
log = logging.getLogger("resume-parser")

def _check_auth(authorization: Optional[str]):
    if AUTH_TOKEN and authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/parse", response_model=ParseResult)
def parse(req: ParseRequest, authorization: Optional[str] = Header(default=None)):
    _check_auth(authorization)
    cache = get_cached(req.resume_text, req.job_text)
    if cache:
        return ParseResult(**cache)

        data = parse_resume_job(req.resume_text, req.job_text, model=req.model, temperature=req.temperature)
    usage = data.pop("_usage", None)
    if usage:
        log.info(f"tokens: {usage}")
    obj = ParseResult(**data)
    save_run(req.resume_text, req.job_text, obj.skills, obj.score, obj.reasons, req.model or MODEL_NAME)
    return obj

@router.get("/runs")
def runs(limit: int = 50, authorization: Optional[str] = Header(default=None)):
    _check_auth(authorization)
    return {"items": list_runs(limit=limit)}


def _do_parse_and_save(resume_text: str, job_text: str, model: str, temperature: float):
        data = parse_resume_job(resume_text, job_text, model=model, temperature=temperature)
    usage = data.pop("_usage", None)
    if usage:
        log.info(f"tokens: {usage}")
    obj = ParseResult(**data)
    save_run(resume_text, job_text, obj.skills, obj.score, obj.reasons, model or MODEL_NAME)


@router.post("/parse_async")
def parse_async(req: ParseRequest, background: BackgroundTasks, authorization: Optional[str] = Header(default=None)):
    _check_auth(authorization)
    # enqueue background job
    background.add_task(_do_parse_and_save, req.resume_text, req.job_text, req.model, req.temperature)
    return {"status": "accepted"}


@router.post("/batch_parse", response_model=BatchParseResult)
def batch_parse(req: BatchParseRequest, authorization: Optional[str] = Header(default=None)):
    _check_auth(authorization)
    out = []
    for resume_text in req.resumes:
        cache = get_cached(resume_text, req.job_text)
        if cache:
            obj = ParseResult(**cache)
        else:
                        data = parse_resume_job(resume_text, req.job_text)
            usage = data.pop("_usage", None)
            if usage:
                log.info(f"tokens: {usage}")
            obj = ParseResult(**data)
            save_run(resume_text, req.job_text, obj.skills, obj.score, obj.reasons, MODEL_NAME)
        out.append(obj)
    return {"items": out}


