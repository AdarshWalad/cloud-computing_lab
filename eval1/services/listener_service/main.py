import os
import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = os.getenv("DB_PATH", "data/listeners.db")
SEED_LISTENERS = [
    ("Alice Smith", "alice@example.com", 1, 0),
    ("Bob Jones", "bob@example.com", 1, 1),
    ("Charlie Brown", "charlie@example.com", 1, 0),
    ("Diana Prince", "diana@example.com", 0, 0),
    ("Evan Wright", "evan@example.com", 1, 1),
]

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    with get_db() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS listeners (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, active INTEGER, is_premium INTEGER)")
        if conn.execute("SELECT COUNT(*) FROM listeners").fetchone()[0] == 0:
            conn.executemany("INSERT INTO listeners (name, email, active, is_premium) VALUES (?, ?, ?, ?)", SEED_LISTENERS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Listener Service", version="1.0", lifespan=lifespan)

class ListenerIn(BaseModel):
    name: str
    email: str
    active: bool
    is_premium: bool

def row_to_listener(row):
    return dict(row)

@app.get("/health")
def health():
    return {"service": "listener-service", "status": "healthy"}

@app.get("/listeners")
def get_listeners():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM listeners").fetchall()
    return [row_to_listener(r) for r in rows]

@app.get("/listeners/{listener_id}")
def get_listener(listener_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM listeners WHERE id = ?", (listener_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Listener not found")
    return row_to_listener(row)

@app.post("/listeners", status_code=201)
def add_listener(listener: ListenerIn):
    with get_db() as conn:
        cur = conn.execute("INSERT INTO listeners (name, email, active, is_premium) VALUES (?, ?, ?, ?)", 
                           (listener.name, listener.email, int(listener.active), int(listener.is_premium)))
    return get_listener(cur.lastrowid)
