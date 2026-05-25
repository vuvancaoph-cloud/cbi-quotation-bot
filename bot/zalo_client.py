"""
Zalo Client — gửi tin nhắn qua Zalo OA API
"""
import os
import httpx

ZALO_API_URL = "https://openapi.zalo.me/v3.0/oa/message/cs"


async def send_message(user_id: str, text: str):
    """Gửi tin nhắn text đến người dùng Zalo"""
    token = os.getenv("ZALO_OA_ACCESS_TOKEN", "")
    if not token:
        print(f"[zalo] Chưa có OA token. Message: {text[:50]}")
        return

    payload = {
        "recipient": {"user_id": user_id},
        "message": {"text": text}
    }

    headers = {
        "access_token": token,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(ZALO_API_URL, json=payload, headers=headers)
            data = resp.json()
            if data.get("error") != 0:
                print(f"[zalo] Lỗi gửi tin: {data}")
    except Exception as e:
        print(f"[zalo] Exception: {e}")
