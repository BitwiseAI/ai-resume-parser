import sqlite3, threading
from ..core.config import DB_PATH

_lock = threading.Lock()

def init_db():
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
