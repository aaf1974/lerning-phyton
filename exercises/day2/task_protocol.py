"""
Python Protocol — структурная типизация (duck typing)
=====================================================
Аналогии C# → Python:
  interface IOrderRepository   = Protocol (+ @runtime_checkable)
  implements IOrderRepository  = НЕТ — duck typing автоматически
  abstract class               = ABC (другой подход, требует явного наследования)
  IEnumerable<T>               = Protocol с __iter__, __next__

КЛЮЧЕВОЕ ОТЛИЧИЕ от C#:
  В C# нужно явно написать ": IOrderRepository"
  В Python достаточно чтобы класс имел нужные методы — isinstance() сработает!
"""

from typing import Protocol, runtime_checkable
from uuid import uuid4

from src.orders.domain.models import Order


# --- Protocol = C# interface ---

@runtime_checkable  # Позволяет isinstance(obj, IOrderRepository)
class IOrderRepository(Protocol):
    """
    C# аналог:
        public interface IOrderRepository {
            Task<Order?> GetByIdAsync(string id);
            Task AddAsync(Order order);
            Task UpdateAsync(Order order);
            Task<IEnumerable<Order>> GetAllAsync();
        }

    @runtime_checkable — позволяет проверять в runtime через isinstance().
    Без него Protocol работает только для статической типизации (mypy/pyright).
    """

    async def get_by_id(self, order_id: str) -> Order | None:
        """Найти заказ по ID. C#: Task<Order?> GetByIdAsync(string id)"""
        ...

    async def add(self, order: Order) -> None:
        """Добавить заказ. C#: Task AddAsync(Order order)"""
        ...

    async def update(self, order: Order) -> None:
        """Обновить заказ. C#: Task UpdateAsync(Order order)"""
        ...

    async def get_all(self) -> list[Order]:
        """Все заказы. C#: Task<IEnumerable<Order>> GetAllAsync()"""
        ...


# --- Реализация БЕЗ явного наследования (duck typing) ---

class InMemoryOrderRepository:
    """
    Реализует IOrderRepository через duck typing.

    C# ПОТРЕБОВАЛ БЫ:
        public class InMemoryOrderRepository : IOrderRepository { ... }

    Python: НЕТ НИ ОДНОГО СЛОВА "implements" или "IOrderRepository" в классе!
    Достаточно просто иметь методы с правильными сигнатурами.
    """

    def __init__(self) -> None:
        self._store: dict[str, Order] = {}

    async def get_by_id(self, order_id: str) -> Order | None:
        return self._store.get(order_id)

    async def add(self, order: Order) -> None:
        self._store[order.id] = order

    async def update(self, order: Order) -> None:
        if order.id not in self._store:
            raise ValueError(f"Order {order.id} not found")
        self._store[order.id] = order

    async def get_all(self) -> list[Order]:
        return list(self._store.values())


# --- Класс который НЕ реализует протокол ---

class FakeRepository:
    """Этот класс НЕ соответствует IOrderRepository — нет метода get_by_id."""

    async def find(self, order_id: str) -> Order | None:  # неправильное имя
        return None

    async def save(self, order: Order) -> None:  # неправильное имя
        pass


# --- Демонстрация duck typing ---

def use_repository(repo: IOrderRepository) -> str:
    """
    Функция принимает любой объект, совместимый с IOrderRepository.

    C# аналог:
        void UseRepository(IOrderRepository repo) { ... }

    В Python: достаточно duck typing — явный интерфейс не нужен.
    """
    return f"Got repo of type: {type(repo).__name__}"


# --- Assert-тесты ---

repo = InMemoryOrderRepository()
fake = FakeRepository()

# МАГИЯ: isinstance работает БЕЗ явного наследования!
assert isinstance(repo, IOrderRepository), (
    "InMemoryOrderRepository должен соответствовать IOrderRepository"
)
assert not isinstance(fake, IOrderRepository), (
    "FakeRepository НЕ должен соответствовать IOrderRepository"
)

# Функция принимает repo без проблем
result = use_repository(repo)  # type: ignore[arg-type]
assert "InMemoryOrderRepository" in result

print("=== Демонстрация Protocol ===")
print(f"isinstance(InMemoryOrderRepository(), IOrderRepository) = {isinstance(repo, IOrderRepository)}")
print(f"isinstance(FakeRepository(), IOrderRepository)          = {isinstance(fake, IOrderRepository)}")
print()
print("InMemoryOrderRepository НЕ наследует IOrderRepository явно,")
print("но isinstance() = True т.к. все методы совпадают (duck typing)!")
print()

# --- ABC для сравнения ---
from abc import ABC, abstractmethod

class AbstractOrderRepository(ABC):
    """
    Альтернатива: явное наследование (как в C#).

    Используй ABC когда:
    - Хочешь общую логику в базовом классе
    - Нужен @abstractmethod для защиты от забытых методов

    Используй Protocol когда:
    - Работаешь с чужими классами (нельзя менять иерархию)
    - Хочешь duck typing совместимость
    - Пишешь библиотеку
    """

    @abstractmethod
    async def get_by_id(self, order_id: str) -> Order | None: ...

    @abstractmethod
    async def add(self, order: Order) -> None: ...

    @abstractmethod
    async def update(self, order: Order) -> None: ...

    @abstractmethod
    async def get_all(self) -> list[Order]: ...


print("=== Protocol vs ABC ===")
print()
print("| Критерий          | Protocol (duck typing) | ABC (explicit) |")
print("|-------------------|------------------------|----------------|")
print("| C# аналог         | interface (implicit)   | interface      |")
print("| Наследование      | НЕ нужно               | Обязательно    |")
print("| isinstance()      | Да (@runtime_checkable)| Да             |")
print("| Общая логика      | Нет                    | Да             |")
print("| Чужие классы      | Работает               | Не работает    |")
print("| Рекомендация      | Предпочтительнее       | При наследовании|")

if __name__ == "__main__":
    print("\nВсе assert прошли!")
