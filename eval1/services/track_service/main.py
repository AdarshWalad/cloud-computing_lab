import os
import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = os.getenv("DB_PATH", "data/tracks.db")
SEED_TRACKS = [
    ("Bohemian Rhapsody", "Queen", 0),
    ("Shape of You", "Ed Sheeran", 0),
    ("Blinding Lights", "The Weeknd", 0),
    ("Hotel California", "Eagles", 0),
    ("Watermelon Sugar", "Harry Styles", 0),
    ("Stairway to Heaven", "Led Zeppelin", 1),
    ("Smells Like Teen Spirit", "Nirvana", 0),
    ("Rolling in the Deep", "Adele", 0),
    ("Imagine", "John Lennon", 1),
    ("Hey Jude", "The Beatles", 0),
]

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    with get_db() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tracks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, artist TEXT, is_premium_only INTEGER)")
        if conn.execute("SELECT COUNT(*) FROM tracks").fetchone()[0] == 0:
            conn.executemany("INSERT INTO tracks (title, artist, is_premium_only) VALUES (?, ?, ?)", SEED_TRACKS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Track Service", version="1.0", lifespan=lifespan)

class TrackIn(BaseModel):
    title: str
    artist: str
    is_premium_only: bool

def row_to_track(row):
    return dict(row)

@app.get("/health")
def health():
    return {"service": "track-service", "status": "healthy"}

@app.get("/tracks")
def get_tracks():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM tracks").fetchall()
    return [row_to_track(r) for r in rows]

@app.get("/tracks/{track_id}")
def get_track(track_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM tracks WHERE id = ?", (track_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return row_to_track(row)

@app.post("/tracks", status_code=201)
def add_track(track: TrackIn):
    with get_db() as conn:
        cur = conn.execute("INSERT INTO tracks (title, artist, is_premium_only) VALUES (?, ?, ?)", 
                           (track.title, track.artist, int(track.is_premium_only)))
    return get_track(cur.lastrowid)
