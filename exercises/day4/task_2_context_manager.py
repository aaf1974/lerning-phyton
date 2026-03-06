"""
Async Context Manager = IAsyncDisposable / await using
=======================================================
Аналогии C# → Python:
  IAsyncDisposable            = async context manager протокол
  await using var db = ...    = async with DatabaseConnection() as db:
  DisposeAsync()              = __aexit__
  IDisposable + using         = контекстный менеджер (синхронный)
  @asynccontextmanager        = упрощённый способ через yield

Контекстный менеджер гарантирует:
  - Ресурс открыт ДО входа в блок
  - Ресурс закрыт ПОСЛЕ блока (даже при исключении)
  Это аналог try/finally или using в C#.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator


# --- Вариант 1: Класс с __aenter__ / __aexit__ ---

class DatabaseConnection:
    """
    Async context manager через специальные методы.

    C# аналог:
        public class DatabaseConnection : IAsyncDisposable {
            public async Task OpenAsync() { ... }
            public async ValueTask DisposeAsync() { ... }
        }

        // Использование:
        await using var db = new DatabaseConnection("connection_string");
        await db.QueryAsync("SELECT ...");

    Python использование:
        async with DatabaseConnection("url") as db:
            result = await db.execute("SELECT ...")
    """

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
        self._connected = False
        self._transaction_active = False

    async def __aenter__(self) -> "DatabaseConnection":
        """
        Вызывается при входе в `async with`.
        C# аналог: конструктор + OpenAsync()
        """
        print(f"  [DB] Открываем соединение: {self.connection_string}")
        await asyncio.sleep(0.01)  # имитация подключения
        self._connected = True
        return self  # возвращается как переменная в `as db`

    async def __aexit__(
        self,
        exc_type: type | None,
        exc_val: Exception | None,
        exc_tb: object,
    ) -> bool:
        """
        Вызывается при выходе из блока (в т.ч. при исключении).

        C# аналог: DisposeAsync() / finally блок
        exc_type != None — было исключение
        Вернуть True — подавить исключение (редко нужно)
        """
        if exc_type is not None:
            print(f"  [DB] Откат транзакции из-за: {exc_type.__name__}")
        else:
            print("  [DB] Фиксация транзакции")

        print(f"  [DB] Закрываем соединение")
        await asyncio.sleep(0.01)  # имитация закрытия
        self._connected = False
        return False  # не подавляем исключение

    async def execute(self, query: str) -> list[dict[str, str]]:
        """Выполнить SQL запрос."""
        if not self._connected:
            raise RuntimeError("Not connected")
        await asyncio.sleep(0.01)
        return [{"result": f"data from: {query}"}]


# --- Вариант 2: @asynccontextmanager декоратор ---

@asynccontextmanager
async def managed_connection(connection_string: str) -> AsyncGenerator[DatabaseConnection, None]:
    """
    Упрощённый async context manager через @asynccontextmanager + yield.

    C# аналог: нет прямого, ближайший — метод с yield return
    в IAsyncEnumerable, но семантика другая.

    Всё ДО yield — это __aenter__
    Всё ПОСЛЕ yield — это __aexit__
    yield возвращает значение для `as variable`

    Использование:
        async with managed_connection("url") as db:
            await db.execute("SELECT ...")
    """
    db = DatabaseConnection(connection_string)
    try:
        await db.__aenter__()
        yield db          # <- здесь выполняется тело `async with`
    except Exception as e:
        await db.__aexit__(type(e), e, None)
        raise
    else:
        await db.__aexit__(None, None, None)


# --- Вариант 3: Вложенные context managers ---

@asynccontextmanager
async def transaction(db: DatabaseConnection) -> AsyncGenerator[None, None]:
    """
    Вложенный context manager для транзакций.

    C# аналог:
        await using var tx = await connection.BeginTransactionAsync();
        try { ...; await tx.CommitAsync(); }
        catch { await tx.RollbackAsync(); throw; }
    """
    print("  [TX] BEGIN TRANSACTION")
    db._transaction_active = True
    try:
        yield
        print("  [TX] COMMIT")
    except Exception:
        print("  [TX] ROLLBACK")
        raise
    finally:
        db._transaction_active = False


async def main() -> None:
    print("=== Вариант 1: Класс __aenter__/__aexit__ ===")
    async with DatabaseConnection("postgresql://localhost/orders") as db:
        result = await db.execute("SELECT * FROM orders")
        print(f"  Запрос выполнен: {result[0]['result'][:30]}...")
    print(f"  После блока: connected={db._connected}\n")

    print("=== Вариант 2: @asynccontextmanager декоратор ===")
    async with managed_connection("sqlite:///test.db") as db2:
        result2 = await db2.execute("SELECT count(*) FROM users")
        print(f"  Запрос выполнен: {result2[0]['result'][:30]}...\n")

    print("=== Вариант 3: Вложенные context managers ===")
    async with DatabaseConnection("postgresql://localhost/orders") as db3:
        async with transaction(db3):
            await db3.execute("INSERT INTO orders VALUES (...)")
            await db3.execute("UPDATE inventory SET stock = stock - 1")
            print("  Операции выполнены\n")

    print("=== Вариант 4: Обработка исключения ===")
    try:
        async with DatabaseConnection("postgresql://localhost/orders") as db4:
            await db4.execute("SELECT 1")
            raise ValueError("Что-то пошло не так")
    except ValueError:
        print("  Исключение поймано снаружи\n")

    print("=== Итог: аналогии ===")
    print()
    print("| C#                          | Python                        |")
    print("|-----------------------------|-------------------------------|")
    print("| IAsyncDisposable            | async context manager         |")
    print("| DisposeAsync()              | __aexit__                     |")
    print("| await using var x = new X()| async with X() as x:          |")
    print("| try/finally                 | __aexit__ вызывается всегда   |")
    print("| нет прямого аналога         | @asynccontextmanager + yield  |")


if __name__ == "__main__":
    asyncio.run(main())
