"""
Formatter — chuẩn hóa định dạng tin nhắn trả về
"""

CBI_PHONE = "0xxx-xxx-xxx"   # Thay bằng số điện thoại thật của CBI


def fmt_price(gia) -> str:
    if not gia:
        return "Liên hệ"
    return f"{int(gia):,}".replace(",", ".") + " đ"


def format_single(p: dict) -> str:
    return (
        f"✅ {p['ten_hang']}\n"
        f"   Mã: {p['ma_hd']}  |  ĐVT: {p.get('don_vi') or '—'}\n"
        f"   💰 Giá: {fmt_price(p.get('gia_ban'))}"
    )


def format_list(products: list, not_found: list = None) -> str:
    lines = ["📋 Bảng giá:\n"]
    for i, p in enumerate(products, 1):
        lines.append(
            f"{i}. {p['ten_hang']}\n"
            f"   {fmt_price(p.get('gia_ban'))} / {p.get('don_vi') or '—'}"
        )
    if not_found:
        lines.append(f"\n⚠️ Không tìm thấy: {', '.join(not_found)}")
    lines.append("\n_Giá chưa bao gồm VAT. Liên hệ CBI để xác nhận._")
    return "\n".join(lines)


def format_not_found(query: str) -> str:
    return (
        f"❓ Không tìm thấy: \"{query}\"\n\n"
        f"Vui lòng liên hệ nhân viên CBI:\n"
        f"📞 {CBI_PHONE}\n\n"
        f"Gõ /danh muc để xem nhóm sản phẩm."
    )


def format_help() -> str:
    return (
        "🤖 Bot Báo giá C&B Tràng An\n\n"
        "Cách dùng:\n"
        "• Nhắn tên sản phẩm để tra giá\n"
        "  Ví dụ: van bi inox dn25\n"
        "• Nhiều sản phẩm: mỗi dòng 1 cái\n\n"
        "Lệnh:\n"
        "  /danh muc — xem nhóm sản phẩm\n"
        "  /lien he  — thông tin liên hệ\n"
        "  /help     — hướng dẫn này"
    )


def format_catalog() -> str:
    return (
        "📦 Nhóm sản phẩm CBI:\n\n"
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
        "📞 Liên hệ C&B Tràng An:\n\n"
        f"Điện thoại: {CBI_PHONE}\n"
        "Địa chỉ: [Địa chỉ CBI]\n"
        "Giờ làm việc: 8:00 – 17:30 (Thứ 2 – Thứ 7)"
    )
