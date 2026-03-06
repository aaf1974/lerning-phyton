# Python Learning — Промт запуска

Скопируй этот текст и вставь в Claude Code в каталоге `F:\Lerning\lerning-phyton`:

---

```
Запусти полный план обучения Python для .NET разработчика.

Рабочий каталог: F:\Lerning\lerning-phyton
Git репозиторий инициализирован.

Используй агента python-learning-orchestrator — он последовательно выполнит
все 8 шагов (0-7), делегируя каждый шаг специализированному агенту.

Требования:
- Каждый шаг должен заканчиваться git commit с номером шага
- Не переходить к следующему шагу пока текущий не закоммичен
- Все файлы создавать в F:\Lerning\lerning-phyton\
- REPORT.md обновлять после каждого шага
```

---

## Агенты которые будут задействованы

| Агент | Шаг | Коммит |
|-------|-----|--------|
| `python-step-0-init` | Инициализация проекта | `Step 0: Initialize...` |
| `python-step-1-syntax` | Python синтаксис | `Step 1: Python syntax...` |
| `python-step-2-oop` | ООП и типизация | `Step 2: OOP...` |
| `python-step-3-ecosystem` | Экосистема | `Step 3: Ecosystem...` |
| `python-step-4-async` | Async/await | `Step 4: Async/await...` |
| `python-step-5-fastapi` | FastAPI | `Step 5: FastAPI...` |
| `python-step-6-sqlalchemy` | SQLAlchemy + Alembic | `Step 6: SQLAlchemy...` |
| `python-step-7-testing` | Тестирование | `Step 7: pytest...` |

## Где находятся агенты

`F:\Lerning\.claude\agents\` — копировать в проект НЕ НУЖНО.
Claude Code автоматически обнаруживает агентов из родительских каталогов.

## Запуск отдельного шага

Если нужно выполнить только один шаг:
```
Выполни шаг 3 используя агента python-step-3-ecosystem.
Рабочий каталог: F:\Lerning\lerning-phyton
```
