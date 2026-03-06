# Справочник инструментов: .NET → Python

> Быстрый справочник для .NET разработчика по инструментам экосистемы Python.

---

## Управление пакетами

| .NET (NuGet) | Python (uv) | Описание |
|--------------|-------------|----------|
| `dotnet add package Foo` | `uv add foo` | Добавить зависимость |
| `dotnet add package Foo --version 1.2` | `uv add "foo==1.2"` | Добавить с версией |
| `dotnet remove package Foo` | `uv remove foo` | Удалить зависимость |
| `dotnet restore` | `uv sync` | Восстановить зависимости |
| `dotnet tool install -g roslynator` | `uv tool install ruff` | Глобальный инструмент |
| `packages.lock.json` | `uv.lock` | Lock файл |
| `.csproj` | `pyproject.toml` | Файл проекта |

---

## Форматирование и линтинг

| .NET | Python (ruff) | Описание |
|------|---------------|----------|
| `dotnet format` | `ruff format .` | Форматировать код |
| `dotnet format --verify-no-changes` | `ruff format --check .` | Проверить форматирование |
| StyleCop / Roslyn analyzers | `ruff check .` | Линтинг |
| `dotnet format --fix` | `ruff check --fix .` | Автоисправление |
| EditorConfig | `pyproject.toml [tool.ruff]` | Настройки |

```bash
# Форматировать весь проект
uv run ruff format .

# Линтинг с автоисправлением
uv run ruff check --fix .

# Проверить без изменений (для CI)
uv run ruff format --check . && uv run ruff check .
```

---

## Статическая типизация

| .NET (Roslyn) | Python (mypy) | Описание |
|---------------|---------------|----------|
| Встроен в компилятор | `mypy src/` | Проверка типов |
| `#pragma warning disable` | `# type: ignore` | Отключить предупреждение |
| Nullable reference types | `Optional[T]` / `T \| None` | Nullable типы |
| Generics `List<T>` | `list[T]` | Обобщённые типы |

```bash
# Проверить типы в src/
uv run mypy src/

# Строгий режим (аналог <Nullable>enable</Nullable>)
uv run mypy src/ --strict
```

---

## Тестирование

| .NET (xUnit) | Python (pytest) | Описание |
|--------------|-----------------|----------|
| `dotnet test` | `uv run pytest` | Запустить тесты |
| `dotnet test --filter "ClassName"` | `pytest -k "test_name"` | Фильтр тестов |
| `dotnet test -v` | `pytest -v` | Подробный вывод |
| `[Fact]` | `def test_*():` | Объявление теста |
| `[Theory]` + `[InlineData]` | `@pytest.mark.parametrize` | Параметрические тесты |
| `Assert.Equal(expected, actual)` | `assert actual == expected` | Проверка |
| `Assert.Throws<T>()` | `pytest.raises(T)` | Ожидание исключения |
| Mock / Moq | `unittest.mock.AsyncMock` | Моки |

```bash
# Запустить все тесты
uv run pytest

# Подробный вывод
uv run pytest -v

# Конкретный файл
uv run pytest tests/unit/test_domain.py

# Фильтр по имени
uv run pytest -k "test_money"

# С покрытием
uv run pytest --cov=src/orders --cov-report=term-missing
```

---

## Миграции БД

| .NET (EF Core) | Python (Alembic) | Описание |
|----------------|------------------|----------|
| `dotnet ef migrations add Init` | `alembic revision --autogenerate -m "init"` | Создать миграцию |
| `dotnet ef database update` | `alembic upgrade head` | Применить все миграции |
| `dotnet ef database update 0` | `alembic downgrade base` | Откатить все |
| `dotnet ef migrations remove` | `alembic downgrade -1` | Откатить одну |
| `dotnet ef migrations list` | `alembic history` | История миграций |
| `dotnet ef dbcontext info` | `alembic current` | Текущая версия |

```bash
# Инициализация Alembic (один раз)
uv run alembic init alembic

# Создать миграцию по изменениям моделей
uv run alembic revision --autogenerate -m "add orders table"

# Применить миграции
uv run alembic upgrade head

# Откатить последнюю миграцию
uv run alembic downgrade -1
```

---

## Запуск приложения

| .NET | Python | Описание |
|------|--------|----------|
| `dotnet run` | `uv run uvicorn src.orders.api.main:app` | Запустить |
| `dotnet watch run` | `uv run uvicorn ... --reload` | Hot reload |
| `dotnet publish` | `uv build` | Сборка |
| `ASPNETCORE_ENVIRONMENT=Production` | `APP_ENV=production` | Среда |

```bash
# Development с hot reload
uv run uvicorn src.orders.api.main:app --reload --port 8000

# Production
APP_ENV=production uv run uvicorn src.orders.api.main:app --workers 4
```

---

## Конфигурация

| .NET | Python | Описание |
|------|--------|----------|
| `appsettings.json` | `.env` файл | Конфигурация |
| `appsettings.Development.json` | `.env.development` | Среда-специфичный |
| `IConfiguration["key"]` | `settings.key` | Доступ к настройкам |
| `IOptions<T>` | `pydantic-settings BaseSettings` | Типизированные настройки |
| `UserSecrets` | `.env` (не в git) | Секреты |

---

## Структура проекта

```
python-orders/              ← аналог Solution
├── src/
│   └── orders/             ← аналог Project (Class Library)
│       ├── domain/         ← Domain Layer
│       ├── application/    ← Application Layer
│       ├── infrastructure/ ← Infrastructure Layer
│       └── api/            ← Presentation Layer (FastAPI)
├── tests/                  ← Test Project
│   ├── unit/
│   └── integration/
├── exercises/              ← обучающие материалы
└── pyproject.toml          ← .csproj / .sln
```
