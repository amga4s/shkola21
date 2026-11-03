from src.domain import calculate_total, purchase_error

# --- расчёт ---

def test_two_bottles_cost_300():
    assert calculate_total(150, 2) == 300

def test_total_of_one_hoodie():
    assert calculate_total(500, 1) == 500

# --- правило покупки ---

def _bottle():
    return {
        "id": "bottle",
        "price_coins": 150,
        "user_limit": 2,
        "stock": {"one_size": 12},
    }

def test_purchase_ok_returns_none():
    assert purchase_error(
        _bottle(), "one_size", 1, balance=850, already_owned=0, total=150
    ) is None

def test_out_of_stock():
    product = {"id": "hoodie", "price_coins": 500, "user_limit": 1, "stock": {"M": 0}}
    assert purchase_error(product, "M", 1, 999, 0, 500) == "OUT_OF_STOCK"

def test_unknown_size_is_out_of_stock():
    # размера нет в stock → available=0 → OUT_OF_STOCK
    assert purchase_error(_bottle(), "XL", 1, 999, 0, 150) == "OUT_OF_STOCK"

def test_user_limit_exceeded():
    # лимит 2, уже 2 взято, берёт ещё 1
    assert purchase_error(_bottle(), "one_size", 1, 999, 2, 150) == "USER_LIMIT_EXCEEDED"

def test_insufficient_coins():
    assert purchase_error(_bottle(), "one_size", 1, 20, 0, 150) == "INSUFFICIENT_COINS"

def test_order_of_checks_stock_before_limit_before_coins():
    # остаток 0, лимит превышен, коинов нет → должен вернуться самый ранний: OUT_OF_STOCK
    product = {"id": "x", "price_coins": 100, "user_limit": 1, "stock": {"S": 0}}
    assert purchase_error(product, "S", 1, 0, 5, 100) == "OUT_OF_STOCK"