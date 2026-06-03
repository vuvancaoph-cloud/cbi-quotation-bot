"""
Search Engine — tra cứu sản phẩm với fuzzy matching
"""
import unicodedata
import re
from rapidfuzz import fuzz, process
from db.crud import get_all_products

# Cache trong RAM
_product_cache = {}   # {normalized_name: product_dict}
_code_cache = {}      # {ma_hd_upper: product_dict}
_loaded = False


def normalize(s: str) -> str:
    """Chuẩn hóa: bỏ dấu, lowercase, bỏ khoảng trắng thừa"""
    s = str(s).strip()
    s = s.replace('đ', 'd').replace('Đ', 'D')
    s = s.lower()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'\s+', ' ', s)
    return s


def load_cache():
    """Load toàn bộ sản phẩm từ DB vào RAM"""
    global _product_cache, _code_cache, _loaded
    _product_cache = {}
    _code_cache = {}
    products = get_all_products()
    for p in products:
        norm_name = normalize(p["ten_hang"])
        _product_cache[norm_name] = p
        _code_cache[p["ma_hd"].upper()] = p
        # Load aliases
        import json
        aliases = json.loads(p.get("aliases") or "[]")
        for alias in aliases:
            norm_alias = normalize(alias)
            _product_cache[norm_alias] = p
    _loaded = True
    print(f"[search] Loaded {len(products)} sản phẩm vào cache")


def search_products(query: str, by_code: bool = False) -> list:
    """
    Tìm sản phẩm theo tên (fuzzy) hoặc mã (exact).
    Trả về list rỗng nếu không tìm thấy.
    """
    if not _loaded:
        load_cache()

    if not query or len(query.strip()) < 2:
        return []

    # Tìm theo mã
    if by_code:
        p = _code_cache.get(query.upper())
        return [p] if p else []

    norm_query = normalize(query)

    # Exact match
    if norm_query in _product_cache:
        return [_product_cache[norm_query]]

    # Fuzzy match
    if not _product_cache:
        return []

    candidates = list(_product_cache.keys())

    # token_set_ratio xử lý tốt query ngắn (subset của tên sản phẩm)
    matches = process.extract(
        norm_query,
        candidates,
        scorer=fuzz.token_set_ratio,
        limit=5
    )

    results = []
    seen_ma = set()
    for match_name, score, _ in matches:
        if score >= 78:
            p = _product_cache[match_name]
            if p["ma_hd"] not in seen_ma:
                results.append(p)
                seen_ma.add(p["ma_hd"])

    return results
