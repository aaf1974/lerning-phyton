"""
Shared pytest fixtures
======================
Аналогии C# (xUnit) → Python (pytest):
  IClassFixture<T>           = fixture со scope="class"
  ICollectionFixture<T>      = fixture со scope="session"
  Constructor DI в тестах    = параметры функции теста (pytest DI)
  Arrange/Act/Assert         = тот же паттерн
  [Fact] / [Theory]          = def test_*() / @pytest.mark.parametrize

Fixture scope:
  "function" (default) = создаётся для каждого теста (C#: нет фикстуры = new каждый раз)
  "class"              = одна на класс тестов
  "module"             = одна на файл
  "session"            = одна на весь тестовый прогон (C#: ICollectionFixture)
"""

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.orders.api.main import app
from src.orders.infrastructure.orm_models import Base

# SQLite in-memory для тестов (C#: UseInMemoryDatabase)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """
    Создаёт тестовый движок БД (один раз на всю сессию).

    C# аналог:
        public class DatabaseFixture : IAsyncLifetime {
            public AppDbContext Context { get; private set; }
            public async Task InitializeAsync() {
                Context = new AppDbContext(new DbContextOptionsBuilder()
                    .UseInMemoryDatabase("TestDb").Options);
            }
        }
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine):
    """
    Создаёт сессию БД с откатом после каждого теста.

    C# аналог:
        // Паттерн rollback в xUnit:
        using var tx = await context.Database.BeginTransactionAsync();
        // ... тест ...
        await tx.RollbackAsync();  // откат — БД чиста для следующего теста
    """
    session_factory = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session_factory() as session:
        yield session
        await session.rollback()  # откат после каждого теста


@pytest_asyncio.fixture(scope="function")
async def client():
    """
    AsyncClient для интеграционных тестов.

    C# аналог:
        var factory = new WebApplicationFactory<Program>();
        var client = factory.CreateClient();
        // или:
        var client = new HttpClient { BaseAddress = new Uri("http://localhost") };

    ASGITransport — аналог TestServer в ASP.NET Core:
    запросы идут напрямую в ASGI app без HTTP стека.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
