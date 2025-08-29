import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

# rate limiting
RATE_WINDOW_MIN = int(os.getenv("RATE_WINDOW_MIN", "5"))
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "60"))

# DB
DB_PATH = os.getenv("DB_PATH", "data/runs.sqlite")

# auth
AUTH_TOKEN = os.getenv("AUTH_TOKEN")  # optional

# CORS for future browser UIs (not needed for Streamlit-server calls)
ALLOWED_ORIGINS = [o for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o]
