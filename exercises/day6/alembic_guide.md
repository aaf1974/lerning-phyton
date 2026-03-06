# Alembic — миграции БД: EF Core → Alembic

> Полный аналог `dotnet ef` для Python/SQLAlchemy

---

## Инициализация (один раз)

| EF Core | Alembic | Описание |
|---------|---------|----------|
| Встроен в пакет | `uv add alembic` | Установка |
| Автоматически | `alembic init alembic` | Создать папку миграций |
| Настройка в `appsettings.json` | Настройка в `alembic.ini` и `env.py` | Конфигурация |

```bash
# Шаг 1: инициализация
uv run alembic init alembic

# Шаг 2: в alembic/env.py добавить:
# from src.orders.infrastructure.orm_models import Base
# target_metadata = Base.metadata
```

**alembic.ini:**
```ini
sqlalchemy.url = postgresql+asyncpg://user:pass@localhost/orders_db
```

---

## Основные команды

| EF Core | Alembic | Описание |
|---------|---------|----------|
| `dotnet ef migrations add <Name>` | `alembic revision --autogenerate -m "<name>"` | Создать миграцию |
| `dotnet ef database update` | `alembic upgrade head` | Применить все миграции |
| `dotnet ef database update <Migration>` | `alembic upgrade <revision>` | До конкретной версии |
| `dotnet ef migrations remove` | `alembic downgrade -1` | Откатить последнюю |
| `dotnet ef database update 0` | `alembic downgrade base` | Откатить все |
| `dotnet ef migrations list` | `alembic history` | История миграций |
| `dotnet ef migrations script` | `alembic upgrade head --sql` | SQL скрипт |
| нет аналога | `alembic current` | Текущая версия БД |

```bash
# Создать первую миграцию (автогенерация по моделям)
uv run alembic revision --autogenerate -m "create orders tables"

# Применить все миграции
uv run alembic upgrade head

# Посмотреть историю
uv run alembic history --verbose

# Откатить одну миграцию
uv run alembic downgrade -1

# Откатить всё
uv run alembic downgrade base

# Текущий статус
uv run alembic current
```

---

## Структура файлов

```
alembic/
├── env.py              ← конфигурация (аналог DbContext в ef migrations)
├── script.py.mako      ← шаблон миграции
└── versions/
    ├── 001_create_orders_table.py
    ├── 002_add_status_index.py
    └── 003_add_updated_at.py
alembic.ini             ← настройки (URL БД)
```

---

## Пример миграции

EF Core генерирует C# класс:
```csharp
public partial class CreateOrdersTable : Migration {
    protected override void Up(MigrationBuilder migrationBuilder) {
        migrationBuilder.CreateTable(name: "Orders", columns: ...);
    }
    protected override void Down(MigrationBuilder migrationBuilder) {
        migrationBuilder.DropTable(name: "Orders");
    }
}
```

Alembic генерирует Python файл:
```python
def upgrade() -> None:
    op.create_table('orders',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('customer_name', sa.String(200), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )

def downgrade() -> None:
    op.drop_table('orders')
```

---

## Async поддержка

Для async SQLAlchemy нужен специальный `env.py`:

```python
# alembic/env.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

def run_migrations_online() -> None:
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

    async def run_async_migrations() -> None:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run_async_migrations())
```

---

## Типичный рабочий процесс

```bash
# 1. Изменить ORM модели (orm_models.py)
# 2. Создать миграцию
uv run alembic revision --autogenerate -m "add shipping_address to orders"

# 3. Проверить сгенерированный файл в alembic/versions/
# 4. Применить
uv run alembic upgrade head

# 5. В CI/CD:
uv run alembic upgrade head  # перед запуском приложения
```

---

## Отличия от EF Core

| EF Core | Alembic |
|---------|---------|
| Автодетект изменений в `*.cs` | Сравнивает схему БД с `Base.metadata` |
| Snapshot в `*ModelSnapshot.cs` | Текущая схема хранится в БД |
| Rollback в транзакции | Явный `downgrade()` метод |
| Встроен в EF | Отдельный инструмент |
| `[Index]` атрибут | `__table_args__ = (Index(...),)` |
