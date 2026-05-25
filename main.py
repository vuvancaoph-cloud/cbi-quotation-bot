"""
CBI Quotation Bot — FastAPI Entry Point
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

from bot.handler import handle_message
from db.database import init_db
from db.migrate import run_migration

app = FastAPI(title="CBI Quotation Bot", version="1.0.0")


@app.on_event("startup")
async def startup():
    """Khởi động: tạo DB + import Excel"""
    init_db()
    run_migration()
    print("[startup] Sẵn sàng!")


@app.get("/health")
def health():
    return {"status": "ok", "service": "cbi-quotation-bot"}


@app.post("/webhook/zalo")
async def zalo_webhook(request: Request):
    """Nhận event từ Zalo OA"""
    body = await request.body()

    # Xác thực chữ ký Zalo
    mac = request.headers.get("X-ZEvent-Mac", "")
    secret = os.getenv("ZALO_APP_SECRET", "")
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    if secret and not hmac.compare_digest(mac, expected):
        raise HTTPException(status_code=403, detail="Invalid signature")

    data = await request.json()
    event_type = data.get("event_name", "")

    if event_type == "user_send_text":
        user_id = data["sender"]["id"]
        message = data["message"]["text"]
        await handle_message(user_id, message)

    return JSONResponse({"status": "ok"})


@app.post("/admin/reload")
async def reload_db():
    """Reload CSDL từ Excel — không cần restart"""
    run_migration(force=True)
    from bot.search import load_cache
    load_cache()
    return {"status": "reloaded"}


@app.get("/admin/stats")
def stats():
    from db.crud import get_stats
    return get_stats()
