"""
Session Manager — quản lý ngữ cảnh hội thoại (30 phút)
"""
import json
import uuid
from datetime import datetime, timedelta
from db.database import get_connection

SESSION_TIMEOUT_MINUTES = 30


def get_session(user_id: str) -> dict:
    """Lấy session hiện tại hoặc tạo mới nếu hết hạn"""
    conn = get_connection()
    row = conn.execute(
        "SELECT session_id, context, last_active FROM sessions WHERE zalo_user_id = ?",
        (user_id,)
    ).fetchone()

    if row:
        last_active = datetime.fromisoformat(row["last_active"])
        if datetime.now() - last_active < timedelta(minutes=SESSION_TIMEOUT_MINUTES):
            conn.close()
            return json.loads(row["context"] or "{}")

    # Tạo session mới
    session_id = str(uuid.uuid4())
    conn.execute(
        "INSERT OR REPLACE INTO sessions (session_id, zalo_user_id, context) VALUES (?, ?, ?)",
        (session_id, user_id, "{}")
    )
    conn.commit()
    conn.close()
    return {}


def update_session(user_id: str, query: str, results: list):
    """Cập nhật ngữ cảnh sau mỗi tin nhắn"""
    context = {
        "last_query": query,
        "last_products": [p["ma_hd"] for p in results]
    }
    conn = get_connection()
    conn.execute(
        """UPDATE sessions
           SET context = ?, last_active = datetime('now','localtime')
           WHERE zalo_user_id = ?""",
        (json.dumps(context, ensure_ascii=False), user_id)
    )
    conn.commit()
    conn.close()
