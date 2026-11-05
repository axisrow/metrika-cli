# metrika-cli

CLI для API Яндекс Метрики. Структура зеркалит API 1:1: одна группа команд = одна ресурсная группа API.

22 группы (105 эндпоинтов): management (13 групп), stat (6 операций), logs (7 операций), Data Import (4 группы), export (/export/v1) и cdp (/cdp/api/v1).

| Группа | API | Префикс | Операции |
|---|---|---|---|
| `metrika counters` | Management API | `/management/v1` | `list`, `get`, `create`, `edit`, `delete` |
| `metrika goals` | Management API | `/management/v1` | `list`, `get`, `create`, `edit`, `delete` |
| `metrika filters` | Management API | `/management/v1` | `list`, `get`, `create`, `edit`, `delete` |
| `metrika operations` | Management API | `/management/v1` | `list`, `get`, `create`, `edit`, `delete` |
| `metrika grants` | Management API | `/management/v1` | `list`, `create`, `delete`, `public-set`, `public-delete` |
| `metrika delegates` | Management API | `/management/v1` | `list`, `create`, `delete` |
| `metrika accounts` | Management API | `/management/v1` | `list`, `update`, `delete` |
| `metrika segments` | Management API | `/management/v1` | `list`, `get`, `create`, `edit`, `delete` |
| `metrika labels` | Management API | `/management/v1` | `list`, `get`, `create`, `edit`, `delete`, `link`, `unlink` |
| `metrika annotations` | Management API | `/management/v1` | `list`, `get`, `create`, `edit`, `delete` |
| `metrika access_filters` | Management API | `/management/v1` | `list`, `get`, `create`, `edit`, `delete` |
| `metrika clients` | Management API | `/management/v1` | `list` |
| `metrika measurement` | Management API | `/management/v1` | `generate`, `delete` |
| `metrika stat` | Reports API | `/stat/v1` | `table`, `bytime`, `comparison`, `drilldown`, `comparison-drilldown`, `pivot` |
| `metrika logs` | Logs API | `/management/v1/counter/{id}/logrequest…` | `evaluate`, `list`, `create`, `info`, `cancel`, `clean`, `download-part` |
| `metrika conversions` | Data Import | `/management/v1` | `upload`, `uploadings`, `uploading` |
| `metrika calls` | Data Import | `/management/v1` | `upload`, `uploadings`, `uploading` |
| `metrika expenses` | Data Import | `/management/v1` | `upload`, `delete`, `delete-single`, `uploadings`, `uploading` |
| `metrika user_params` | Data Import | `/management/v1` | `upload`, `uploadings`, `uploading`, `confirm` |
| `metrika export` | Yandex Cloud export | `/export/v1` | `list`, `delete` |
| `metrika cdp` | CDP/CRM | `/cdp/api/v1` | `upload-contacts`, `upload-contacts-json`, `upload-orders`, `upload-orders-json`, `upload-simple-orders`, `last-uploadings`, `attributes`, `create-attributes`, `order-statuses`, `map-order-statuses`, `predefined-types`, `types`, `create-products` |
| `metrika yclid` | Data Import | `/management/v1` | пустая группа: API yclid_conversions удалён Яндексом (17.06.2020) — YCLID-конверсии передаются через `metrika conversions` (`client_id_type=YCLID`) |

## Установка

```bash
pip install -e .
metrika --help
metrika --version   # metrika-cli 0.0.1
```

## Токен

OAuth-токен Яндекса (scopes: `metrika:read`, `metrika:write`; для выгрузок —
`metrika:offline_data`, `metrika:expenses`, `metrika:user_params`). Источники по приоритету:

1. `--token`;
2. переменная окружения `METRIKA_TOKEN`;
3. файл `~/.config/metrika-cli/token` (одна строка).

## Примеры

```bash
# Счётчики
metrika counters list
metrika counters get 44147844

# Отчёт-таблица (JSON)
metrika stat table --ids 44147844 \
  --metrics ym:s:visits,ym:s:users \
  --dimensions ym:s:operatingSystem \
  --date1 2026-10-01 --date2 2026-10-31 --limit 100

# То же в CSV + сравнение периодов + пресет
metrika stat table --ids 44147844 --metrics ym:s:visits --preset sources_summary --csv
metrika stat comparison --ids 44147844 --metrics ym:s:visits \
  --date1-a 2026-09-01 --date2-a 2026-09-30 --date1-b 2026-10-01 --date2-b 2026-10-31

# Сырые данные: evaluate → create → info (poll) → download-part → clean
metrika logs evaluate 44147844 --date1 2026-10-01 --date2 2026-10-31 \
  --source visits --fields ym:pv:dateTime,ym:pv:URL
metrika logs create 44147844 --data '{"source":"visits","date1":"2026-10-01","date2":"2026-10-31","fields":["ym:pv:dateTime","ym:pv:URL"]}'
metrika logs info 44147844 12345
metrika logs download-part 44147844 12345 --part 0 --out part0.csv
metrika logs clean 44147844 12345
```

Глобальные опции: `--token`, `--base-url`, `--output json|table`, `--pretty`, `--version`.

## Лимиты (проверено 2026-11-04)

- квоты: 30 req/s на IP (все API), 10 req/s (Logs), 3 параллельных и 5000/сутки на пользователя, отчёты 200/5 мин; при превышении HTTP 429 (клиент ретраит 1 раз по `Retry-After`);
- Reports API: ≤20 метрик и ≤10 группировок на запрос, `limit` ≤100000 (по умолчанию 100), `offset` с 1; префиксы `ym:s:`/`ym:pv:` нельзя смешивать в одном запросе; фильтровать по ID значений, не по локализованным именам;
- Logs API: период запроса ≤1 год, `fields` ≤3000 символов, 10 ГБ данных на счётчик (освобождать через `logs clean`).

Подробности и источники — [docs/api-notes.md](docs/api-notes.md).

## Структура

```
metrika_cli/
├── cli.py          # корневое Typer-приложение
├── config.py       # токен/хост
├── client.py       # httpx: OAuth-заголовок, ретрай 429, разбор ошибок
├── registry/       # единый источник правды: файл = эндпоинт
├── api/            # ресурсные классы ( методы = op из registry)
├── commands/       # Typer-подприложения по группам
└── render/output/inputs/context
```

## Разработка

```bash
pip install -e ".[dev]"
pytest            # юнит + интеграция (respx), без сети
ruff check .
```

## Roadmap

Реализовано:

- Management API: `counters`, `goals`, `filters`, `operations`, `grants`, `delegates`, `accounts`, `segments`, `labels`, `annotations`, `access_filters`, `clients`, `measurement`;
- Reports API (`stat`): `table`, `bytime`, `comparison`, `comparison-drilldown`, `drilldown`, `pivot` — 6 операций; `stat evaluate` и каталог метрик/группировок как эндпоинты не существуют (вердикт в [docs/api-notes.md](docs/api-notes.md));
- Logs API (`logs`): `evaluate`, `list`, `create`, `info`, `cancel`, `clean`, `download-part` — 7 операций;
- Data Import: `conversions`, `calls`, `expenses`, `user_params`; `yclid` — API удалён Яндексом (17.06.2020), YCLID-конверсии идут через `metrika conversions` (`client_id_type=YCLID`), группа показывает вердикт-справку;
- Экспорт в Yandex Cloud (`export`, `/export/v1`): `list`, `delete`;
- CDP/CRM (`cdp`, `/cdp/api/v1`): загрузки клиентов/заказов (CSV и JSON), simple_orders, last-uploadings, schema (атрибуты, статусы заказов, типы, товары).

Отложено владельцем:

- `metrika auth login` (OAuth device-flow) — issue #12;
- живая проверка обработки `Retry-After` — до появления тестового токена (ретрай в `client.py` покрыт юнит-тестами).

Не заведены (есть в API, вне эпика): chats — единственная недостающая операция `findAll_chats` имеет противоречивую страницу openapi (обсуждение в issue #42); загрузка/статус чатов покрываются `metrika conversions --type CHATS`.
