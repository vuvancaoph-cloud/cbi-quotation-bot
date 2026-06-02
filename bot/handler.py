"""
Bot Handler — phân tích tin nhắn Telegram và điều hướng xử lý
"""
import re
from bot.search import search_products
from bot.ai_client import analyze_with_ai
from bot.telegram_client import send_message, send_typing
from bot.session import get_session, update_session
from bot.formatter import (format_start, format_single, format_list,
                            format_not_found, format_help, format_catalog, format_contact)
from db.crud import log_quote


async def handle_update(update: dict):
    """Entry point xử lý mọi update từ Telegram"""
    message = update.get("message") or update.get("edited_message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()
    if not text:
        return

    if text.startswith("/"):
        await handle_command(chat_id, text)
    else:
        await handle_query(chat_id, text)


async def handle_command(chat_id: int, text: str):
    """Xử lý lệnh /start /help /danhmuc /lienhe /gia"""
    parts = text.split()
    cmd = parts[0].lower().split("@")[0]
    args = " ".join(parts[1:]).strip()

    if cmd == "/start":
        await send_message(chat_id, format_start())

    elif cmd in ("/help", "/huongdan"):
        await send_message(chat_id, format_help())

    elif cmd in ("/danhmuc", "/dm"):
        await send_message(chat_id, format_catalog())

    elif cmd in ("/lienhe", "/lh"):
        await send_message(chat_id, format_contact())

    elif cmd == "/gia":
        if args:
            await handle_query(chat_id, args)
        else:
            await send_message(chat_id,
                "Dùng: /gia [tên sản phẩm]\n"
                "Ví dụ: <code>/gia van bi inox dn25</code>")


async def handle_query(chat_id: int, text: str):
    """Xử lý câu hỏi tra giá"""
    await send_typing(chat_id)

    session = get_session(str(chat_id))
    queries = split_queries(text)
    results = []
    not_found = []

    for query in queries:
        found = search_products(query)
        if found:
            results.extend(found)
        else:
            ai_result = await analyze_with_ai(query, session)
            if ai_result:
                for item in ai_result:
                    product = search_products(item.get("ma_hd", ""), by_code=True)
                    if product:
                        results.extend(product)
                    else:
                        not_found.append(query)
            else:
                not_found.append(query)

    # Loại trùng
    seen = set()
    unique = []
    for p in results:
        if p["ma_hd"] not in seen:
            unique.append(p)
            seen.add(p["ma_hd"])

    if not unique:
        reply = format_not_found(text)
    elif len(unique) == 1 and not not_found:
        reply = format_single(unique[0])
    else:
        reply = format_list(unique, not_found)

    await send_message(chat_id, reply)
    update_session(str(chat_id), text, unique)
    log_quote(str(chat_id), text, unique)


def split_queries(text: str) -> list:
    parts = re.split(r'[,\n]|\bvà\b', text, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 2]
