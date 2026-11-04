"""Эндпоинты группы user_params (параметры посетителей, Data Import).

Источник правды: openapi Management API (страницы
https://yandex.ru/dev/metrika/ru/management/openapi/user_params/ — upload,
findAll, findById, confirm; проверено 2026-11-05). У ресурса ровно 4
операции; DELETE/PUT из вендорного маппинга tapi (2022) в текущем openapi
не задокументированы — не реализованы. Scope токена: ``metrika:user_params``.
"""
