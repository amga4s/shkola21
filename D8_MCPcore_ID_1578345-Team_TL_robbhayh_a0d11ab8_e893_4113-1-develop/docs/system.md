# Паспорт Лавки

Профиль правил: base

## Что делает сервер

Перечислите доступные действия и изменяемые данные.

## Границы

Какие пользователи существуют? Есть ли проверка личности? Какие действия клиенту обещать нельзя?

## Путь запроса

client.py → get_product → mcp_adapter.get_product → read_handlers.get_product → Storage.get_product [SELECT products WHERE id=?; SELECT stock WHERE product_id=? ORDER BY size] → success(product) или failure("PRODUCT_NOT_FOUND")

## Проверка отказа

Пример запроса:
Ожидаемый отказ:
Где проверяется:
Как показали неизменность данных:

## Подключение следующего дня

Команда запуска сервера:
Транспорт:
Контракты: contracts/tools_schemas.json
Инструкция: RUN.md
Журнал: logs/client.jsonl
Известные ограничения:

