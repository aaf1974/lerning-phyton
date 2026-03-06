# Master Prompt — Python Learning Execution

> **Инструкция для Claude Code:** прочитай этот файл и выполни все шаги последовательно.
> Рабочий каталог: `F:\Lerning\lerning-phyton`
> После каждого шага — обязательный `git commit` с указанным сообщением.
> Не жди подтверждений между шагами — выполняй всё подряд.

---

## Контекст

Учебный проект: **Orders API** — Python для .NET разработчика (ASP.NET Core, EF Core, CQRS).
Стек: FastAPI + SQLAlchemy + Alembic + pytest + pydantic + ruff + mypy.
Принцип: не учить программированию — учить Python-идиомам через аналогии с C#.

---

## ШАГ 0 — Инициализация проекта

### 0.1 Создай структуру каталогов

```
F:\Lerning\lerning-phyton\
├── src/
│   └── orders/
│       ├── __init__.py
│       ├── domain/
│       │   ├── __init__.py
│       │   └── models.py
│       ├── application/
│       │   ├── __init__.py
│       │   └── services.py
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── orm_models.py
│       │   ├── database.py
│       │   └── repositories.py
│       └── api/
│           ├── __init__.py
│           ├── main.py
│           └── routers/
│               ├── __init__.py
│               └── orders.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── __init__.py
│   │   └── .gitkeep
│   └── integration/
│       ├── __init__.py
│       └── .gitkeep
├── exercises/
│   ├── day1/
│   │   └── .gitkeep
│   ├── day2/
│   │   └── .gitkeep
│   ├── day3/
│   │   └── .gitkeep
│   ├── day4/
│   │   └── .gitkeep
├── pyproject.toml
├── .env.example
├── README.md
└── REPORT.md
```

### 0.2 Создай файлы

**`pyproject.toml`:**
```toml
[project]
name = "python-orders"
version = "0.1.0"
description = "Orders API — Python для .NET разработчика"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "aiosqlite>=0.20.0",
    "httpx>=0.27.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "mypy>=1.10.0",
    "ruff>=0.5.0",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]

[tool.mypy]
python_version = "3.12"
strict = true
ignore_missing_imports = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**`.env.example`:**
```
DATABASE_URL=sqlite+aiosqlite:///./orders.db
APP_ENV=development
DEBUG=true
```

**`README.md`:**
```markdown
# Python Orders API

Учебный проект: REST API управления заказами.
Python для .NET разработчика — 7-дневный курс.

## Стек
- FastAPI (аналог ASP.NET Core Minimal API)
- SQLAlchemy 2.x async (аналог EF Core)
- Alembic (аналог dotnet ef migrations)
- pytest (аналог xUnit)
- pydantic (аналог FluentValidation + DataAnnotations)
- ruff (аналог StyleCop + dotnet format)
- mypy (аналог Roslyn type checking)

## Запуск
```bash
uv run uvicorn src.orders.api.main:app --reload
```

## Тесты
```bash
uv run pytest -v
```
```

**`REPORT.md`:**
```markdown
# Отчёт: Python обучение (.NET → Python)

> Профиль: ASP.NET Core / EF Core / CQRS/MediatR разработчик
> Принцип: учить Python-идиомы, не основам программирования

## Статус

| Шаг | Тема | Статус |
|-----|------|--------|
| 0 | Инициализация | ✅ |
| 1 | Синтаксис Python | ⏳ |
| 2 | ООП и типизация | ⏳ |
| 3 | Экосистема | ⏳ |
| 4 | Async/await | ⏳ |
| 5 | FastAPI | ⏳ |
| 6 | SQLAlchemy + Alembic | ⏳ |
| 7 | Тестирование | ⏳ |

## Шаг 0 — Инициализация

Создана структура проекта Orders API.

### Аналоги инструментов .NET → Python

| .NET | Python |
|------|--------|
| NuGet + .csproj | pyproject.toml + uv |
| dotnet format / StyleCop | ruff |
| Roslyn analyzers | mypy |
| appsettings.json + IOptions | pydantic-settings + .env |
| xUnit + Moq | pytest + AsyncMock |
| dotnet ef migrations add | alembic revision --autogenerate |
| dotnet ef database update | alembic upgrade head |

## Шаг 1 — Синтаксис

_Заполняется после выполнения шага 1._

## Шаг 2 — ООП

_Заполняется после выполнения шага 2._

## Шаг 3 — Экосистема

_Заполняется после выполнения шага 3._

## Шаг 4 — Async/await

_Заполняется после выполнения шага 4._

## Шаг 5 — FastAPI

_Заполняется после выполнения шага 5._

## Шаг 6 — SQLAlchemy

_Заполняется после выполнения шага 6._

## Шаг 7 — Тестирование

_Заполняется после выполнения шага 7._
```

**Все `__init__.py`** — пустые файлы.

### 0.3 Git commit

```bash
git -C "F:/Lerning/lerning-phyton" add .
git -C "F:/Lerning/lerning-phyton" commit -m "Step 0: Initialize project structure — pyproject.toml, src layout, REPORT.md"
```

---

## ШАГ 1 — Python синтаксис (C# глазами)

### 1.1 Создай `exercises/day1/task_1_collections.py`

```python
"""
День 1, Задание 1 — Коллекции и аналоги LINQ.

C# → Python:
  .Where(n => n % 2 == 0)      →  [n for n in nums if n % 2 == 0]
  .Select(n => n * n)           →  [n * n for n in nums]
  .OrderByDescending(n => n)    →  sorted(nums, reverse=True)
  .ToDictionary(k, v)           →  {k: v for k, v in items}
  dict.GetValueOrDefault(k, 0)  →  dict.get(k, 0)
"""
from collections import Counter

# --- List comprehension (аналог .Where().Select()) ---
numbers = list(range(1, 11))

# C#: numbers.Where(n => n % 2 == 0).Select(n => n * n).OrderByDescending(n => n)
even_squares = sorted([n * n for n in numbers if n % 2 == 0], reverse=True)
assert even_squares == [100, 64, 36, 16, 4]

# --- Dict comprehension (аналог .ToDictionary()) ---
squares_dict = {n: n * n for n in range(1, 6)}
assert squares_dict == {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# --- Set comprehension (уникальные значения) ---
words = "the quick brown fox jumps over the lazy dog".split()
unique_words = {w for w in words}
assert "the" in unique_words
assert len(unique_words) < len(words)  # дубли убраны

# --- Counter (аналог Dictionary + GetValueOrDefault + группировка) ---
word_count = Counter(words)
assert word_count["the"] == 2
assert word_count["fox"] == 1
top_3 = word_count.most_common(3)  # аналог .OrderByDescending().Take(3)
print(f"Top 3 words: {top_3}")

# --- dict.get() = GetValueOrDefault ---
manual_count: dict[str, int] = {}
for word in words:
    manual_count[word] = manual_count.get(word, 0) + 1
assert manual_count["the"] == 2

print("✅ Task 1 — Collections: all assertions passed")
```

### 1.2 Создай `exercises/day1/task_2_strings.py`

```python
"""
День 1, Задание 2 — f-strings и форматирование строк.

C#: $"Name: {name}, Amount: {amount:N2}"
Python: f"Name: {name}, Amount: {amount:,.2f}"
"""


def format_money(amount: float, currency: str = "USD") -> str:
    """
    Форматирует денежную сумму.

    >>> format_money(1234567.89, "USD")
    'USD 1,234,567.89'
    >>> format_money(1000.0)
    'USD 1,000.00'
    """
    return f"{currency} {amount:,.2f}"


def format_table_row(name: str, value: float, width: int = 20) -> str:
    """Выравнивание в таблице — аналог PadRight/PadLeft"""
    return f"{name:<{width}} {value:>10,.2f}"


# Тесты
assert format_money(1234567.89, "USD") == "USD 1,234,567.89"
assert format_money(1000.0) == "USD 1,000.00"
assert format_money(0.5, "RUB") == "RUB 0.50"

# Полезные форматы f-strings:
pi = 3.14159265
print(f"Pi fixed:    {pi:.2f}")          # 3.14
print(f"Pi width:    {pi:10.3f}")        # '     3.142'
print(f"Percent:     {0.756:.1%}")       # 75.6%
print(f"Hex:         {255:#x}")          # 0xff
print(f"Debug:       {pi=}")             # pi=3.14159265  (Python 3.8+)
print(f"Sci:         {1234567:.2e}")     # 1.23e+06
print(format_table_row("Revenue", 1234567.89))

print("✅ Task 2 — Strings: all assertions passed")
```

### 1.3 Создай `exercises/day1/task_3_pattern_matching.py`

```python
"""
День 1, Задание 3 — Pattern matching (match/case).

C# switch expression:
    code switch {
        200 or 201 => "Success",
        404 => "Not Found",
        >= 500 and < 600 => $"Server Error {code}",
        _ => "Unknown"
    }

Python match/case (Python 3.10+):
    match code:
        case 200 | 201: return "Success"
        case 404: return "Not Found"
        case c if 500 <= c < 600: return f"Server Error {c}"
        case _: return "Unknown"
"""
from dataclasses import dataclass


def describe_http_status(code: int) -> str:
    match code:
        case 200 | 201 | 204:
            return "Success"
        case 301 | 302:
            return "Redirect"
        case 400:
            return "Bad Request"
        case 401 | 403:
            return "Auth Error"
        case 404:
            return "Not Found"
        case code if 500 <= code < 600:
            return f"Server Error {code}"
        case _:
            return "Unknown"


@dataclass
class Ok:
    value: object


@dataclass
class Err:
    message: str


def process_result(result: Ok | Err | None) -> str:
    """Pattern matching по типу — аналог switch на типах в C#"""
    match result:
        case None:
            return "Empty"
        case Ok(value=v):
            return f"Success: {v}"
        case Err(message=m):
            return f"Error: {m}"


# Тесты
assert describe_http_status(200) == "Success"
assert describe_http_status(201) == "Success"
assert describe_http_status(404) == "Not Found"
assert describe_http_status(401) == "Auth Error"
assert describe_http_status(500) == "Server Error 500"
assert describe_http_status(503) == "Server Error 503"
assert describe_http_status(999) == "Unknown"

assert process_result(None) == "Empty"
assert process_result(Ok(42)) == "Success: 42"
assert process_result(Err("not found")) == "Error: not found"

print("✅ Task 3 — Pattern matching: all assertions passed")
```

### 1.4 Создай `exercises/day1/task_4_args_kwargs.py`

```python
"""
День 1, Задание 4 — *args и **kwargs.

C# аналоги:
  *args   →  params int[] numbers
  **kwargs →  Dictionary<string, object> options  или  именованные параметры
"""
from typing import Any


def sum_all(*numbers: int | float) -> float:
    """
    *args = params в C#
    Вызов: sum_all(1, 2, 3) или sum_all(*my_list)
    """
    return sum(numbers)


def create_config(base: str, **overrides: Any) -> dict[str, Any]:
    """
    **kwargs = произвольные именованные параметры.
    Аналог Dictionary<string, object> или dynamic.
    """
    defaults: dict[str, Any] = {
        "base": base,
        "debug": False,
        "timeout": 30,
        "retries": 3,
    }
    return {**defaults, **overrides}  # dict merge = {**a, **b}


def log(message: str, *, level: str = "INFO", prefix: str = "") -> str:
    """
    * в сигнатуре = всё после * — keyword-only аргументы.
    Аналог именованных параметров в C# (но обязательно по имени).
    """
    return f"[{level}] {prefix}{message}".strip()


# Тесты
assert sum_all(1, 2, 3) == 6
assert sum_all(1.5, 2.5) == 4.0
assert sum_all(*[10, 20, 30]) == 60  # распаковка списка

config = create_config("production", debug=True, timeout=60)
assert config["base"] == "production"
assert config["debug"] is True
assert config["timeout"] == 60
assert config["retries"] == 3  # из defaults

assert log("hello") == "[INFO] hello"
assert log("error occurred", level="ERROR", prefix=">> ") == "[ERROR] >> error occurred"

print("✅ Task 4 — Args/kwargs: all assertions passed")
```

### 1.5 Обнови REPORT.md — раздел Шаг 1

Замени строку `_Заполняется после выполнения шага 1._` на:

```markdown
## Шаг 1 — Синтаксис Python

### Ключевые аналогии C# → Python

| C# | Python | Нюанс |
|----|--------|-------|
| `.Where(n => n > 0)` | `[n for n in nums if n > 0]` | Comprehension читается слева→направо |
| `.Select(n => n*2)` | `[n*2 for n in nums]` | То же comprehension |
| `.OrderByDescending()` | `sorted(lst, reverse=True)` | Не мутирует, возвращает новый список |
| `dict.GetValueOrDefault(k,0)` | `dict.get(k, 0)` | |
| `$"{val:N2}"` | `f"{val:,.2f}"` | Формат чисел немного отличается |
| `switch expr { ... }` | `match/case` (3.10+) | Guard: `case x if x > 0` |
| `params int[]` | `*args` | `**kwargs` = именованные |
| `null` / `true` / `false` | `None` / `True` / `False` | С заглавной! |
| `x == null` | `x is None` | Всегда `is None`, не `== None` |

### Созданные файлы
- `exercises/day1/task_1_collections.py` — comprehensions, Counter
- `exercises/day1/task_2_strings.py` — f-strings форматирование
- `exercises/day1/task_3_pattern_matching.py` — match/case
- `exercises/day1/task_4_args_kwargs.py` — *args, **kwargs

Обнови строку в таблице: `| 1 | Синтаксис Python | ✅ |`
```

### 1.6 Git commit

```bash
git -C "F:/Lerning/lerning-phyton" add .
git -C "F:/Lerning/lerning-phyton" commit -m "Step 1: Python syntax — comprehensions, f-strings, pattern matching, args/kwargs"
```

---

## ШАГ 2 — ООП и типизация

### 2.1 Создай `src/orders/domain/models.py`

```python
"""
Доменные модели Orders API.

Аналогии C# → Python:
  record Money { }          →  @dataclass class Money
  interface IOrderRepository →  Protocol (duck typing, без наследования)
  class Repo<T>              →  class Repo(Generic[T])
  ToString()                 →  __str__
  IEquatable<T>              →  __eq__ (dataclass генерирует автоматически)
  конструктор с проверками  →  __post_init__
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from decimal import Decimal
from enum import Enum, auto
from functools import reduce
from uuid import UUID, uuid4


class OrderStatus(Enum):
    PENDING = auto()
    CONFIRMED = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


@dataclass
class Money:
    """
    Value Object — сравнивается по значению.
    @dataclass автоматически генерирует __eq__ и __repr__.
    """
    amount: Decimal
    currency: str = "RUB"

    def __post_init__(self) -> None:
        """Аналог конструктора с проверками в C#."""
        if self.amount < 0:
            raise ValueError(f"Amount cannot be negative: {self.amount}")
        object.__setattr__(self, "amount", Decimal(str(self.amount)))

    def __add__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} != {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, factor: int | Decimal) -> Money:
        return Money(self.amount * Decimal(str(factor)), self.currency)

    def __str__(self) -> str:
        return f"{self.amount:,.2f} {self.currency}"


@dataclass
class OrderItem:
    product_id: UUID
    name: str
    price: Money
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(f"Quantity must be positive: {self.quantity}")
        if not self.name.strip():
            raise ValueError("Name cannot be empty")

    @property
    def total(self) -> Money:
        """C# аналог: public Money Total => Price * Quantity;"""
        return self.price * self.quantity


@dataclass
class Order:
    id: UUID = field(default_factory=uuid4)
    items: list[OrderItem] = field(default_factory=list)
    status: OrderStatus = field(default=OrderStatus.PENDING)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def add_item(self, item: OrderItem) -> None:
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"Cannot add items to order in {self.status.name} status")
        self.items.append(item)

    @property
    def total(self) -> Money:
        """Сумма позиций — аналог LINQ .Sum()"""
        if not self.items:
            return Money(Decimal("0"))
        return reduce(lambda acc, item: acc + item.total, self.items)

    def confirm(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"Cannot confirm order in {self.status.name} status")
        self.status = OrderStatus.CONFIRMED

    def cancel(self) -> None:
        if self.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise ValueError(f"Cannot cancel order in {self.status.name} status")
        self.status = OrderStatus.CANCELLED

    def __str__(self) -> str:
        return (
            f"Order({str(self.id)[:8]}, "
            f"status={self.status.name}, "
            f"items={len(self.items)}, "
            f"total={self.total})"
        )
```

### 2.2 Создай `exercises/day2/task_protocol.py`

```python
"""
День 2 — Protocol (аналог interface в C#).

Ключевое отличие:
  C#: class Foo : IFoo { }        — номинальная типизация (явное объявление)
  Python: class Foo — структурная типизация (duck typing)
          Класс реализует Protocol автоматически если у него есть нужные методы.
"""
from typing import Protocol, runtime_checkable
from uuid import UUID

from orders.domain.models import Order


@runtime_checkable  # позволяет isinstance() проверки
class IOrderRepository(Protocol):
    """
    Аналог:
    public interface IOrderRepository {
        Task<Order?> GetByIdAsync(Guid id);
        Task AddAsync(Order order);
        Task UpdateAsync(Order order);
    }
    """
    async def get_by_id(self, id: UUID) -> Order | None: ...
    async def add(self, entity: Order) -> None: ...
    async def update(self, entity: Order) -> None: ...
    async def get_all(self) -> list[Order]: ...


class InMemoryOrderRepository:
    """
    Реализация БЕЗ явного 'implements IOrderRepository'.
    Python проверяет структуру (наличие методов), а не наследование.
    """
    def __init__(self) -> None:
        self._store: dict[UUID, Order] = {}

    async def get_by_id(self, id: UUID) -> Order | None:
        return self._store.get(id)

    async def add(self, entity: Order) -> None:
        self._store[entity.id] = entity

    async def update(self, entity: Order) -> None:
        if entity.id not in self._store:
            raise KeyError(f"Order {entity.id} not found")
        self._store[entity.id] = entity

    async def get_all(self) -> list[Order]:
        return list(self._store.values())

    def __len__(self) -> int:
        return len(self._store)


# Демонстрация duck typing
repo = InMemoryOrderRepository()
print(f"Is IOrderRepository (without inheritance): {isinstance(repo, IOrderRepository)}")
# → True! Без единой строки 'implements'
```

### 2.3 Обнови REPORT.md — раздел Шаг 2

Замени `_Заполняется после выполнения шага 2._` на:

```markdown
## Шаг 2 — ООП и типизация

### Ключевые аналогии

| C# | Python | Важный нюанс |
|----|--------|--------------|
| `record Money` | `@dataclass class Money` | `__post_init__` = конструктор с валидацией |
| `interface IFoo` | `Protocol` | Duck typing — без явного наследования |
| `abstract class` | `class X(ABC)` | Явное наследование от ABC |
| `class Foo<T>` | `class Foo(Generic[T])` | TypeVar + Generic |
| `ToString()` | `__str__` | dunder методы |
| `get; set;` property | `@property` / `@x.setter` | Декораторы |

### Protocol vs ABC
- **Protocol** = структурная типизация. Класс реализует протокол автоматически если у него есть нужные методы — без `implements`.
- **ABC** = номинальная типизация. Нужно явное наследование `class Foo(ABC)`, как в C#.

Обнови строку в таблице: `| 2 | ООП и типизация | ✅ |`
```

### 2.4 Git commit

```bash
git -C "F:/Lerning/lerning-phyton" add .
git -C "F:/Lerning/lerning-phyton" commit -m "Step 2: OOP — dataclass, Protocol (duck typing), domain models Order/Money"
```

---

## ШАГ 3 — Экосистема и структура проекта

### 3.1 Создай `src/orders/__init__.py` (не пустой)

```python
"""
Orders — учебный пакет Python для .NET разработчика.

Этот файл делает папку Python-пакетом (аналог namespace в C#).
Можно экспортировать публичный API модуля через __all__.
"""
__version__ = "0.1.0"
```

### 3.2 Создай `src/orders/config.py`

```python
"""
Конфигурация приложения.

Аналог в .NET:
  appsettings.json + IOptions<AppSettings> + IConfiguration
  В Python: pydantic-settings читает из .env файла или переменных окружения.
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # БД
    database_url: str = Field(default="sqlite+aiosqlite:///./orders.db")

    # Приложение
    app_env: str = Field(default="development")
    debug: bool = Field(default=True)
    app_title: str = Field(default="Orders API")
    app_version: str = Field(default="0.1.0")

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


# Синглтон — аналог IOptions<Settings> зарегистрированного как Singleton
settings = Settings()
```

### 3.3 Создай `exercises/day3/task_ecosystem.md`

```markdown
# День 3 — Экосистема Python для .NET разработчика

## Установленные инструменты

| .NET | Python | Команда |
|------|--------|---------|
| NuGet + .csproj | pyproject.toml + uv | `uv add fastapi` |
| dotnet format | ruff format | `ruff format .` |
| StyleCop / Roslyn | ruff check | `ruff check .` |
| Roslyn type checker | mypy | `mypy src/` |
| xUnit | pytest | `pytest -v` |
| dotnet ef | alembic | `alembic upgrade head` |

## Структура пакета Python

```
src/orders/             ← пакет (есть __init__.py)
├── __init__.py         ← делает папку пакетом (аналог namespace)
├── domain/
│   ├── __init__.py     ← вложенный пакет
│   └── models.py
```

## Команды проекта

```bash
# Зависимости (аналог dotnet restore / dotnet add package)
uv sync              # установить из pyproject.toml
uv add fastapi       # добавить зависимость
uv add --dev ruff    # dev зависимость

# Запуск
uv run uvicorn src.orders.api.main:app --reload

# Качество кода
uv run ruff check .        # линтинг
uv run ruff format .       # форматирование
uv run mypy src/           # типы

# Тесты
uv run pytest -v
uv run pytest --cov=src/orders
```
```

### 3.4 Обнови REPORT.md — раздел Шаг 3

Замени `_Заполняется после выполнения шага 3._` на:

```markdown
## Шаг 3 — Экосистема

### Аналоги команд

| .NET | Python |
|------|--------|
| `dotnet add package X` | `uv add X` |
| `dotnet format` | `uv run ruff format .` |
| `dotnet build` (тип-чек) | `uv run mypy src/` |
| `dotnet test` | `uv run pytest -v` |

### pyproject.toml = .csproj + global.json + .editorconfig
Один файл описывает: зависимости, версию Python, настройки ruff/mypy/pytest.

Обнови строку в таблице: `| 3 | Экосистема | ✅ |`
```

### 3.5 Git commit

```bash
git -C "F:/Lerning/lerning-phyton" add .
git -C "F:/Lerning/lerning-phyton" commit -m "Step 3: Ecosystem — config (pydantic-settings), package structure, tooling docs"
```

---

## ШАГ 4 — Async/await

### 4.1 Создай `exercises/day4/task_1_gather.py`

```python
"""
День 4, Задание 1 — asyncio.gather() = Task.WhenAll()

КРИТИЧЕСКОЕ ОТЛИЧИЕ от .NET:
  C#: Task запускается сразу при создании
  Python: coroutine НЕ запускается без await или create_task()

  result = fetch_data()        # ← это НЕ результат, это объект coroutine!
  result = await fetch_data()  # ← вот так правильно
"""
import asyncio
import time
from typing import Any


async def fetch_user(user_id: int) -> dict[str, Any]:
    """Имитация HTTP запроса."""
    await asyncio.sleep(0.1)  # I/O задержка
    return {"id": user_id, "name": f"User {user_id}", "email": f"user{user_id}@example.com"}


async def fetch_sequential(user_ids: list[int]) -> list[dict[str, Any]]:
    """Последовательно — как обычный foreach."""
    results = []
    for uid in user_ids:
        user = await fetch_user(uid)
        results.append(user)
    return results


async def fetch_parallel(user_ids: list[int]) -> list[dict[str, Any]]:
    """
    Параллельно — asyncio.gather() = Task.WhenAll()

    C#: var users = await Task.WhenAll(userIds.Select(GetUserAsync));
    Python: users = await asyncio.gather(*[fetch_user(uid) for uid in user_ids])
    """
    tasks = [fetch_user(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks)
    return list(results)


async def fetch_with_semaphore(user_ids: list[int], max_concurrent: int = 5) -> list[dict[str, Any]]:
    """
    Ограничение параллелизма — asyncio.Semaphore = SemaphoreSlim

    C#: var semaphore = new SemaphoreSlim(5);
        await semaphore.WaitAsync();
        try { ... } finally { semaphore.Release(); }

    Python: async with semaphore:  ← автоматический acquire/release
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_limited(uid: int) -> dict[str, Any]:
        async with semaphore:
            return await fetch_user(uid)

    return list(await asyncio.gather(*[fetch_limited(uid) for uid in user_ids]))


async def main() -> None:
    user_ids = list(range(1, 11))

    start = time.perf_counter()
    seq = await fetch_sequential(user_ids[:3])
    seq_time = time.perf_counter() - start
    print(f"Sequential (3 users): {seq_time:.2f}s")

    start = time.perf_counter()
    par = await fetch_parallel(user_ids[:3])
    par_time = time.perf_counter() - start
    print(f"Parallel (3 users):   {par_time:.2f}s  ({seq_time/par_time:.1f}x faster)")

    limited = await fetch_with_semaphore(user_ids, max_concurrent=3)
    print(f"With semaphore: got {len(limited)} users")


asyncio.run(main())
```

### 4.2 Создай `exercises/day4/task_2_context_manager.py`

```python
"""
День 4, Задание 2 — Async Context Manager = IAsyncDisposable

C#: await using var db = new DatabaseConnection();
Python: async with DatabaseConnection() as db:
"""
import asyncio
from contextlib import asynccontextmanager
from types import TracebackType
from typing import AsyncGenerator, Self


class DatabaseConnection:
    """
    __aenter__ = начало using блока
    __aexit__  = конец using блока (автоматический вызов Dispose)
    """
    def __init__(self, url: str = "sqlite:///test.db") -> None:
        self._url = url
        self._connected = False

    async def __aenter__(self) -> Self:
        await asyncio.sleep(0.01)  # имитация подключения
        self._connected = True
        print(f"Connected to {self._url}")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await asyncio.sleep(0.01)  # имитация отключения
        self._connected = False
        print("Disconnected")
        # None = не подавлять исключения (как Dispose в C#)

    async def execute(self, query: str) -> list[dict[str, str]]:
        if not self._connected:
            raise RuntimeError("Not connected")
        await asyncio.sleep(0.01)
        return [{"result": "ok", "query": query}]


# Декораторный стиль — asynccontextmanager = удобнее для простых случаев
@asynccontextmanager
async def get_db(url: str = "sqlite:///test.db") -> AsyncGenerator[DatabaseConnection, None]:
    """Этот стиль используется в FastAPI Depends(get_db)"""
    db = DatabaseConnection(url)
    async with db:
        yield db  # yield разделяет setup от teardown


async def main() -> None:
    # Стиль 1: класс
    async with DatabaseConnection() as db:
        result = await db.execute("SELECT * FROM orders")
        print(f"Result: {result}")

    # Стиль 2: декоратор
    async with get_db() as db:
        result = await db.execute("SELECT 1")
        print(f"Result: {result}")


asyncio.run(main())
```

### 4.3 Обнови REPORT.md — раздел Шаг 4

Замени `_Заполняется после выполнения шага 4._` на:

```markdown
## Шаг 4 — Async/await

### Главные отличия от .NET async

| .NET | Python | Критично |
|------|--------|----------|
| Task запускается сразу | coroutine без await = объект, не результат | ⚠️ Частая ошибка |
| Многопоточный | Однопоточный event loop | CPU-bound → ProcessPoolExecutor |
| Task.WhenAll() | asyncio.gather() | |
| SemaphoreSlim | asyncio.Semaphore | |
| IAsyncDisposable | async with (__aenter__/__aexit__) | |
| IAsyncEnumerable | async for / AsyncGenerator | |

### Ловушка №1
`result = fetch_data()` — НЕ запускает coroutine!
`result = await fetch_data()` — правильно.
Python не покажет ошибку при создании coroutine без await.

Обнови строку в таблице: `| 4 | Async/await | ✅ |`
```

### 4.4 Git commit

```bash
git -C "F:/Lerning/lerning-phyton" add .
git -C "F:/Lerning/lerning-phyton" commit -m "Step 4: Async/await — gather, Semaphore, async context managers"
```

---

## ШАГ 5 — FastAPI

### 5.1 Создай `src/orders/application/services.py`

```python
"""Application Service — аналог MediatR Handler / ApplicationService."""
from decimal import Decimal
from uuid import UUID

from orders.domain.models import Money, Order, OrderItem


class OrderService:
    def __init__(self, repository: object) -> None:
        self._repo = repository  # type: ignore[assignment]

    async def create_order(self, items_data: list[dict]) -> Order:  # type: ignore[type-arg]
        order = Order()
        for item in items_data:
            order.add_item(OrderItem(
                product_id=item["product_id"],
                name=item["name"],
                price=Money(Decimal(str(item["price"]))),
                quantity=item["quantity"],
            ))
        await self._repo.add(order)  # type: ignore[union-attr]
        return order

    async def get_order(self, order_id: UUID) -> Order | None:
        return await self._repo.get_by_id(order_id)  # type: ignore[union-attr]

    async def confirm_order(self, order_id: UUID) -> Order:
        order = await self._repo.get_by_id(order_id)  # type: ignore[union-attr]
        if order is None:
            raise ValueError(f"Order {order_id} not found")
        order.confirm()
        await self._repo.update(order)  # type: ignore[union-attr]
        return order

    async def get_all_orders(self) -> list[Order]:
        return await self._repo.get_all()  # type: ignore[union-attr]
```

### 5.2 Создай `src/orders/infrastructure/repositories.py`

```python
"""In-memory репозиторий — для разработки и тестов."""
from uuid import UUID

from orders.domain.models import Order


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._store: dict[UUID, Order] = {}

    async def get_by_id(self, id: UUID) -> Order | None:
        return self._store.get(id)

    async def add(self, entity: Order) -> None:
        self._store[entity.id] = entity

    async def update(self, entity: Order) -> None:
        if entity.id not in self._store:
            raise KeyError(f"Order {entity.id} not found")
        self._store[entity.id] = entity

    async def get_all(self) -> list[Order]:
        return list(self._store.values())
```

### 5.3 Создай `src/orders/api/routers/orders.py`

```python
"""
Orders Router — аналог ApiController в ASP.NET Core.

FastAPI DI vs ASP.NET Core DI:
  C#: constructor injection / [FromServices]
  Python: def endpoint(service = Depends(get_service))

Pydantic Field vs DataAnnotations:
  C#: [Required] [Range(1, 1000)] string Name
  Python: name: str = Field(min_length=1, max_length=200)
          price: Decimal = Field(gt=0)
"""
from decimal import Decimal
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from orders.application.services import OrderService
from orders.infrastructure.repositories import InMemoryOrderRepository

router = APIRouter(prefix="/orders", tags=["orders"])

# Singleton репозиторий (в продакшне — через DI с правильным lifetime)
_repo = InMemoryOrderRepository()


# --- Request / Response модели (аналог ViewModel + DTO) ---

class OrderItemRequest(BaseModel):
    product_id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=200)
    price: Decimal = Field(gt=0, decimal_places=2)
    quantity: int = Field(gt=0, le=1000)


class CreateOrderRequest(BaseModel):
    items: list[OrderItemRequest] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    product_id: UUID
    name: str
    price: str
    quantity: int
    total: str


class OrderResponse(BaseModel):
    id: UUID
    status: str
    total: str
    items_count: int
    items: list[OrderItemResponse]


# --- Dependency (аналог AddScoped + constructor injection) ---

def get_service() -> OrderService:
    """
    FastAPI вызывает при каждом запросе.
    Аналог AddScoped<OrderService> в ASP.NET Core.
    """
    return OrderService(_repo)


# --- Endpoints ---

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
async def create_order(
    request: CreateOrderRequest,
    service: OrderService = Depends(get_service),
) -> OrderResponse:
    order = await service.create_order([item.model_dump() for item in request.items])
    return _map(order)


@router.get("/", response_model=list[OrderResponse])
async def list_orders(service: OrderService = Depends(get_service)) -> list[OrderResponse]:
    return [_map(o) for o in await service.get_all_orders()]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: UUID, service: OrderService = Depends(get_service)) -> OrderResponse:
    order = await service.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return _map(order)


@router.put("/{order_id}/confirm", response_model=OrderResponse)
async def confirm_order(
    order_id: UUID,
    service: OrderService = Depends(get_service),
) -> OrderResponse:
    try:
        return _map(await service.confirm_order(order_id))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


def _map(order: object) -> OrderResponse:  # type: ignore[type-arg]
    from orders.domain.models import Order as DomainOrder
    o: DomainOrder = order  # type: ignore[assignment]
    return OrderResponse(
        id=o.id,
        status=o.status.name,
        total=str(o.total),
        items_count=len(o.items),
        items=[
            OrderItemResponse(
                product_id=i.product_id,
                name=i.name,
                price=str(i.price),
                quantity=i.quantity,
                total=str(i.total),
            )
            for i in o.items
        ],
    )
```

### 5.4 Создай `src/orders/api/main.py`

```python
"""
FastAPI точка входа — аналог Program.cs.

lifespan = IHostedService.StartAsync/StopAsync
app.include_router = app.MapGroup() / UseRouting()
@app.middleware = app.Use(async (ctx, next) => ...)
@app.exception_handler = IExceptionHandler
"""
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from orders.api.routers.orders import router as orders_router
from orders.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print(f"▶ Starting {settings.app_title} v{settings.app_version} [{settings.app_env}]")
    yield
    print("■ Shutdown complete")


app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(orders_router)


@app.middleware("http")
async def timing_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}s"
    return response


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": settings.app_version}
```

### 5.5 Обнови REPORT.md — раздел Шаг 5

Замени `_Заполняется после выполнения шага 5._` на:

```markdown
## Шаг 5 — FastAPI

### Ключевые аналогии

| ASP.NET Core | FastAPI |
|---|---|
| `[ApiController]` + `[Route]` | `APIRouter(prefix=..., tags=[...])` |
| `[FromServices]` / constructor DI | `Depends(get_service)` |
| `DataAnnotations [Required][Range]` | `pydantic Field(min_length=1, gt=0)` |
| Swagger (Swashbuckle) | Встроен, `/docs` |
| `IMiddleware` | `@app.middleware("http")` |
| `IExceptionHandler` | `@app.exception_handler(Type)` |
| `IHostedService` | `lifespan` context manager |
| `ActionResult<T>` | `response_model=OrderResponse` |

Запуск: `uv run uvicorn src.orders.api.main:app --reload`
Swagger: http://localhost:8000/docs

Обнови строку в таблице: `| 5 | FastAPI | ✅ |`
```

### 5.6 Git commit

```bash
git -C "F:/Lerning/lerning-phyton" add .
git -C "F:/Lerning/lerning-phyton" commit -m "Step 5: FastAPI CRUD — routers, Pydantic models, Depends DI, middleware"
```

---

## ШАГ 6 — SQLAlchemy + Alembic

### 6.1 Создай `src/orders/infrastructure/orm_models.py`

```python
"""
SQLAlchemy ORM модели.

Аналогии EF Core → SQLAlchemy:
  DbContext            → AsyncSession
  IEntityTypeConfig    → DeclarativeBase + класс с атрибутами
  .Include()           → selectinload() — явный eager loading
  Navigation property  → relationship()
  .FirstOrDefaultAsync → scalar_one_or_none()
  .ToListAsync()       → .scalars().all()
"""
import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс — аналог OnModelCreating."""
    pass


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="PENDING")
    created_at: Mapped[str] = mapped_column(String(50), nullable=False)

    # relationship = Navigation property
    # lazy="selectin" = всегда eager loading (как .Include() по умолчанию)
    items: Mapped[list["OrderItemModel"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="RUB")
    quantity: Mapped[int] = mapped_column(nullable=False)

    order: Mapped["OrderModel"] = relationship(back_populates="items")
```

### 6.2 Создай `src/orders/infrastructure/database.py`

```python
"""
Database setup — аналог DbContext + DbContextFactory.

get_session() используется в FastAPI Depends:
  async def endpoint(session: AsyncSession = Depends(get_session))
  = аналог constructor injection DbContext с AddScoped lifetime
"""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from orders.config import settings
from orders.infrastructure.orm_models import Base

engine = create_async_engine(settings.database_url, echo=settings.debug)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,  # объекты не протухают после commit (важно!)
    autocommit=False,
    autoflush=False,
)


async def create_tables() -> None:
    """Создать таблицы без Alembic — только для тестов."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency для FastAPI.
    Новая сессия на каждый HTTP запрос (AddScoped lifetime).
    auto-commit при успехе, auto-rollback при исключении.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### 6.3 Создай `exercises/day6/task_alembic.md`

```markdown
# День 6 — Alembic миграции (аналог dotnet ef)

## Команды

| dotnet ef | alembic |
|-----------|---------|
| `dotnet ef migrations add InitialCreate` | `alembic revision --autogenerate -m "initial_create"` |
| `dotnet ef database update` | `alembic upgrade head` |
| `dotnet ef database update PreviousMigration` | `alembic downgrade -1` |
| `dotnet ef migrations list` | `alembic history` |
| `dotnet ef migrations remove` | `alembic downgrade -1` + удалить файл |

## Инициализация (один раз)

```bash
uv run alembic init alembic
```

Затем в `alembic/env.py` добавить:
```python
from orders.infrastructure.orm_models import Base
from orders.config import settings

config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata
```

## Рабочий флоу

```bash
# 1. Создать миграцию после изменения ORM моделей
uv run alembic revision --autogenerate -m "add_user_table"

# 2. Применить
uv run alembic upgrade head

# 3. Проверить текущую версию
uv run alembic current

# 4. Откатить последнюю миграцию
uv run alembic downgrade -1
```
```

### 6.4 Обнови REPORT.md — раздел Шаг 6

Замени `_Заполняется после выполнения шага 6._` на:

```markdown
## Шаг 6 — SQLAlchemy + Alembic

### Аналогии EF Core → SQLAlchemy

| EF Core | SQLAlchemy | |
|---------|-----------|---|
| DbContext | AsyncSession | Сессия = Unit of Work |
| `.Include(o => o.Items)` | `selectinload(OrderModel.items)` | Явный eager loading |
| `.FirstOrDefaultAsync()` | `.scalar_one_or_none()` | |
| `.ToListAsync()` | `.scalars().all()` | |
| Navigation property | `relationship()` | lazy="selectin" = всегда eager |
| `dotnet ef migrations add` | `alembic revision --autogenerate` | |
| `dotnet ef database update` | `alembic upgrade head` | |

### Важные отличия
- Нет LINQ — запросы через `select()` функцию
- Lazy loading в async по умолчанию ОТКЛЮЧЁН — используй `selectinload()`
- `expire_on_commit=False` — объекты не протухают после commit

Обнови строку в таблице: `| 6 | SQLAlchemy + Alembic | ✅ |`
```

### 6.5 Git commit

```bash
git -C "F:/Lerning/lerning-phyton" add .
git -C "F:/Lerning/lerning-phyton" commit -m "Step 6: SQLAlchemy ORM models, AsyncSession setup, Alembic migration guide"
```

---

## ШАГ 7 — Тестирование + финальная сборка

### 7.1 Создай `tests/conftest.py`

```python
"""
Shared fixtures — аналог базового класса тестов в xUnit.

@pytest.fixture с yield = [SetUp] + [TearDown]
scope="session" = [ClassInitialize] — один раз на всю сессию
scope="function" = [SetUp] — перед каждым тестом (default)
"""
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from orders.api.main import app
from orders.infrastructure.orm_models import Base


@pytest.fixture(scope="session")
async def test_engine():
    """In-memory SQLite — изолированная БД для тестов."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine):  # type: ignore[no-untyped-def]
    """Сессия с откатом после каждого теста — изоляция."""
    factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with factory() as session:
        yield session
        await session.rollback()  # ← откат = изоляция тестов


@pytest.fixture
async def client() -> AsyncClient:
    """
    Тестовый HTTP клиент.
    Аналог WebApplicationFactory<Program> в ASP.NET Core.
    ASGITransport = не делает реальных HTTP запросов.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as c:
        yield c
```

### 7.2 Создай `tests/unit/test_domain.py`

```python
"""
Unit тесты доменных моделей.

pytest vs xUnit:
  [Fact]              →  def test_...()
  [Theory+InlineData] →  @pytest.mark.parametrize
  Assert.Equal(e, a)  →  assert actual == expected
  Assert.Throws<T>    →  with pytest.raises(T, match="...")
"""
import pytest
from decimal import Decimal
from uuid import uuid4

from orders.domain.models import Money, Order, OrderItem, OrderStatus


class TestMoney:
    def test_add_same_currency(self) -> None:
        result = Money(Decimal("10.00")) + Money(Decimal("5.50"))
        assert result.amount == Decimal("15.50")
        assert result.currency == "RUB"

    def test_add_different_currencies_raises(self) -> None:
        with pytest.raises(ValueError, match="Currency mismatch"):
            Money(Decimal("10"), "RUB") + Money(Decimal("5"), "USD")

    def test_negative_amount_raises(self) -> None:
        with pytest.raises(ValueError, match="cannot be negative"):
            Money(Decimal("-1"))

    @pytest.mark.parametrize("amount,factor,expected", [
        ("10.00", 2, "20.00"),
        ("5.50", 3, "16.50"),
        ("100.00", 1, "100.00"),
        ("0.01", 100, "1.00"),
    ])
    def test_multiply(self, amount: str, factor: int, expected: str) -> None:
        result = Money(Decimal(amount)) * factor
        assert result.amount == Decimal(expected)


class TestOrderItem:
    def test_total_is_price_times_quantity(self) -> None:
        item = OrderItem(uuid4(), "Widget", Money(Decimal("10.00")), 3)
        assert item.total.amount == Decimal("30.00")

    def test_zero_quantity_raises(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            OrderItem(uuid4(), "Widget", Money(Decimal("10")), 0)

    def test_empty_name_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            OrderItem(uuid4(), "   ", Money(Decimal("10")), 1)


class TestOrder:
    def test_new_order_is_pending(self) -> None:
        assert Order().status == OrderStatus.PENDING

    def test_add_item_increases_count(self) -> None:
        order = Order()
        order.add_item(OrderItem(uuid4(), "Widget", Money(Decimal("10")), 1))
        assert len(order.items) == 1

    def test_total_is_sum_of_items(self) -> None:
        order = Order()
        order.add_item(OrderItem(uuid4(), "A", Money(Decimal("10.00")), 2))  # 20
        order.add_item(OrderItem(uuid4(), "B", Money(Decimal("5.50")), 1))   # 5.50
        assert order.total.amount == Decimal("25.50")

    def test_empty_order_total_is_zero(self) -> None:
        assert Order().total.amount == Decimal("0")

    def test_confirm_changes_status(self) -> None:
        order = Order()
        order.confirm()
        assert order.status == OrderStatus.CONFIRMED

    def test_cannot_confirm_twice(self) -> None:
        order = Order()
        order.confirm()
        with pytest.raises(ValueError, match="Cannot confirm"):
            order.confirm()

    def test_cannot_add_item_to_confirmed_order(self) -> None:
        order = Order()
        order.confirm()
        with pytest.raises(ValueError, match="Cannot add"):
            order.add_item(OrderItem(uuid4(), "A", Money(Decimal("10")), 1))
```

### 7.3 Создай `tests/unit/test_service.py`

```python
"""
Unit тесты сервиса с мокированием.

AsyncMock — аналог Mock<IOrderRepository>() из Moq.
Автоматически делает async методы awaitable.

Moq:      mock.Setup(r => r.GetByIdAsync(...)).Returns(null)
AsyncMock: mock_repo.get_by_id.return_value = None
"""
import pytest
from decimal import Decimal
from uuid import uuid4
from unittest.mock import AsyncMock

from orders.application.services import OrderService
from orders.domain.models import Order, OrderStatus


@pytest.fixture
def mock_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def service(mock_repo: AsyncMock) -> OrderService:
    return OrderService(mock_repo)


async def test_get_order_returns_none_when_not_found(
    service: OrderService, mock_repo: AsyncMock
) -> None:
    mock_repo.get_by_id.return_value = None
    assert await service.get_order(uuid4()) is None
    mock_repo.get_by_id.assert_called_once()


async def test_create_order_calls_repo_add(
    service: OrderService, mock_repo: AsyncMock
) -> None:
    items = [{"product_id": uuid4(), "name": "Widget", "price": "10.00", "quantity": 2}]
    order = await service.create_order(items)
    mock_repo.add.assert_called_once()  # аналог mock.Verify(Times.Once)
    saved: Order = mock_repo.add.call_args[0][0]
    assert len(saved.items) == 1
    assert saved.status == OrderStatus.PENDING


async def test_confirm_raises_when_order_not_found(
    service: OrderService, mock_repo: AsyncMock
) -> None:
    mock_repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match="not found"):
        await service.confirm_order(uuid4())


async def test_confirm_updates_repo(
    service: OrderService, mock_repo: AsyncMock
) -> None:
    existing = Order()
    mock_repo.get_by_id.return_value = existing
    result = await service.confirm_order(existing.id)
    assert result.status == OrderStatus.CONFIRMED
    mock_repo.update.assert_called_once_with(existing)
```

### 7.4 Создай `tests/integration/test_api.py`

```python
"""
Integration тесты FastAPI.
Аналог WebApplicationFactory<Program> + HttpClient в ASP.NET Core.
"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


async def test_health_check(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_create_order_returns_201(client: AsyncClient) -> None:
    response = await client.post("/orders/", json={
        "items": [{"name": "Python Book", "price": "1500.00", "quantity": 1}]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "PENDING"
    assert data["items_count"] == 1
    assert "id" in data


async def test_create_order_validates_negative_price(client: AsyncClient) -> None:
    response = await client.post("/orders/", json={
        "items": [{"name": "Widget", "price": "-10.00", "quantity": 1}]
    })
    assert response.status_code == 422  # Pydantic validation error


async def test_get_order_404_for_unknown(client: AsyncClient) -> None:
    response = await client.get(f"/orders/{uuid4()}")
    assert response.status_code == 404


async def test_confirm_order_flow(client: AsyncClient) -> None:
    """Тест полного флоу: создать → получить → подтвердить → нельзя подтвердить снова."""
    # Create
    create = await client.post("/orders/", json={
        "items": [{"name": "Item", "price": "100.00", "quantity": 2}]
    })
    assert create.status_code == 201
    order_id = create.json()["id"]

    # Get
    get = await client.get(f"/orders/{order_id}")
    assert get.status_code == 200

    # Confirm
    confirm = await client.put(f"/orders/{order_id}/confirm")
    assert confirm.status_code == 200
    assert confirm.json()["status"] == "CONFIRMED"

    # Cannot confirm again → 400
    again = await client.put(f"/orders/{order_id}/confirm")
    assert again.status_code == 400
```

### 7.5 Обнови REPORT.md — раздел Шаг 7 и итоговую таблицу

Замени `_Заполняется после выполнения шага 7._` на:

```markdown
## Шаг 7 — Тестирование

### pytest vs xUnit

| xUnit | pytest | |
|-------|--------|---|
| `[Fact]` | `def test_...()` | Имя начинается с test_ |
| `[Theory + InlineData]` | `@pytest.mark.parametrize` | |
| `[SetUp]/[TearDown]` | `@pytest.fixture` с `yield` | yield разделяет setup/teardown |
| Базовый класс тестов | `conftest.py` | Fixtures автодискавери |
| `Mock<T>` из Moq | `AsyncMock` | Для async методов |
| `WebApplicationFactory` | `AsyncClient + ASGITransport` | |
| `Assert.Throws<T>` | `with pytest.raises(T, match="...")` | |

### Запуск тестов

```bash
uv run pytest -v                          # все тесты
uv run pytest tests/unit/ -v             # только unit
uv run pytest tests/integration/ -v     # только integration
uv run pytest -k "test_confirm" -v      # по имени
```

Обнови ВСЕ строки таблицы статусов на ✅.
```

### 7.6 Git commit — финальный

```bash
git -C "F:/Lerning/lerning-phyton" add .
git -C "F:/Lerning/lerning-phyton" commit -m "Step 7: pytest — unit tests (AsyncMock), integration tests, conftest fixtures"
```

---

## Проверка результата

После выполнения всех шагов в `F:\Lerning\lerning-phyton` должно быть:

```
8 коммитов:
  Step 0: Initialize project structure
  Step 1: Python syntax — comprehensions, f-strings, pattern matching, args/kwargs
  Step 2: OOP — dataclass, Protocol (duck typing), domain models Order/Money
  Step 3: Ecosystem — config (pydantic-settings), package structure, tooling docs
  Step 4: Async/await — gather, Semaphore, async context managers
  Step 5: FastAPI CRUD — routers, Pydantic models, Depends DI, middleware
  Step 6: SQLAlchemy ORM models, AsyncSession setup, Alembic migration guide
  Step 7: pytest — unit tests (AsyncMock), integration tests, conftest fixtures
```

Проверь командой:
```bash
git -C "F:/Lerning/lerning-phyton" log --oneline
```
