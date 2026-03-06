"""
Юнит-тесты OrderService с AsyncMock
=====================================
Аналогии C# (Moq) → Python (unittest.mock):
  new Mock<IOrderRepository>()      = AsyncMock()
  mock.Setup(r => r.GetByIdAsync(id)).ReturnsAsync(order)
                                    = mock_repo.get_by_id.return_value = order
  mock.Verify(r => r.AddAsync(It.IsAny<Order>()), Times.Once())
                                    = mock_repo.add.assert_called_once()
  It.IsAny<T>()                     = unittest.mock.ANY
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, call

from src.orders.application.services import OrderService
from src.orders.domain.models import Money, Order, OrderItem, OrderStatus


@pytest.fixture
def mock_repo() -> AsyncMock:
    """
    Мок репозитория.

    C# аналог (Moq):
        var mockRepo = new Mock<IOrderRepository>();
        mockRepo.Setup(r => r.GetByIdAsync(It.IsAny<string>()))
                .ReturnsAsync((Order?)null);
    """
    repo = AsyncMock()
    repo.get_by_id = AsyncMock(return_value=None)
    repo.add = AsyncMock(return_value=None)
    repo.update = AsyncMock(return_value=None)
    repo.get_all = AsyncMock(return_value=[])
    return repo


@pytest.fixture
def service(mock_repo: AsyncMock) -> OrderService:
    """OrderService с мок-репозиторием."""
    return OrderService(repository=mock_repo)


def _make_order(order_id: str = "order-1", status: OrderStatus = OrderStatus.PENDING) -> Order:
    """Вспомогательная фабрика заказа для тестов."""
    order = Order(id=order_id, customer_name="Test User", status=status)
    order.items.append(OrderItem(
        name="Widget",
        unit_price=Money(10.0, "USD"),
        quantity=2,
    ))
    return order


class TestOrderServiceGet:

    async def test_get_order_returns_none_when_not_found(
        self, service: OrderService, mock_repo: AsyncMock
    ) -> None:
        """
        C# аналог (Moq):
            mockRepo.Setup(r => r.GetByIdAsync("unknown")).ReturnsAsync((Order?)null);
            var result = await service.GetOrderAsync("unknown");
            Assert.Null(result);
        """
        mock_repo.get_by_id.return_value = None

        result = await service.get_order("unknown-id")

        assert result is None
        mock_repo.get_by_id.assert_called_once_with("unknown-id")

    async def test_get_order_returns_order_when_found(
        self, service: OrderService, mock_repo: AsyncMock
    ) -> None:
        order = _make_order("order-42")
        mock_repo.get_by_id.return_value = order

        result = await service.get_order("order-42")

        assert result is order
        assert result is not None
        assert result.id == "order-42"

    async def test_get_all_orders_returns_empty_list(
        self, service: OrderService, mock_repo: AsyncMock
    ) -> None:
        mock_repo.get_all.return_value = []

        result = await service.get_all_orders()

        assert result == []
        mock_repo.get_all.assert_called_once()


class TestOrderServiceCreate:

    async def test_create_order_calls_repo_add(
        self, service: OrderService, mock_repo: AsyncMock
    ) -> None:
        """
        C# аналог (Moq):
            await service.CreateOrderAsync(cmd);
            mockRepo.Verify(r => r.AddAsync(It.IsAny<Order>()), Times.Once());
        """
        items = [{"name": "Widget", "unit_price": 10.0, "quantity": 2}]

        order = await service.create_order("Alice", items)

        # Проверяем что add был вызван ровно один раз
        mock_repo.add.assert_called_once()

        # Проверяем что передали Order объект
        added_order: Order = mock_repo.add.call_args[0][0]
        assert added_order.customer_name == "Alice"
        assert len(added_order.items) == 1
        assert added_order.items[0].name == "Widget"

    async def test_create_order_generates_unique_id(
        self, service: OrderService, mock_repo: AsyncMock
    ) -> None:
        items = [{"name": "Item", "unit_price": 5.0, "quantity": 1}]

        order1 = await service.create_order("Alice", items)
        order2 = await service.create_order("Bob", items)

        assert order1.id != order2.id

    async def test_create_order_returns_pending_status(
        self, service: OrderService, mock_repo: AsyncMock
    ) -> None:
        items = [{"name": "Item", "unit_price": 5.0, "quantity": 1}]
        order = await service.create_order("Alice", items)
        assert order.status == OrderStatus.PENDING


class TestOrderServiceConfirm:

    async def test_confirm_raises_when_not_found(
        self, service: OrderService, mock_repo: AsyncMock
    ) -> None:
        """
        C# аналог:
            mockRepo.Setup(r => r.GetByIdAsync("x")).ReturnsAsync((Order?)null);
            await Assert.ThrowsAsync<NotFoundException>(() => service.ConfirmOrderAsync("x"));
        """
        mock_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            await service.confirm_order("nonexistent")

        # update НЕ должен был вызваться
        mock_repo.update.assert_not_called()

    async def test_confirm_calls_update_on_success(
        self, service: OrderService, mock_repo: AsyncMock
    ) -> None:
        order = _make_order("order-1", status=OrderStatus.PENDING)
        mock_repo.get_by_id.return_value = order

        result = await service.confirm_order("order-1")

        assert result.status == OrderStatus.CONFIRMED
        mock_repo.update.assert_called_once_with(order)

    async def test_confirm_raises_for_already_confirmed(
        self, service: OrderService, mock_repo: AsyncMock
    ) -> None:
        order = _make_order("order-1", status=OrderStatus.CONFIRMED)
        mock_repo.get_by_id.return_value = order

        with pytest.raises(ValueError):
            await service.confirm_order("order-1")
