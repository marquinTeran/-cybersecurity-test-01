from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import sqlite3
import jwt
import os
import platform
import socket
import bcrypt

load_dotenv()
ENV = os.getenv("ENV", "prod")
app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set in environment variables")
DB_PATH = "./users.db"

# Database setup
@app.on_event("startup")
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
    if ENV == "dev":
        hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute(
            "INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', ?)",
            (hashed_password,)
        )
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

    query = "SELECT * FROM users WHERE username = ?"
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
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
