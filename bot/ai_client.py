"""
Claude AI Client — phân tích câu hỏi phức tạp
"""
import os
import json
from anthropic import Anthropic
from db.crud import get_all_products_summary

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

SYSTEM_PROMPT = """Bạn là trợ lý tra cứu sản phẩm của công ty C&B Tràng An,
chuyên về thiết bị đường ống, van, phụ kiện công nghiệp.

Nhiệm vụ: Từ câu hỏi của khách hàng, trích xuất danh sách sản phẩm họ cần hỏi giá.

Quy tắc QUAN TRỌNG:
- Chỉ trả về sản phẩm có trong danh mục CBI được cung cấp
- KHÔNG tự bịa mã sản phẩm
- Nếu không chắc chắn, trả về mảng rỗng []
- Luôn trả về JSON hợp lệ, không kèm giải thích

Format trả về (JSON array):
[{"ten_hang": "Tên chính xác trong danh mục", "ma_hd": "MÃ_SP"}]
"""


async def analyze_with_ai(query: str, session: dict) -> list | None:
    """
    Dùng Claude Haiku để phân tích câu hỏi và trích xuất sản phẩm.
    Chỉ gọi khi fuzzy search thất bại (tiết kiệm chi phí).
    """
    if not os.getenv("ANTHROPIC_API_KEY"):
        return None

    catalog = get_all_products_summary()
    catalog_text = "\n".join(
        f"- {p['ten_hang']} | Mã: {p['ma_hd']}"
        for p in catalog[:300]
    )

    user_prompt = (
        f"Danh mục sản phẩm CBI:\n{catalog_text}\n\n"
        f"Câu hỏi khách: \"{query}\"\n\n"
        f"Trả về JSON danh sách sản phẩm khách đang hỏi."
    )

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}]
        )
        content = response.content[0].text.strip()
        # Lấy phần JSON từ response
        start = content.find("[")
        end = content.rfind("]") + 1
        if start >= 0 and end > start:
            result = json.loads(content[start:end])
            return result if isinstance(result, list) else None
        return None
    except Exception as e:
        print(f"[ai_client] Lỗi: {e}")
        return None
