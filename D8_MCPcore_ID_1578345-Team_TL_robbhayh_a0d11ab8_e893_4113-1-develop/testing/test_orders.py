from src import order_handlers


class FakeStorage:
    """Минимальная заглушка: только то, что нужно create_order."""
    def __init__(self):
        self.products = {
            "bottle": {
                "id": "bottle",
                "price_coins": 150,
                "user_limit": 2,
                "stock": {"one_size": 12},
            },
        }
        self.users = {"student_01": {"id": "student_01", "coins": 1000}}
        self.owned = {}           # (user_id, product_id) -> int
        self.written = None       # сюда попадёт вызов create_order

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_product(self, product_id):
        return self.products.get(product_id)

    def count_owned(self, user_id, product_id):
        return self.owned.get((user_id, product_id), 0)

    def create_order(self, user_id, product_id, size, quantity, total):
        self.written = {
            "user_id": user_id, "product_id": product_id,
            "size": size, "quantity": quantity, "total": total,
        }
        return {"order_id": "fake-1", "status": "created", "total_price": total}


def test_create_order_user_not_found():
    storage = FakeStorage()
    result = order_handlers.create_order(storage, "ghost", "bottle", "one_size", 1)
    assert result["ok"] is False
    assert result["error"]["code"] == "USER_NOT_FOUND"
    assert storage.written is None          # ← данных не тронули


def test_create_order_product_not_found():
    storage = FakeStorage()
    result = order_handlers.create_order(storage, "student_01", "ghost", "one_size", 1)
    assert result["error"]["code"] == "PRODUCT_NOT_FOUND"
    assert storage.written is None


def test_create_order_out_of_stock():
    storage = FakeStorage()
    storage.products["bottle"]["stock"]["one_size"] = 0
    result = order_handlers.create_order(storage, "student_01", "bottle", "one_size", 1)
    assert result["error"]["code"] == "OUT_OF_STOCK"
    assert storage.written is None


def test_create_order_insufficient_coins():
    storage = FakeStorage()
    storage.users["student_01"]["coins"] = 20
    result = order_handlers.create_order(storage, "student_01", "bottle", "one_size", 1)
    assert result["error"]["code"] == "INSUFFICIENT_COINS"
    assert storage.written is None


def test_create_order_success_writes_once():
    storage = FakeStorage()
    result = order_handlers.create_order(storage, "student_01", "bottle", "one_size", 1)
    assert result["ok"] is True
    assert storage.written == {
        "user_id": "student_01", "product_id": "bottle",
        "size": "one_size", "quantity": 1, "total": 150,
    }