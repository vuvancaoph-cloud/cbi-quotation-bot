"""
CBI Quotation Bot — FastAPI Entry Point (Telegram)
"""
from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

from bot.handler import handle_update
from db.database import init_db
from db.migrate import run_migration

app = FastAPI(title="CBI Quotation Bot", version="2.0.0")

WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")


@app.on_event("startup")
async def startup():
    init_db()
    run_migration()
    # Đăng ký lệnh menu Telegram
    try:
        from bot.telegram_client import set_my_commands
        await set_my_commands()
    except Exception as e:
        print(f"[startup] Không đăng ký được commands: {e}")
    print("[startup] CBI Bot sẵn sàng!")


@app.get("/health")
def health():
    return {"status": "ok", "platform": "telegram", "service": "cbi-quotation-bot"}


@app.post("/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(default="")
):
    """Nhận update từ Telegram"""
    # Xác thực secret token
    if WEBHOOK_SECRET and x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    update = await request.json()
    await handle_update(update)
    return JSONResponse({"ok": True})


@app.get("/setup/webhook")
async def setup_webhook():
    """Đăng ký webhook URL với Telegram — gọi 1 lần sau khi deploy"""
    base_url = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")
    if not base_url:
        return {"error": "Chưa có RAILWAY_PUBLIC_DOMAIN"}
    webhook_url = f"https://{base_url}/webhook"
    from bot.telegram_client import set_webhook
    result = await set_webhook(webhook_url, WEBHOOK_SECRET)
    return result


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


@app.get("/products/search")
def search(q: str = ""):
    if not q:
        return {"error": "Thiếu ?q=tên_sản_phẩm"}
    from bot.search import search_products
    results = search_products(q)
    return {
        "found": bool(results),
        "query": q,
        "count": len(results),
        "results": [
            {"ma_hd": p["ma_hd"], "ten_hang": p["ten_hang"],
             "don_vi": p.get("don_vi"), "gia_ban": p.get("gia_ban")}
            for p in results
        ]
    }
