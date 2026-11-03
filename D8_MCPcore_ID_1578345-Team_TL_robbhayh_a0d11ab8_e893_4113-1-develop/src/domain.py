"""Правила без SQL и MCP. Вся арифметика в целых коинах."""

def calculate_total(price, quantity):
    'Стоимость заказа.'
    total_price = price * quantity
    return total_price

def purchase_error(product, size, quantity, balance, already_owned, total):
    'Код отказа или None. Пользователь и товар уже найдены.'
    stock = product.get("stock", {})
    available = stock.get(size, 0)
    if available < quantity:
        return "OUT_OF_STOCK"
    if already_owned + quantity > product["user_limit"]:
        return "USER_LIMIT_EXCEEDED"
    if total > balance:
        return "INSUFFICIENT_COINS"
    return None

def refund_amount(total_price):
    'Сумма возврата по сохранённой стоимости заказа.'
    return (total_price)

def can_cancel(order):
    'Можно ли отменить найденный заказ.'
    print("Можно отменить", order)
    return order["status"] == "created"

def can_pickup(order):
    'Можно ли выдать найденный заказ.'
    print("Можно выдать", order)
    return order["status"] == "created"

