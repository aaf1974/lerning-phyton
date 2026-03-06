# Отчёт об обучении Python (для .NET разработчика)

> Начало: 2026-03-06
> Профиль: ASP.NET Core / EF Core / CQRS разработчик
> Цель: освоить Python-идиомы за 7 дней

---

## Статус прохождения

| Шаг | Тема | Статус | Коммит |
|-----|------|--------|--------|
| 0 | Инициализация проекта | ✅ Выполнен | Step 0 |
| 1 | Python синтаксис | ⏳ Ожидает | — |
| 2 | ООП и типизация | ⏳ Ожидает | — |
| 3 | Экосистема и инструменты | ⏳ Ожидает | — |
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

*(Заполняется агентом python-step-1-syntax)*

---

## Шаг 2 — ООП и типизация

*(Заполняется агентом python-step-2-oop)*

---

## Шаг 3 — Экосистема и инструменты

*(Заполняется агентом python-step-3-ecosystem)*

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
