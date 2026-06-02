from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
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

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    await handle_update(data)
    return JSONResponse({"ok": True})

@app.get("/products/search")
def search(q: str = ""):
    from bot.search import search_products
    results = search_products(q)
    return {"found": bool(results), "count": len(results),
            "results": [{"ma_hd": p["ma_hd"], "ten_hang": p["ten_hang"],
                         "gia_ban": p.get("gia_ban")} for p in results]}
