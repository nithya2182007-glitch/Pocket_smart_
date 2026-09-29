import sqlite3, json
from pathlib import Path
from datetime import datetime, timezone

DB_PATH=Path("pocketsmart.db")

def db():
    c=sqlite3.connect(DB_PATH)
    c.row_factory=sqlite3.Row
    return c

def init_db():
    with db() as c:
        c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY,password_hash TEXT NOT NULL)")
        c.execute("CREATE TABLE IF NOT EXISTS history (id TEXT PRIMARY KEY,username TEXT NOT NULL,planner TEXT NOT NULL,request_json TEXT NOT NULL,response_json TEXT NOT NULL,created_at TEXT NOT NULL)")
        c.commit()

def create_user(username,password_hash):
    with db() as c:
        c.execute("INSERT INTO users VALUES (?,?)",(username,password_hash)); c.commit()

def get_user(username):
    with db() as c: return c.execute("SELECT * FROM users WHERE username=?",(username,)).fetchone()

def save_history(i,u,p,req,res):
    with db() as c:
        c.execute("INSERT INTO history VALUES (?,?,?,?,?,?)",(i,u,p,json.dumps(req),json.dumps(res),datetime.now(timezone.utc).isoformat())); c.commit()

def get_history(u):
    with db() as c: return [dict(x) for x in c.execute("SELECT * FROM history WHERE username=? ORDER BY created_at DESC",(u,)).fetchall()]

def get_recommendation(i,u):
    with db() as c: return c.execute("SELECT * FROM history WHERE id=? AND username=?",(i,u)).fetchone()
