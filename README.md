# Python Orders API — Учебный проект

Проект создан в рамках недельного обучения Python для .NET разработчика.

## Структура

```
src/orders/         — основное приложение (Clean Architecture)
  domain/           — доменные модели (Order, Money, OrderStatus)
  application/      — сервисы (OrderService)
  infrastructure/   — репозитории, ORM, БД (SQLAlchemy)
  api/              — FastAPI роутеры и main.py
tests/
  unit/             — юнит-тесты (pytest, AsyncMock)
  integration/      — интеграционные тесты (AsyncClient)
exercises/
  day1/             — синтаксис Python
  day2/             — ООП, Protocol, dataclass
  day3/             — экосистема, инструменты
  day4/             — async/await
```

## Запуск

```bash
uv run uvicorn src.orders.api.main:app --reload
```

## Тесты

```bash
uv run pytest -v
```

## Инструменты (.NET → Python)

| .NET | Python |
|------|--------|
| `dotnet add package` | `uv add` |
| `dotnet format` | `ruff format .` |
| Roslyn analyzers | `mypy src/` |
| xUnit | `pytest` |
| `dotnet ef migrations add` | `alembic revision --autogenerate` |
