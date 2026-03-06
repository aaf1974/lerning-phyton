"""
OrderService — сервисный слой (Application Layer)
==================================================
Аналогии C# → Python:
  Dependency Injection через конструктор   = конструктор + FastAPI Depends
  IOrderRepository в конструкторе          = тот же паттерн
  MediatR ICommandHandler                  = метод сервиса
"""

import uuid

from src.orders.domain.models import Money, Order, OrderItem, OrderStatus
from src.orders.infrastructure.repositories import InMemoryOrderRepository


class OrderService:
    """
    Сервис управления заказами.

    C# аналог:
        public class OrderService(IOrderRepository repository) {
            public async Task<Order> CreateOrderAsync(CreateOrderRequest req) { ... }
            public async Task<Order?> GetOrderAsync(string id) { ... }
            public async Task ConfirmOrderAsync(string id) { ... }
        }
    """

    def __init__(self, repository: InMemoryOrderRepository) -> None:
        self._repo = repository

    async def create_order(
        self,
        customer_name: str,
        items: list[dict[str, object]],
    ) -> Order:
        """
        Создать новый заказ.

        C# аналог:
            public async Task<Order> CreateOrderAsync(CreateOrderCommand cmd) {
                var order = new Order(Guid.NewGuid().ToString(), cmd.CustomerName);
                foreach (var item in cmd.Items)
                    order.AddItem(new OrderItem(item.Name, item.UnitPrice, item.Quantity));
                await _repository.AddAsync(order);
                return order;
            }
        """
        order_id = str(uuid.uuid4())
        order = Order(id=order_id, customer_name=customer_name)

        for item_data in items:
            name = str(item_data["name"])
            amount = float(item_data["unit_price"])  # type: ignore[arg-type]
            quantity = int(item_data["quantity"])  # type: ignore[arg-type]
            currency = str(item_data.get("currency", "USD"))

            order.add_item(OrderItem(
                name=name,
                unit_price=Money(amount=amount, currency=currency),
                quantity=quantity,
            ))

        await self._repo.add(order)
        return order

    async def get_order(self, order_id: str) -> Order | None:
        """C#: Task<Order?> GetOrderAsync(string id)"""
        return await self._repo.get_by_id(order_id)

    async def confirm_order(self, order_id: str) -> Order:
        """
        Подтвердить заказ.

        C# аналог:
            public async Task<Order> ConfirmOrderAsync(string id) {
                var order = await _repository.GetByIdAsync(id)
                    ?? throw new NotFoundException(id);
                order.Confirm();
                await _repository.UpdateAsync(order);
                return order;
            }
        """
        order = await self._repo.get_by_id(order_id)
        if order is None:
            raise ValueError(f"Order {order_id} not found")
        order.confirm()
        await self._repo.update(order)
        return order

    async def get_all_orders(self) -> list[Order]:
        """C#: Task<IEnumerable<Order>> GetAllOrdersAsync()"""
        return await self._repo.get_all()
