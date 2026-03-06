"""
InMemoryOrderRepository — in-memory реализация репозитория
==========================================================
C# аналог: Dictionary<string, Order> в памяти
Используется для разработки и тестирования.
"""

from src.orders.domain.models import Order


class InMemoryOrderRepository:
    """
    Репозиторий заказов в памяти.

    C# аналог:
        public class InMemoryOrderRepository : IOrderRepository {
            private readonly Dictionary<string, Order> _store = new();
            ...
        }
    """

    def __init__(self) -> None:
        self._store: dict[str, Order] = {}

    async def get_by_id(self, order_id: str) -> Order | None:
        """C#: Task<Order?> GetByIdAsync(string id)"""
        return self._store.get(order_id)

    async def add(self, order: Order) -> None:
        """C#: Task AddAsync(Order order)"""
        self._store[order.id] = order

    async def update(self, order: Order) -> None:
        """C#: Task UpdateAsync(Order order)"""
        if order.id not in self._store:
            raise ValueError(f"Order {order.id} not found")
        self._store[order.id] = order

    async def get_all(self) -> list[Order]:
        """C#: Task<IEnumerable<Order>> GetAllAsync()"""
        return list(self._store.values())
