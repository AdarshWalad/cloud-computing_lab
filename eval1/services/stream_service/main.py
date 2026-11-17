import os
import sqlite3
import httpx
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = os.getenv("DB_PATH", "data/streams.db")
TRACK_URL = os.getenv("TRACK_SERVICE_URL", "http://127.0.0.1:8001")
LISTENER_URL = os.getenv("LISTENER_SERVICE_URL", "http://127.0.0.1:8002")

client = httpx.Client(timeout=5.0)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    with get_db() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS streams (id INTEGER PRIMARY KEY AUTOINCREMENT, listener_id INTEGER, track_id INTEGER, stream_time REAL)")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Stream Service", version="1.0", lifespan=lifespan)

class StreamIn(BaseModel):
    listener_id: int
    track_id: int

def call(method, url, **kwargs):
    try:
        return client.request(method, url, **kwargs)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Cannot reach {url}: {exc.__class__.__name__}")

def fetch_track(track_id):
    r = call("GET", f"{TRACK_URL}/tracks/{track_id}")
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="Track not found")
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Track Service returned an error")
    return r.json()

def fetch_listener(listener_id):
    r = call("GET", f"{LISTENER_URL}/listeners/{listener_id}")
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="Listener not found")
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Listener Service returned an error")
    return r.json()

@app.get("/health")
def health():
    return {"service": "stream-service", "status": "healthy"}

@app.get("/services/status")
def services_status():
    status = {"stream-service": "healthy"}
    for name, url in [("track-service", TRACK_URL), ("listener-service", LISTENER_URL)]:
        try:
            r = client.get(f"{url}/health")
            status[name] = r.json().get("status", "unknown") if r.status_code == 200 else "error"
        except httpx.RequestError:
            status[name] = "unreachable"
    return status

@app.get("/stream/check")
def check_stream(listener_id: int, track_id: int):
    listener = fetch_listener(listener_id)
    track = fetch_track(track_id)
    
    can_stream = bool(listener["active"] and (listener["is_premium"] or not track["is_premium_only"]))
    
    return {
        "listener": listener["name"], 
        "track": track["title"],
        "listener_active": listener["active"], 
        "listener_premium": listener["is_premium"],
        "track_premium_only": track["is_premium_only"],
        "can_stream": can_stream
    }

@app.post("/stream", status_code=201)
def log_stream(req: StreamIn):
    listener = fetch_listener(req.listener_id)
    if not listener["active"]:
        raise HTTPException(status_code=400, detail="Listener is not active")
    
    track = fetch_track(req.track_id)
    if track["is_premium_only"] and not listener["is_premium"]:
        raise HTTPException(status_code=409, detail="Track is premium only and listener is not premium")

    with get_db() as conn:
        cur = conn.execute("INSERT INTO streams (listener_id, track_id, stream_time) VALUES (?, ?, ?)",
                           (req.listener_id, req.track_id, time.time()))
        stream_id = cur.lastrowid
        
    return {
        "stream_id": stream_id, 
        "listener": listener["name"], 
        "track": track["title"]
    }

@app.get("/streams")
def get_streams():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM streams ORDER BY id DESC LIMIT 50").fetchall()
    return [dict(r) for r in rows]
