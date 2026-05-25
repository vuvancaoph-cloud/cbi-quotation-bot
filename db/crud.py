"""
CRUD operations — tương tác với SQLite
"""
import json
from db.database import get_connection


def get_all_products() -> list:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM products ORDER BY ten_hang").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_products_summary() -> list:
    """Chỉ lấy tên + mã — dùng cho AI prompt (nhỏ gọn hơn)"""
    conn = get_connection()
    rows = conn.execute("SELECT ma_hd, ten_hang FROM products ORDER BY ten_hang").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def log_quote(user_id: str, query: str, products: list):
    """Ghi lịch sử báo giá"""
    found_json = json.dumps(
        [{"ma_hd": p["ma_hd"], "ten_hang": p["ten_hang"], "gia_ban": p.get("gia_ban")}
         for p in products],
        ensure_ascii=False
    )
    conn = get_connection()
    conn.execute(
        "INSERT INTO quote_history (zalo_user_id, query_text, products_found) VALUES (?, ?, ?)",
        (user_id, query, found_json)
    )
    conn.commit()
    conn.close()


def get_stats() -> dict:
    conn = get_connection()
    total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    total_queries  = conn.execute("SELECT COUNT(*) FROM quote_history").fetchone()[0]
    today_queries  = conn.execute(
        "SELECT COUNT(*) FROM quote_history WHERE date(created_at) = date('now','localtime')"
    ).fetchone()[0]
    top_queries = conn.execute(
        """SELECT query_text, COUNT(*) as cnt
           FROM quote_history
           GROUP BY query_text
           ORDER BY cnt DESC LIMIT 10"""
    ).fetchall()
    conn.close()
    return {
        "total_products": total_products,
        "total_queries":  total_queries,
        "today_queries":  today_queries,
        "top_queries": [{"query": r[0], "count": r[1]} for r in top_queries]
    }
