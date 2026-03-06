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
| 4 | Async/await | ✅ Выполнен | Step 4 |
| 5 | FastAPI | ✅ Выполнен | Step 5 |
| 6 | SQLAlchemy + Alembic | ✅ Выполнен | Step 6 |
| 7 | Тестирование + финальный проект | ✅ Выполнен | Step 7 |

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

**Дата:** 2026-03-06

### Файлы

- `exercises/day4/task_1_gather.py` — asyncio.gather, Semaphore, замер времени
- `exercises/day4/task_2_context_manager.py` — __aenter__/__aexit__, @asynccontextmanager

### Ключевые отличия от .NET async

| C# | Python | Важное отличие |
|----|--------|----------------|
| `async Task<T> M()` | `async def m() -> T:` | — |
| `await M()` | `await m()` | — |
| `Task.WhenAll(t1,t2)` | `asyncio.gather(t1(),t2())` | В Python передаём корутины |
| `Task.WhenAny(...)` | `asyncio.wait(..., FIRST_COMPLETED)` | — |
| `new SemaphoreSlim(3)` | `asyncio.Semaphore(3)` | — |
| `await semaphore.WaitAsync()` | `async with semaphore:` | Через context manager |
| `IAsyncDisposable` | async context manager | `__aenter__`/`__aexit__` |
| `await using var x = new X()` | `async with X() as x:` | — |
| Задача запускается сразу | **Корутина — объект до `await`!** | ⚠️ Главное отличие |

---

## Шаг 5 — FastAPI

**Дата:** 2026-03-06

### Файлы

- `src/orders/infrastructure/repositories.py` — InMemoryOrderRepository
- `src/orders/application/services.py` — OrderService
- `src/orders/api/routers/orders.py` — APIRouter CRUD endpoints
- `src/orders/api/main.py` — FastAPI app, lifespan, middleware

### Аналогии ASP.NET Core → FastAPI

| ASP.NET Core | FastAPI | Описание |
|--------------|---------|----------|
| `[ApiController]` | `APIRouter` | Контроллер/роутер |
| `[HttpPost]` | `@router.post("/")` | HTTP метод |
| `[FromBody]` | Pydantic модель параметра | Десериализация |
| `IActionResult` | автоматически из return | Ответ |
| `services.AddScoped<T>()` | `Depends(factory)` | DI |
| `app.UseMiddleware<T>()` | `@app.middleware("http")` | Middleware |
| `IHostedService` lifespan | `@asynccontextmanager lifespan` | Lifecycle |
| `ProblemDetails` | `HTTPException` | Ошибки |
| `ModelState.IsValid` (авто) | Pydantic валидация (авто) | Валидация |

---

## Шаг 6 — SQLAlchemy + Alembic

**Дата:** 2026-03-06

### Файлы

- `src/orders/infrastructure/orm_models.py` — OrderModel, OrderItemModel, Base
- `src/orders/infrastructure/database.py` — engine, session factory, get_session
- `exercises/day6/alembic_guide.md` — команды EF Core → Alembic

### Аналогии EF Core → SQLAlchemy

| EF Core | SQLAlchemy 2.0 | Описание |
|---------|----------------|----------|
| `DbContext` | `AsyncSession` | Единица работы |
| `DbContextOptions` | `create_async_engine(url)` | Конфигурация |
| `IDbContextFactory<T>` | `async_sessionmaker` | Фабрика сессий |
| `.Include(o => o.Items)` | `lazy="selectin"` | Загрузка связанных |
| `[Required]` | `nullable=False` | Обязательное поле |
| `[MaxLength(200)]` | `String(200)` | Длина строки |
| `SaveChangesAsync()` | `await session.commit()` | Сохранить изменения |
| `dotnet ef migrations add` | `alembic revision --autogenerate` | Создать миграцию |
| `dotnet ef database update` | `alembic upgrade head` | Применить миграции |

---

## Шаг 7 — Тестирование

**Дата:** 2026-03-06

### Файлы

- `tests/conftest.py` — shared fixtures: test_engine, db_session, client
- `tests/unit/test_domain.py` — TestMoney, TestOrderItem, TestOrder (30+ тестов)
- `tests/unit/test_service.py` — тесты OrderService с AsyncMock
- `tests/integration/test_api.py` — тесты через AsyncClient (health, CRUD, validation)

### Аналогии xUnit → pytest

| xUnit (C#) | pytest (Python) | Описание |
|------------|-----------------|----------|
| `[Fact]` | `def test_name():` | Обычный тест |
| `[Theory] + [InlineData]` | `@pytest.mark.parametrize` | Параметрические тесты |
| `Assert.Equal(exp, act)` | `assert act == exp` | Проверка равенства |
| `Assert.Throws<T>(lambda)` | `pytest.raises(T)` | Ожидание исключения |
| `Assert.IsType<T>(obj)` | `assert isinstance(obj, T)` | Проверка типа |
| `IClassFixture<T>` | `fixture(scope="class")` | Fixture на класс |
| `ICollectionFixture<T>` | `fixture(scope="session")` | Fixture на сессию |
| `Mock<T>` (Moq) | `AsyncMock()` | Мок асинхронного объекта |
| `mock.Setup(...).Returns(x)` | `mock.method.return_value = x` | Настройка возврата |
| `mock.Verify(..., Times.Once)` | `mock.method.assert_called_once()` | Проверка вызова |
| `WebApplicationFactory<T>` | `ASGITransport(app=app)` | HTTP тест-клиент |

---

## Итоговая карта навыков

### Реализованные концепции

| Область | Навык | Файл |
|---------|-------|------|
| **Синтаксис** | List/dict/set comprehensions | `day1/task_1_collections.py` |
| | f-strings, форматирование | `day1/task_2_strings.py` |
| | match/case (pattern matching) | `day1/task_3_pattern_matching.py` |
| | *args, **kwargs, keyword-only | `day1/task_4_args_kwargs.py` |
| **ООП** | @dataclass, __post_init__ | `domain/models.py` |
| | Operator overloading | `domain/models.py` |
| | Protocol (duck typing) | `day2/task_protocol.py` |
| | Enum с auto() | `domain/models.py` |
| **Экосистема** | pydantic-settings + .env | `config.py` |
| | uv, ruff, mypy, pytest | `day3/tooling_guide.md` |
| **Async** | asyncio.gather (Task.WhenAll) | `day4/task_1_gather.py` |
| | asyncio.Semaphore | `day4/task_1_gather.py` |
| | async context manager | `day4/task_2_context_manager.py` |
| | @asynccontextmanager | `day4/task_2_context_manager.py` |
| **FastAPI** | APIRouter, @router.post/get | `api/routers/orders.py` |
| | Pydantic request/response | `api/routers/orders.py` |
| | Depends (DI) | `api/routers/orders.py` |
| | Middleware, lifespan | `api/main.py` |
| | Exception handlers | `api/main.py` |
| **SQLAlchemy** | DeclarativeBase, mapped_column | `infrastructure/orm_models.py` |
| | relationship + lazy="selectin" | `infrastructure/orm_models.py` |
| | AsyncSession, async_sessionmaker | `infrastructure/database.py` |
| | get_session (Depends + yield) | `infrastructure/database.py` |
| **Тестирование** | pytest fixtures (scope) | `tests/conftest.py` |
| | AsyncMock (Moq аналог) | `tests/unit/test_service.py` |
| | @pytest.mark.parametrize | `tests/unit/test_domain.py` |
| | AsyncClient (httpx) | `tests/integration/test_api.py` |

### Финальная структура проекта

```
lerning-phyton/
├── src/orders/
│   ├── domain/models.py        ✅ Order, Money, OrderStatus
│   ├── application/services.py ✅ OrderService (CQRS-like)
│   ├── infrastructure/
│   │   ├── repositories.py     ✅ InMemoryOrderRepository
│   │   ├── orm_models.py       ✅ SQLAlchemy ORM
│   │   └── database.py         ✅ AsyncSession, engine
│   ├── api/
│   │   ├── routers/orders.py   ✅ CRUD endpoints
│   │   └── main.py             ✅ FastAPI app
│   └── config.py               ✅ pydantic-settings
├── tests/
│   ├── conftest.py             ✅ shared fixtures
│   ├── unit/test_domain.py     ✅ 30+ unit tests
│   ├── unit/test_service.py    ✅ AsyncMock tests
│   └── integration/test_api.py ✅ API integration tests
├── exercises/
│   ├── day1/ — синтаксис (4 файла)
│   ├── day2/ — ООП, Protocol
│   ├── day3/ — tooling guide
│   ├── day4/ — async/await (2 файла)
│   └── day6/ — Alembic guide
└── pyproject.toml              ✅ зависимости + конфигурация
```
