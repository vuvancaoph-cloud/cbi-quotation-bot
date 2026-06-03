from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

from bot.handler import handle_update
from db.database import init_db
from db.migrate import run_migration

app = FastAPI()

@app.on_event("startup")
async def startup():
    init_db()
    run_migration()
    await _register_webhook()


async def _register_webhook():
    """Đăng ký webhook + menu lệnh với Telegram sau khi server khởi động"""
    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "").strip()
    token  = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not domain or not token:
        print("[startup] Chưa có RAILWAY_PUBLIC_DOMAIN hoặc TELEGRAM_BOT_TOKEN — bỏ qua đăng ký webhook.")
        return

    from bot.telegram_client import set_webhook, set_my_commands
    secret = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
    webhook_url = f"https://{domain}/webhook"

    result = await set_webhook(webhook_url, secret)
    if result.get("ok"):
        print(f"[startup] Webhook đã đăng ký: {webhook_url}")
    else:
        print(f"[startup] Lỗi đăng ký webhook: {result}")

    cmd_result = await set_my_commands()
    if cmd_result.get("ok"):
        print("[startup] Menu lệnh đã đăng ký.")
    else:
        print(f"[startup] Lỗi đăng ký menu lệnh: {cmd_result}")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(request: Request):
    secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    expected = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
    if expected and secret != expected:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)
    data = await request.json()
    await handle_update(data)
    return JSONResponse({"ok": True})

@app.get("/products/search")
def search(q: str = ""):
    if not q:
        return {"error": "Thieu ?q="}
    from bot.search import search_products
    results = search_products(q)
    return {"found": bool(results), "count": len(results),
            "results": [{"ma_hd": p["ma_hd"], "ten_hang": p["ten_hang"],
                         "gia_ban": p.get("gia_ban")} for p in results]}

@app.get("/admin/stats")
def stats():
    from db.crud import get_stats
    return get_stats()

@app.post("/admin/setup-webhook")
async def setup_webhook():
    """Gọi thủ công để đăng ký lại webhook (dùng khi đổi domain)"""
    await _register_webhook()
    return {"ok": True}

@app.post("/admin/reload-products")
def reload_products():
    """Reload Excel → DB → cache (dùng khi cập nhật giá)"""
    run_migration(force=True)
    return {"ok": True}
