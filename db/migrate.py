"""
Migration — Import CSDL_HangHoa_PA3.xlsx vào SQLite
"""
import os
import openpyxl
from db.database import get_connection

EXCEL_PATH = os.getenv("EXCEL_PATH", "./data/CSDL_HangHoa_PA3.xlsx")


def run_migration(force: bool = False):
    """
    Đọc sheet A_DanhMuc từ Excel và upsert vào bảng products.
    force=True: xóa toàn bộ và import lại từ đầu.
    """
    if not os.path.exists(EXCEL_PATH):
        print(f"[migrate] Không tìm thấy: {EXCEL_PATH} — bỏ qua.")
        return

    try:
        wb = openpyxl.load_workbook(EXCEL_PATH, read_only=True, data_only=True)
    except Exception as e:
        print(f"[migrate] Lỗi mở Excel: {e}")
        return

    if "A_DanhMuc" not in wb.sheetnames:
        print("[migrate] Không tìm thấy sheet A_DanhMuc")
        wb.close()
        return

    ws = wb["A_DanhMuc"]
    conn = get_connection()

    if force:
        conn.execute("DELETE FROM products")
        conn.commit()
        print("[migrate] Đã xóa dữ liệu cũ.")

    inserted = updated = skipped = 0

    # Cột: A=STT, B=MãHĐ, C=TênHàng, D=ĐVT, E=GiáBán, F=Nhóm
    for row in ws.iter_rows(min_row=4, values_only=True):
        if len(row) < 3:
            continue
        stt     = row[0]
        ma_hd   = row[1]
        ten     = row[2]
        dvt     = row[3] if len(row) > 3 else None
        gia     = row[4] if len(row) > 4 else None
        nhom    = row[5] if len(row) > 5 else None

        if not ma_hd or not ten:
            continue
        ma_hd = str(ma_hd).strip()
        if ma_hd.startswith("???") or ma_hd == "":
            skipped += 1
            continue

        try:
            gia_val = float(gia) if gia is not None else None
            conn.execute("""
                INSERT INTO products (ma_hd, ten_hang, don_vi, gia_ban, nhom)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(ma_hd) DO UPDATE SET
                    ten_hang = excluded.ten_hang,
                    don_vi   = excluded.don_vi,
                    gia_ban  = excluded.gia_ban,
                    nhom     = excluded.nhom,
                    updated_at = datetime('now','localtime')
            """, (ma_hd, str(ten).strip(),
                  str(dvt).strip() if dvt else None,
                  gia_val,
                  str(nhom).strip() if nhom else None))
            inserted += 1
        except Exception as e:
            print(f"[migrate] Lỗi dòng {stt}: {e}")

    conn.commit()
    conn.close()
    wb.close()

    # Reload cache
    from bot.search import load_cache
    load_cache()

    print(f"[migrate] Xong: {inserted} sản phẩm, bỏ qua {skipped} (??? hoặc rỗng)")
