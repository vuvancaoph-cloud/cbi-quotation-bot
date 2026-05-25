"""
Bot Handler — phân tích tin nhắn và điều hướng xử lý
"""
import re
from bot.search import search_products, load_cache
from bot.ai_client import analyze_with_ai
from bot.zalo_client import send_message
from bot.session import get_session, update_session
from bot.formatter import format_single, format_list, format_not_found, format_help, format_catalog, format_contact
from db.crud import log_quote


async def handle_message(user_id: str, text: str):
    """Xử lý tin nhắn đến từ người dùng Zalo"""
    text = text.strip()
    if not text:
        return

    # 1. Kiểm tra lệnh đặc biệt
    cmd = normalize_cmd(text)
    if cmd in ("/help", "/?", "help"):
        await send_message(user_id, format_help())
        return
    if cmd in ("/danh muc", "danh muc"):
        await send_message(user_id, format_catalog())
        return
    if cmd in ("/lien he", "lien he"):
        await send_message(user_id, format_contact())
        return

    # 2. Lấy session
    session = get_session(user_id)

    # 3. Tách nhiều sản phẩm
    queries = split_queries(text)

    results = []
    not_found = []

    for query in queries:
        # 4. Tìm bằng fuzzy search
        found = search_products(query)
        if found:
            results.extend(found)
        else:
            # 5. Gọi AI nếu fuzzy thất bại
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

    # 6. Format và gửi reply
    if not results and not_found:
        reply = format_not_found(text)
    elif len(results) == 1:
        reply = format_single(results[0])
    else:
        reply = format_list(results, not_found)

    await send_message(user_id, reply)

    # 7. Cập nhật session + log
    update_session(user_id, text, results)
    log_quote(user_id, text, results)


def normalize_cmd(text: str) -> str:
    return text.lower().strip()


def split_queries(text: str) -> list:
    """Tách câu hỏi nhiều sản phẩm"""
    parts = re.split(r'[,\n]|(?:\s+và\s+)', text, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 2]
