from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import sqlite3
import jwt
import os
import platform
import socket

app = FastAPI()

SECRET_KEY = "supersecret"
DB_PATH = "./users.db"

# Database setup
@app.on_event("startup")
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
    conn.commit()
    conn.close()

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "secret_key_hint": SECRET_KEY[:5] + "*****"
    }

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        token = jwt.encode({"user_id": user[0], "username": user[1]}, SECRET_KEY, algorithm="HS256")
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/profile/{user_id}")
async def profile(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {"id": user[0], "username": user[1]}
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/exec")
async def exec_cmd(request: Request):
    data = await request.json()
    cmd = data.get("cmd")
    os.system(f"echo {cmd} > /tmp/output.log")
    return {"message": "Command executed"}
