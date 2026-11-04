"""Эндпоинты группы calls (офлайн-звонки, Data Import).

Источник правды: openapi-справочник Management API (openapi/call/,
проверено 2026-11-05) — у ресурса call ровно 3 операции: uploadCalls
(upload), findAllCallUploadings (uploadings), findCallUploadingById
(uploading). Пути совпадают с вендорным маппингом tapi-yandex-metrika
(``_resource_mapping.py``).
"""
