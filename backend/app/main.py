from fastapi import FastAPI
from dotenv import load_dotenv
from .core.logging import setup_logging, access_log_middleware
from .storage.db import init_db
from .api.routes import router as api_router

load_dotenv()
setup_logging()
app = FastAPI(title="Resume ↔ JD Parser API")
app.middleware("http")(access_log_middleware)
app.include_router(api_router)

@app.on_event("startup")
def on_startup():
    init_db()
