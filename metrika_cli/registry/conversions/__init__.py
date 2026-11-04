"""Эндпоинты группы conversions (офлайн-конверсии, Data Import).

Источник правды: openapi-справочник Management API (ревизия r21770580,
проверена 2026-11-04) — у ресурса offline_conversions ровно 3 операции:
upload, findAll (uploadings), findById (uploading). Confirm/delete из
раннего ТЗ в текущем openapi отсутствуют (confirm есть только у
user_params) — поэтому их здесь нет.
"""
