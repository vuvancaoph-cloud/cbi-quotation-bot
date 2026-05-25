"""
SQLite Database Setup
"""
import sqlite3
import os

DB_PATH = os.getenv("DATABASE_URL", "./cbi.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Tạo bảng nếu chưa tồn tại"""
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ma_hd       TEXT NOT NULL UNIQUE,
            ten_hang    TEXT NOT NULL,
            don_vi      TEXT,
            gia_ban     REAL,
            nhom        TEXT,
            aliases     TEXT DEFAULT '[]',
            updated_at  TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS quote_history (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            zalo_user_id    TEXT NOT NULL,
            session_id      TEXT,
            query_text      TEXT,
            products_found  TEXT DEFAULT '[]',
            created_at      TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS sessions (
            session_id      TEXT PRIMARY KEY,
            zalo_user_id    TEXT NOT NULL UNIQUE,
            context         TEXT DEFAULT '{}',
            last_active     TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE INDEX IF NOT EXISTS idx_products_ma   ON products(ma_hd);
        CREATE INDEX IF NOT EXISTS idx_history_user  ON quote_history(zalo_user_id);
        CREATE INDEX IF NOT EXISTS idx_history_date  ON quote_history(created_at);
    """)
    conn.commit()
    conn.close()
    print("[db] Khởi tạo DB xong.")
