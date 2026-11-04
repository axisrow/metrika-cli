# Контракты API Яндекс Метрики (по результатам deep-research от 2026-11-04)

Исследование: 20 первичных источников, 100 клеймов, 25 прошли adversarial-верификацию
(23 подтверждены, 2 опровергнуты). Живая проверка ключевых URL — 2026-11-04, ревизия доков r21770580.

## 4 документированных API на одном хосте

Хост: `https://api-metrika.yandex.net` (написание `api-metrica.yandex.net` тоже рабочее,
проверено HTTP 200). Общий шаблон REST: `https://api-metrika.yandex.net/<раздел>/<версия>/<метод>[.<формат>]`.

| API | Префикс путей | Что делает |
|---|---|---|
| **Management API** | `/management/v1/…` | CRUD: счётчики, цели, фильтры, операции, grants, delegates |
| **Reports (stat)** | `/stat/v1/…` | Агрегированные отчёты: `data`, `data/bytime`, `data/comparison`, `data/drilldown`, `data/pivot`, пресеты |
| **Logs API** | `/management/v1/counter/{counterId}/logrequest…` | Неагрегированные сырые данные (хиты/визиты), асинхронный workflow |
| **Data Import** | `/management/v1/…` (физически management-хост) | Расходы, CRM, звонки (`uploadCalls`), офлайн-конверсии, user params, Measurement Protocol |

## Auth

- OAuth-токен Яндекса в **каждом** запросе: `Authorization: OAuth <token>`; без него — 401.
- Scopes: `metrika:read`, `metrika:write`, `metrika:expenses`, `metrika:user_params`, `metrika:offline_data`.
- Открытый вопрос (v0.0.1 не блокирует): flow регистрации приложения и refresh токена.

## Квоты и ошибки (общие для всех API)

- 30 req/s на IP (все API); 10 req/s (Logs API); 3 параллельных + 5000 запросов/сутки на пользователя; отчёты — 200/5 мин.
- При превышении — HTTP 429 (тип квоты в теле ответа). Клиент ретраит 1 раз с паузой `Retry-After`/60с.
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

1. «Management API даёт полный CRUD по segments, labels, chart annotations, clients, Yandex Cloud exports» — голос 1-2, не подтверждено.
2. «Только три stat-эндпоинта (data/bytime/comparison)» — упускает drilldown и pivot; всего их пять.
3. Префиксы `ym:u:`/`ym:ep:` — встречались только у сторонних источников; официально подтверждена лишь пара `ym:s:`/`ym:pv:`. Не хардкодить префикс в CLI.

## Открытые вопросы (для следующих версий)

- Полный OAuth-flow для CLI и минимальный scope для read-only отчётов.
- Есть ли `Retry-After` при 429 и отдельные квоты по разделам.
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
