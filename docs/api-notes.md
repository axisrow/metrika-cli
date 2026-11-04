# Контракты API Яндекс Метрики (по результатам deep-research от 2026-11-04)

Исследование: 20 первичных источников, 100 клеймов, 25 прошли adversarial-верификацию
(23 подтверждены, 2 опровергнуты). Живая проверка ключевых URL — 2026-11-04, ревизия доков r21770580.

## 4 документированных API на одном хосте

Хост: `https://api-metrika.yandex.net` (написание `api-metrica.yandex.net` тоже рабочее,
проверено HTTP 200). Общий шаблон REST: `https://api-metrika.yandex.net/<раздел>/<версия>/<метод>[.<формат>]`.

| API | Префикс путей | Что делает |
|---|---|---|
| **Management API** | `/management/v1/…` | CRUD: счётчики, цели, фильтры, операции, grants, delegates |
| **Reports (stat)** | `/stat/v1/…` | Агрегированные отчёты: `data`, `data/bytime`, `data/comparison`, `data/comparison/drilldown`, `data/drilldown`, `data/pivot`, пресеты |
| **Logs API** | `/management/v1/counter/{counterId}/logrequest…` | Неагрегированные сырые данные (хиты/визиты), асинхронный workflow |
| **Data Import** | `/management/v1/…` (физически management-хост) | Расходы, CRM, звонки (`uploadCalls`), офлайн-конверсии, user params, Measurement Protocol |

## Auth

- OAuth-токен Яндекса в **каждом** запросе: `Authorization: OAuth <token>`; без него — 401.
- Scopes: `metrika:read`, `metrika:write`, `metrika:expenses`, `metrika:user_params`, `metrika:offline_data`.
- Открытый вопрос (v0.0.1 не блокирует): flow регистрации приложения и refresh токена.

## Квоты и ошибки (общие для всех API)

- 30 req/s на IP (все API); 10 req/s (Logs API); 3 параллельных + 5000 запросов/сутки на пользователя; отчёты — 200/5 мин.
- При превышении — HTTP 429: в теле тип превышенной квоты (`quota_requests_by_ip`, `quota_requests_by_uid`, `quota_parallel_requests`, `quota_requests_by_counter_id`, `quota_delegate_requests`, `quota_grants_requests` — по errors.md) в едином конверте ошибок.
- **`Retry-After` при 429 — не подтверждён** (investigation 2026-11-04 по докам: 0 упоминаний в quotas.md и errors.md, машинный индекс llms.txt страницы про ретраи не содержит). Живая проверка отложена до появления тестового токена (по решению владельца). Клиент: 2 повторные попытки, экспоненциальный backoff 30с → 60с; заголовок `Retry-After` учитывается, если API его отдаст. Источники: [quotas.md](https://yandex.ru/dev/metrika/ru/intro/quotas.md), [errors.md](https://yandex.ru/dev/metrika/ru/intro/errors.md).
- Единый конверт ошибок: `{"errors": [{"error_type": …, "message": …, "location": …}], "code": <http-status>, "message": …}`.

## Reports API (/stat/v1) — контракт

- `GET /stat/v1/data` — таблица; `.csv`-расширение пути = CSV-ответ (JSON — по умолчанию, UTF-8).
- Параметры: `ids` (ID счётчиков через запятую; форма `id` тоже принимается и нормализуется), `metrics`, `dimensions` (через запятую), `date1`/`date2`, `filters`, `sort`, `limit`, `offset`, `preset`, `lang`.
- Лимиты: **≤20 метрик**, **≤10 группировок**; `limit` max 100 000 (default 100); `offset` c 1.
- Префиксы `ym:s:` (сессии) и `ym:pv:` (просмотры); смешивать в одном запросе нельзя; `filters` может ссылаться на другой префикс. Выражения: `ym:s:pageViews>5`, `ym:s:trafficSource=='organic' AND ym:s:isRobot=='No'`, IN-списки.
- Группировки с ID-интерпретацией возвращают `{id, name}`; в `filters` и drilldown использовать **id** (напр. `'organic'`), не name.
- `bytime`: + `group=day|week|…`; `comparison`: `date1_a/date2_a` vs `date1_b/date2_b` или `filters_a` vs `filters_b`; `drilldown`: дерево, `parent_id`; `pivot`: + `pivot_dimensions`.
- Формат ответа: `query` (эхо запроса), `data[]` (строки: `dimensions[]` — объекты с `name` (+`id`), `metrics[]` — числа), `totals`, `total_rows`, сэмплинг: `sampled`, `sample_share`, `sample_size`, `data_lag`.
- `lang` управляет языком значений; omit → `en` (подтверждено только для stat, голос 2-1 — в CLI передаётся как есть, дефолт не хардкодится).
- Операции OpenAPI stat (llms.txt, 2026-11-04): `data` («Таблица»), `bytime`, `comparison`, `comparison_drilldown`, `drilldown`, `pivot` — всего 6; все заведены в registry (`comparison_drilldown` — PR #35, путь `/stat/v1/data/comparison/drilldown`). `evaluate` и «каталог метрик/группировок» как эндпоинты в Reports API ОТСУТСТВУЮТ — см. «Опровергнуто» №4.

## Logs API — контракт и workflow

- Эндпоинты (все на management-хосте):
  - `GET /management/v1/counter/{id}/logrequests/evaluate` — оценка (date1, date2, source: hits|visits, fields);
  - `POST …/logrequests` — создать `{source, date1, date2, fields}`;
  - `GET …/logrequests` — список;
  - `GET …/logrequest/{requestId}` — статус: `created|canceled|processed|cleaned_by_user|awaiting_retry` + `parts[]`;
  - `GET …/logrequest/{requestId}/part/{partNumber}/download` — CSV-часть;
  - `POST …/logrequest/{requestId}/cancel` — отменить необработанный;
  - `POST …/logrequest/{requestId}/clean` — освободить квоту обработанного.
- Ограничения: период ≤1 год на запрос; `fields` ≤3000 символов; **10 ГБ** суммарно на счётчик (увеличение — только Метрика Про); квота 10 req/s.
- ClickHouse-интеграция — официальный гайд + выгрузка по URL, не нативный протокол.

## Опровергнуто при верификации (НЕ использовать)

1. ~~«Management API даёт полный CRUD по segments, labels, chart annotations, clients, Yandex Cloud exports»~~ — **ПОПРАВКА от 2026-11-04 (позже исследования):** прямая проверка llms.txt показала, что в Management OpenAPI-справочнике эти ресурсы ЕСТЬ: `segment` (5 ops), `label` (5), `chart_annotation` (5), `access_filter` (5), `chats` (3), `clients` (1), `cloud` (2). Вердикт 1-2 верификаторов был ошибочным. При дизайне CLI опираться на перечень ресурсов из llms.txt.
2. ~~«Только три stat-эндпоинта (data/bytime/comparison)» — упускает drilldown и pivot; всего их пять~~ — **ПОПРАВКА от 2026-11-04 (позже исследования, issue #7):** прямая проверка llms.txt показала, что stat OpenAPI содержит 6 операций: `data`, `bytime`, `comparison`, `comparison_drilldown` («Сравнение — drill down», путь `/stat/v1/data/comparison/drilldown`), `drilldown`, `pivot`. Итого шесть, не пять (см. также «Опровергнуто» №4).
3. Префиксы `ym:u:`/`ym:ep:` — встречались только у сторонних источников; официально подтверждена лишь пара `ym:s:`/`ym:pv:`. Не хардкодить префикс в CLI.
4. «stat evaluate» (оценка объёма запроса до выполнения) и «каталог метрик/группировок как API-эндпоинт» (issue #7) — НЕ существуют в Reports API. Проверено 2026-11-04: полный индекс llms.txt содержит для stat ровно 6 OpenAPI-операций (см. контракт выше); `stat/openapi/evaluate.md` (ru и en) → HTTP 404; вендорный справочник tapi-yandex-metrika знает только `stat/v1/data`. Оценка объёма данных в Метрике есть только в Logs API (`logrequests/evaluate`, реализован). Справочник метрик/группировок — статические страницы доков (`stat/attrandmetr/dim_all.md`, разделы `stat/metrics/*` и `stat/attributes/*`), не API-ресурс: CLI-команда для него потребовала бы скрейпинг HTML доков вместо OAuth-вызова — в registry не заводить.

## Машиночитаемый контракт

Единого downloadable OpenAPI/Swagger-файла (json/yaml) Метрика не публикует (`index.yaml` в корне доков — сборочный манифест Diplodoc, не API-спека). Машиночитаемость обеспечивают:

1. **`https://yandex.ru/dev/metrika/ru/llms.txt`** — полный машинный индекс документации (для LLM-агентов): все секции + по одному .md на каждый эндпоинт и схему.
2. **OpenAPI-справочники в Markdown**: `https://yandex.ru/dev/metrika/ru/<api>/openapi/<ресурс>/<операция>.md` — генерированная страница на каждый эндпоинт (параметры, схемы запроса/ответа, ошибки). Сайт собирается Diplodoc (ревизия r21770580 на 2026-11-04).

Реестр ресурсов из llms.txt (ops на 2026-11-04): counter (8), grant (8), goal (7), segment (5), operation (5), label (5), filter (5), expense (5), chart_annotation (5), access_filter (5), user_params (4), offline_conversions (3), delegates (3), chats (3), call (3), account (3), measurement (2 — Measurement Protocol), cloud (2), clients (1); stat: data, bytime, comparison, comparison_drilldown, drilldown, pivot; logs: 7 операций (createLogRequest, getLogRequests, getLogRequest, evaluate, download, cancel, clean). Итого ~75 эндпоинтов.

**Вендореный справочник путей:** `metrika_cli/_resource_mapping.py` — копия `resource_mapping.py` из [tapi-yandex-metrika](https://github.com/pavelmaksimov/tapi-yandex-metrika) (MIT; библиотека не обновлялась с 2022-04). ~50 эндпоинтов management/logs/stats с путями, HTTP-методами и параметрами. Не зависимость: в рантайме не импортируется, используется как стартовая точка путей при расширении registry; каждый путь сверять с живым openapi-справочником (файлу 4+ года). Из него уже подтверждены пути goals/filters/operations/grants (в т.ч. `DELETE /grant?user_login=`), calls (`offline_conversions/upload_calls`), user_params (`uploadings/upload`), segments (`apisegment/…`), labels (`management/v1/labels`), пагинация `counters` (`per_page`/`offset`). Не покрывает expenses/access_filter — для них источник правды llms.txt.

## Открытые вопросы (для следующих версий)

- Полный OAuth-flow для CLI и минимальный scope для read-only отчётов.
- ~~Есть ли `Retry-After` при 429 и отдельные квоты по разделам~~ — закрыто 2026-11-04 по докам (см. «Квоты и ошибки»); живая проверка отложена до появления тестового токена (по решению владельца).
- Пагинация list-эндпоинтов Management/Logs.
- Контракты upload-эндпоинтов Data Import (CSV-форматы conversions/calls/expenses) — в v0.0.1 отложены.

## Источники (первичные, все проверены 2026-11-04)

- https://yandex.ru/dev/metrika/ru/llms.txt — машинный индекс всей документации (4 секции)
- https://yandex.ru/dev/metrika/ru/{management,logs,stat} — интро разделов
- https://yandex.com/dev/metrika/en/stat/openapi/data — справочник /stat/v1/data (параметры, схема ответа)
- https://yandex.com/dev/metrika/en/stat, /en/stat/localize, /en/stat/get-id — форматы, локализация, ID группировок
- https://yandex.com/dev/metrika/doc/api2/api_v1/examples.html — примеры четырёх stat-методов
- https://yandex.com/dev/metrika/en/logs{,/openapi/createLogRequest,/openapi/evaluate,/openapi/clean,/openapi/getLogRequest} — Logs API
- https://yandex.ru/dev/metrika/ru/intro/{versions,method-call,quotas,authorization,errors}.md — кросс-API контракты
