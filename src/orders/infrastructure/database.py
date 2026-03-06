"""
Настройка базы данных — AsyncEngine + AsyncSession
===================================================
Аналогии C# (EF Core) → Python (SQLAlchemy 2.0 async):
  DbContext                   = AsyncSession
  DbContextOptions            = create_async_engine(url, ...)
  DbContextFactory            = async_sessionmaker
  services.AddDbContext<T>()  = get_session() как FastAPI Depends
  context.SaveChangesAsync()  = await session.commit()
  using var ctx = new Ctx()   = async with AsyncSession() as session:
  context.Database.EnsureCreated() = await conn.run_sync(Base.metadata.create_all)
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.orders.config import settings
from src.orders.infrastructure.orm_models import Base

# --- Engine (C#: DbContextOptions) ---
# pool_pre_ping=True — проверяет соединение перед использованием
# (C#: нет прямого аналога, обрабатывается connection resilience)
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,        # SQL логирование (C#: EnableSensitiveDataLogging)
    pool_pre_ping=True,
)

# --- Session Factory (C#: IDbContextFactory<AppDbContext>) ---
# expire_on_commit=False — объекты остаются доступны после commit
# В C# это поведение по умолчанию (tracked entities остаются)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,     # C#: по умолчанию entities не expire после SaveChanges
    autoflush=True,
)


async def create_tables() -> None:
    """
    Создаёт все таблицы (для тестов и разработки).

    C# аналог:
        await context.Database.EnsureCreatedAsync();
        // или:
        await context.Database.MigrateAsync();

    В продакшне используй Alembic миграции!
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    """
    Удаляет все таблицы (только для тестов!).

    C# аналог:
        await context.Database.EnsureDeletedAsync();
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Dependency для получения сессии БД.

    C# аналог:
        services.AddScoped<AppDbContext>();
        // Затем в контроллере:
        public MyController(AppDbContext ctx) { _ctx = ctx; }

    yield — это ключевое слово для FastAPI Depends с cleanup:
    Всё ДО yield — setup (открыть сессию)
    yield session — внедрить в endpoint
    Всё ПОСЛЕ yield — cleanup (commit или rollback, закрыть)

    Использование:
        @router.get("/orders")
        async def get_orders(session: AsyncSession = Depends(get_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()      # C#: await ctx.SaveChangesAsync()
        except Exception:
            await session.rollback()    # C#: автоматически при using
            raise
