# Отчёт об обучении Python (для .NET разработчика)

> Начало: 2026-03-06
> Профиль: ASP.NET Core / EF Core / CQRS разработчик
> Цель: освоить Python-идиомы за 7 дней

---

## Статус прохождения

| Шаг | Тема | Статус | Коммит |
|-----|------|--------|--------|
| 0 | Инициализация проекта | ✅ Выполнен | Step 0 |
| 1 | Python синтаксис | ✅ Выполнен | Step 1 |
| 2 | ООП и типизация | ✅ Выполнен | Step 2 |
| 3 | Экосистема и инструменты | ✅ Выполнен | Step 3 |
| 4 | Async/await | ⏳ Ожидает | — |
| 5 | FastAPI | ⏳ Ожидает | — |
| 6 | SQLAlchemy + Alembic | ⏳ Ожидает | — |
| 7 | Тестирование + финальный проект | ⏳ Ожидает | — |

---

## Шаг 0 — Инициализация проекта

**Дата:** 2026-03-06

### Что создано

- `pyproject.toml` — зависимости: fastapi, sqlalchemy, alembic, pydantic, pytest, ruff, mypy
- `src/orders/` — пакет с Clean Architecture layout
- `tests/` — unit/ и integration/ с conftest.py
- `exercises/day1..day4/` — папки для упражнений
- `.env.example` — шаблон конфигурации
- `README.md` — описание проекта

### Ключевые аналогии .NET → Python

| .NET | Python | Назначение |
|------|--------|------------|
| NuGet / .csproj | pyproject.toml + uv | Управление зависимостями |
| `dotnet format` / StyleCop | ruff | Форматирование и линтинг |
| Roslyn analyzers | mypy | Статическая типизация |
| xUnit | pytest | Тестирование |
| `dotnet ef migrations add` | `alembic revision --autogenerate` | Миграции БД |

---

## Шаг 1 — Python синтаксис

**Дата:** 2026-03-06

### Файлы упражнений

- `exercises/day1/task_1_collections.py` — list/dict/set comprehensions, Counter
- `exercises/day1/task_2_strings.py` — f-strings, форматирование, выравнивание
- `exercises/day1/task_3_pattern_matching.py` — match/case, guard conditions
- `exercises/day1/task_4_args_kwargs.py` — *args, **kwargs, keyword-only

### Ключевые аналогии C# → Python

| C# | Python | Пример |
|----|--------|--------|
| `LINQ .Where().Select().ToList()` | list comprehension | `[x*x for x in nums if x>0]` |
| `ToDictionary(k, v)` | dict comprehension | `{w: len(w) for w in words}` |
| `new HashSet<T>(items)` | set comprehension | `{x%3 for x in nums}` |
| `GroupBy().Count()` | `Counter(items)` | `Counter("mississippi")` |
| `dict.GetValueOrDefault(k, d)` | `dict.get(k, d)` | `cfg.get("timeout", 30)` |
| `$"{amount:N2}"` | `f"{amount:,.2f}"` | `f"{1234.5:,.2f}"` → `"1,234.50"` |
| `switch expression` | `match/case` | `match code: case 200: ...` |
| `when` guard | `case x if cond:` | `case n if n < 0:` |
| `params T[]` | `*args` | `def sum_all(*numbers)` |
| named args | `**kwargs` | `def create(**overrides)` |

---

## Шаг 2 — ООП и типизация

**Дата:** 2026-03-06

### Файлы

- `src/orders/domain/models.py` — Money, OrderItem, Order, OrderStatus
- `exercises/day2/task_protocol.py` — Protocol, duck typing vs ABC

### Protocol vs ABC

| Критерий | Protocol (duck typing) | ABC (явное) |
|----------|------------------------|-------------|
| C# аналог | interface (implicit) | interface |
| Наследование | НЕ нужно | Обязательно |
| `isinstance()` | Да (`@runtime_checkable`) | Да |
| Общая логика | Нет | Да |
| Чужие классы | ✅ Работает | ❌ Не работает |

### Ключевые аналогии

| C# | Python |
|----|--------|
| `record` / `record struct` | `@dataclass` / `@dataclass(frozen=True)` |
| конструктор с валидацией | `__post_init__` |
| `operator +` | `__add__` |
| `get-only property` | `@property` |
| `LINQ .Aggregate()` | `functools.reduce()` |
| `interface IRepo` | `Protocol` |
| `: IRepo` (реализация) | duck typing — не нужно! |

---

## Шаг 3 — Экосистема и инструменты

**Дата:** 2026-03-06

### Файлы

- `src/orders/config.py` — pydantic-settings с `.env`, синглтон через `lru_cache`
- `exercises/day3/tooling_guide.md` — полная таблица аналогов команд

### Аналоги команд

| .NET | Python | Назначение |
|------|--------|------------|
| `dotnet add package` | `uv add` | Пакетный менеджер |
| `dotnet format` | `ruff format .` | Форматирование |
| Roslyn analyzers | `mypy src/` | Статическая типизация |
| `dotnet test` | `pytest` | Тестирование |
| `dotnet ef migrations add` | `alembic revision --autogenerate` | Миграции |
| `appsettings.json` + `IOptions<T>` | `pydantic-settings BaseSettings` | Конфигурация |

---

## Шаг 4 — Async/await

*(Заполняется агентом python-step-4-async)*

---

## Шаг 5 — FastAPI

*(Заполняется агентом python-step-5-fastapi)*

---

## Шаг 6 — SQLAlchemy + Alembic

*(Заполняется агентом python-step-6-sqlalchemy)*

---

## Шаг 7 — Тестирование

*(Заполняется агентом python-step-7-testing)*

---

## Итоговые паттерны

*(Заполняется по мере прохождения)*
