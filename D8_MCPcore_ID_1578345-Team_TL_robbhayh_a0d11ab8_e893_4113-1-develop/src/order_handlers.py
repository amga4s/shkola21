"""Порядок работы с заказом. Правила в domain, SQL в storage."""
from . import domain
from .errors import success, failure

def create_order(storage, user_id, product_id, size, quantity):
    'Реализуйте по правилам Лавки и согласованным методам.'
    # 1. Пользователь
    user = storage.get_user(user_id)
    if user is None:
        return failure("USER_NOT_FOUND", "Пользователь не найден")

    # 2. Товар
    product = storage.get_product(product_id)
    if product is None:
        return failure("PRODUCT_NOT_FOUND", "Товар не найден")

    # 3 - 5. Правила: остаток → лимит → коины
    total = domain.calculate_total(product["price_coins"], quantity)
    already_owned = storage.count_owned(user_id, product_id)
    code = domain.purchase_error(
        product, size, quantity, user["coins"], already_owned, total
    )
    if code is not None:
        return failure(code, "Покупка отклонена")

    # Запись одной транзакцией внутри storage.create_order
    order = storage.create_order(user_id, product_id, size, quantity, total)
    return success(order)

def cancel_order(storage, order_id):
    order = storage.get_order(order_id)
    if order is None:
        return failure("ORDER_NOT_FOUND", "Заказ не найден")
    if not domain.can_cancel(order):
        return failure("ORDER_STATUS_ERROR", "Нельзя отменить заказ в этом статусе")
    refund = domain.refund_amount(order["total_price"])
    result = storage.cancel_order(order, refund)
    return success(result)

def confirm_pickup(storage, order_id):
    'Реализуйте по правилам Лавки и согласованным методам.'
    order = storage.get_order(order_id)
    if order is None:
        return failure("ORDER_NOT_FOUND", "Заказ не найден")
    if not domain.can_pickup(order):
        return failure("ORDER_STATUS_ERROR", "Нельзя выдать заказ в этом статусе")
    result = storage.confirm_pickup(order_id)
    return success(result)