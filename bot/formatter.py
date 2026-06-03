"""
Formatter — định dạng tin nhắn Telegram (hỗ trợ HTML)
"""

CBI_PHONE = "0xxx-xxx-xxx"   # ← Thay số điện thoại thật của CBI vào đây


def fmt_price(gia) -> str:
    if not gia:
        return "Liên hệ"
    return f"{int(gia):,}".replace(",", ".") + " đ"


def format_start() -> str:
    return (
        "👋 Xin chào! Tôi là <b>Bot Báo giá C&amp;B Tràng An</b>\n\n"
        "Nhắn tên sản phẩm để tra giá:\n"
        "<i>Ví dụ: van bi inox dn25</i>\n\n"
        "Hoặc dùng /help để xem hướng dẫn."
    )


def format_single(p: dict) -> str:
    return (
        f"✅ <b>{p['ten_hang']}</b>\n"
        f"   Mã: <code>{p['ma_hd']}</code>  |  ĐVT: {p.get('don_vi') or '—'}\n"
        f"   💰 Giá: <b>{fmt_price(p.get('gia_ban'))}</b>"
    )


def format_list(products: list, not_found: list = None) -> str:
    lines = ["📋 <b>Bảng giá:</b>\n"]
    for i, p in enumerate(products, 1):
        lines.append(
            f"{i}. <b>{p['ten_hang']}</b>\n"
            f"   {fmt_price(p.get('gia_ban'))} / {p.get('don_vi') or '—'}"
        )
    if not_found:
        lines.append(f"\n⚠️ Không tìm thấy: {', '.join(not_found)}")
    lines.append("\n<i>Giá chưa bao gồm VAT. Liên hệ CBI để xác nhận.</i>")
    return "\n".join(lines)


def format_not_found(query: str) -> str:
    return (
        f"❓ Không tìm thấy: <b>{query}</b>\n\n"
        f"Vui lòng liên hệ nhân viên CBI:\n"
        f"📞 {CBI_PHONE}\n\n"
        "Gõ /danhmuc để xem nhóm sản phẩm."
    )


def format_help() -> str:
    return (
        "🤖 <b>Bot Báo giá C&amp;B Tràng An</b>\n\n"
        "<b>Cách dùng:</b>\n"
        "• Nhắn tên sản phẩm để tra giá\n"
        "  <i>Ví dụ: van bi inox dn25</i>\n"
        "• Nhiều sản phẩm: mỗi dòng 1 cái\n\n"
        "<b>Lệnh:</b>\n"
        "/gia [tên] — tra giá trực tiếp\n"
        "/danhmuc   — xem nhóm sản phẩm\n"
        "/lienhe    — thông tin liên hệ\n"
        "/help      — hướng dẫn này"
    )


def format_catalog() -> str:
    return (
        "📦 <b>Nhóm sản phẩm CBI:</b>\n\n"
        "• Van bi inox / Van bi đồng\n"
        "• Kép ren / Kép inox\n"
        "• Racco inox\n"
        "• Mặt bích thép\n"
        "• Tê thép / Cút thép\n"
        "• Gioăng CS\n"
        "• Khớp nối / Van 1 chiều\n"
        "• Đầu bịt / Đầu ren inox\n\n"
        "Nhắn tên sản phẩm để tra giá!"
    )


def format_contact() -> str:
    return (
        "📞 <b>Liên hệ C&amp;B Tràng An:</b>\n\n"
        f"Điện thoại: {CBI_PHONE}\n"
        "Địa chỉ: [Địa chỉ CBI]\n"
        "Giờ làm việc: 8:00–17:30 (Thứ 2 – Thứ 7)"
    )
