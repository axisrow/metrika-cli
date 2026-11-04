# metrika-cli

CLI для API Яндекс Метрики. Структура зеркалит API 1:1: одна группа команд = одна ресурсная группа API.

18 групп (44 эндпоинта; для групп с пометкой «каркас» команды приходят в фичевых PR — issues 2–19 эпика):

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
| `metrika labels` | Management API | `/management/v1` | каркас: метки и привязка к счётчикам |
| `metrika annotations` | Management API | `/management/v1` | каркас: графические аннотации счётчика |
| `metrika access_filters` | Management API | `/management/v1` | `list`, `get`, `create`, `edit`, `delete` |
| `metrika stat` | Reports API | `/stat/v1` | `table`, `bytime`, `comparison`, `drilldown`, `pivot` |
| `metrika logs` | Logs API | `/management/v1/counter/{id}/logrequest…` | `evaluate`, `list`, `create`, `info`, `cancel`, `clean`, `download-part` |
| `metrika conversions` | Data Import | `/management/v1` | каркас: офлайн-конверсии (upload + uploadings) |
| `metrika calls` | Data Import | `/management/v1` | `upload`, `uploadings`, `uploading` |
| `metrika expenses` | Data Import | `/management/v1` | каркас: загрузка расходов |
| `metrika user_params` | Data Import | `/management/v1` | каркас: параметры посетителей |
| `metrika yclid` | Data Import | `/management/v1` | каркас: YCLID-конверсии (upload + uploadings) |

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

- Management: цели, фильтры, операции, grants, delegates, accounts;
- Management (следующий слой): segments, labels, chart annotations, access filters, chats, clients, cloud exports;
- Data Import: офлайн-конверсии, звонки, расходы, user params (upload на management-хосте);
- `stat evaluate`, каталог метрик/группировок;
- `metrika auth login` (OAuth device-flow).
