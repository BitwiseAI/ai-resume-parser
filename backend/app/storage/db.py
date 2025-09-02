import sqlite3, threading, hashlib, os
from ..core.config import DB_PATH

_lock = threading.Lock()

def _ensure_db_dir():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)


def init_db():
    _ensure_db_dir()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS runs(
              id INTEGER PRIMARY KEY,
              ts DATETIME DEFAULT CURRENT_TIMESTAMP,
              resume TEXT,
              job TEXT,
              skills TEXT,
              score INTEGER,
              reasons TEXT,
              model TEXT
            )
        """)

def save_run(resume, job, skills, score, reasons, model):
    _ensure_db_dir()
    with _lock, sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT INTO runs(resume,job,skills,score,reasons,model) VALUES(?,?,?,?,?,?)",
            (resume, job, ",".join(skills), int(score), reasons, model)
        )

def list_runs(limit=50):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.execute(
            "SELECT id,ts,score,skills,model FROM runs ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

def get_cached(resume: str, job: str):
    """Return the most recent match from the DB if it exists"""
    with sqlite3.connect(DB_PATH) as con:
        cur = con.execute("SELECT score, skills, reasons, model FROM runs WHERE resume = ? AND job = ? ORDER BY id DESC LIMIT 1", (resume, job))
        row = cur.fetchone()
        if not row:
            return None
        score, skills, reasons, model = row
        # Guard against empty skills string
        skill_list = skills.split(",") if skills else []
        return {"skills": skill_list, "score": int(score), "reasons": reasons, "model": model}
