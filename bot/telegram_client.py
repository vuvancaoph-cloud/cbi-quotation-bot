"""
Telegram Client — gửi tin nhắn qua Telegram Bot API
"""
import os
import httpx


def _api(method: str) -> str:
    return f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN', '')}/{method}"


async def send_message(chat_id: int, text: str, parse_mode: str = "HTML"):
    """Gửi tin nhắn text đến người dùng"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(_api("sendMessage"), json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        })
        data = resp.json()
        if not data.get("ok"):
            print(f"[telegram] Lỗi gửi tin: {data}")
        return data


async def send_typing(chat_id: int):
    """Hiện typing indicator"""
    async with httpx.AsyncClient(timeout=5) as client:
        await client.post(_api("sendChatAction"), json={
            "chat_id": chat_id,
            "action": "typing"
        })


async def set_webhook(webhook_url: str, secret: str = ""):
    """Đăng ký webhook URL với Telegram"""
    payload = {"url": webhook_url, "allowed_updates": ["message"]}
    if secret:
        payload["secret_token"] = secret
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(_api("setWebhook"), json=payload)
        return resp.json()


async def set_my_commands():
    """Đăng ký menu lệnh trong bot"""
    commands = [
        {"command": "start",   "description": "Bắt đầu / Giới thiệu bot"},
        {"command": "gia",     "description": "Tra giá: /gia van bi inox dn25"},
        {"command": "danhmuc", "description": "Xem nhóm sản phẩm"},
        {"command": "help",    "description": "Hướng dẫn sử dụng"},
        {"command": "lienhe",  "description": "Thông tin liên hệ CBI"},
    ]
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(_api("setMyCommands"), json={"commands": commands})
        return resp.json()
