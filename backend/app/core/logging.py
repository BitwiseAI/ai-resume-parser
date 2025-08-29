import logging, sys, time
from collections import deque
from datetime import datetime, timedelta
from typing import Dict
from fastapi import Request
from starlette.responses import JSONResponse
from .config import RATE_WINDOW_MIN, RATE_LIMIT

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
        stream=sys.stdout,
    )

_requests: Dict[str, deque] = {}
WINDOW = timedelta(minutes=RATE_WINDOW_MIN)

def allow(ip: str) -> bool:
    dq = _requests.setdefault(ip, deque())
    now = datetime.utcnow()
    while dq and (now - dq[0]) > WINDOW:
        dq.popleft()
    if len(dq) >= RATE_LIMIT:
        return False
    dq.append(now)
    return True

async def access_log_middleware(request: Request, call_next):
    log = logging.getLogger("resume-parser")
    ip = request.client.host if request.client else "unknown"
    path = request.url.path
    start = time.time()

    if not allow(ip):
        return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)

    try:
        resp = await call_next(request)
        ms = int((time.time() - start) * 1000)
        log.info(f"{ip} {request.method} {path} -> {resp.status_code} {ms}ms")
        return resp
    except Exception as e:
        ms = int((time.time() - start) * 1000)
        log.exception(f"{ip} {request.method} {path} -> 500 {ms}ms ERROR: {e}")
        raise
