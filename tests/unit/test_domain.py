"""
Юнит-тесты доменных моделей
============================
Аналогии C# (xUnit) → Python (pytest):
  [Fact]                    = def test_name():
  [Theory] + [InlineData]   = @pytest.mark.parametrize
  Assert.Equal(exp, act)    = assert act == exp
  Assert.Throws<T>(lambda)  = pytest.raises(T)
  new TestClass()           = fixture или прямое создание
"""

import pytest

from src.orders.domain.models import Money, Order, OrderItem, OrderStatus


class TestMoney:
    """
    C# аналог:
        public class MoneyTests {
            [Fact] public void Constructor_NegativeAmount_ThrowsException() { ... }
        }
    """

    def test_create_money_valid(self) -> None:
        money = Money(100.0, "USD")
        assert money.amount == 100.0
        assert money.currency == "USD"

    def test_currency_normalized_to_uppercase(self) -> None:
        money = Money(50.0, "usd")
        assert money.currency == "USD"

    def test_negative_amount_raises(self) -> None:
        """C#: Assert.Throws<ArgumentException>(() => new Money(-1, "USD"))"""
        with pytest.raises(ValueError, match="negative"):
            Money(-1.0, "USD")

    def test_empty_currency_raises(self) -> None:
        with pytest.raises(ValueError, match="Currency"):
            Money(100.0, "")

    def test_add_same_currency(self) -> None:
        """C#: Assert.Equal(new Money(150), new Money(100) + new Money(50))"""
        a = Money(100.0, "USD")
        b = Money(50.0, "USD")
        result = a + b
        assert result.amount == 150.0
        assert result.currency == "USD"

    def test_add_different_currency_raises(self) -> None:
        usd = Money(100.0, "USD")
        eur = Money(50.0, "EUR")
        with pytest.raises(ValueError, match="Cannot add"):
            _ = usd + eur

    @pytest.mark.parametrize("quantity,expected", [
        (1, 100.0),
        (3, 300.0),
        (0, 0.0),
        (10, 1000.0),
    ])
    def test_multiply_by_quantity(self, quantity: int, expected: float) -> None:
        """
        C# аналог:
            [Theory]
            [InlineData(1, 100.0)]
            [InlineData(3, 300.0)]
            public void Multiply_ReturnsCorrect(int qty, decimal expected) { ... }
        """
        money = Money(100.0, "USD")
        result = money * quantity
        assert result.amount == pytest.approx(expected)
        assert result.currency == "USD"

    def test_multiply_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="negative"):
            _ = Money(100.0, "USD") * (-1)

    def test_str_representation(self) -> None:
        money = Money(1234567.89, "USD")
        assert str(money) == "1,234,567.89 USD"


class TestOrderItem:
    """Тесты позиции заказа."""

    def test_create_valid_item(self) -> None:
        item = OrderItem(
            name="Widget",
            unit_price=Money(10.0, "USD"),
            quantity=3,
        )
        assert item.name == "Widget"
        assert item.quantity == 3

    def test_total_calculated_correctly(self) -> None:
        """C#: Assert.Equal(new Money(30), item.Total)"""
        item = OrderItem(
            name="Widget",
            unit_price=Money(10.0, "USD"),
            quantity=3,
        )
        assert item.total.amount == pytest.approx(30.0)
        assert item.total.currency == "USD"

    def test_empty_name_raises(self) -> None:
        with pytest.raises(ValueError, match="name"):
            OrderItem(name="", unit_price=Money(10.0), quantity=1)

    def test_whitespace_name_raises(self) -> None:
        with pytest.raises(ValueError, match="name"):
            OrderItem(name="   ", unit_price=Money(10.0), quantity=1)

    def test_zero_quantity_raises(self) -> None:
        with pytest.raises(ValueError, match="Quantity"):
            OrderItem(name="Item", unit_price=Money(10.0), quantity=0)

    def test_negative_quantity_raises(self) -> None:
        with pytest.raises(ValueError, match="Quantity"):
            OrderItem(name="Item", unit_price=Money(10.0), quantity=-1)


class TestOrder:
    """Тесты агрегата заказа."""

    def _make_item(self, name: str = "Widget", price: float = 10.0, qty: int = 1) -> OrderItem:
        return OrderItem(name=name, unit_price=Money(price, "USD"), quantity=qty)

    def test_new_order_is_pending(self) -> None:
        order = Order(id="1", customer_name="Alice")
        assert order.status == OrderStatus.PENDING
        assert order.items == []

    def test_add_item_to_pending_order(self) -> None:
        order = Order(id="1", customer_name="Alice")
        order.add_item(self._make_item())
        assert len(order.items) == 1

    def test_total_of_empty_order_is_zero(self) -> None:
        order = Order(id="1", customer_name="Alice")
        assert order.total.amount == 0.0

    def test_total_sums_all_items(self) -> None:
        """C#: Assert.Equal(new Money(35), order.Total)"""
        order = Order(id="1", customer_name="Alice")
        order.add_item(self._make_item("A", price=10.0, qty=2))  # 20
        order.add_item(self._make_item("B", price=15.0, qty=1))  # 15
        assert order.total.amount == pytest.approx(35.0)

    def test_confirm_pending_order(self) -> None:
        order = Order(id="1", customer_name="Alice")
        order.add_item(self._make_item())
        order.confirm()
        assert order.status == OrderStatus.CONFIRMED

    def test_confirm_empty_order_raises(self) -> None:
        order = Order(id="1", customer_name="Alice")
        with pytest.raises(ValueError, match="empty"):
            order.confirm()

    def test_confirm_already_confirmed_raises(self) -> None:
        order = Order(id="1", customer_name="Alice")
        order.add_item(self._make_item())
        order.confirm()
        with pytest.raises(ValueError, match="CONFIRMED"):
            order.confirm()

    def test_cancel_pending_order(self) -> None:
        order = Order(id="1", customer_name="Alice")
        order.cancel()
        assert order.status == OrderStatus.CANCELLED

    def test_cancel_confirmed_order(self) -> None:
        order = Order(id="1", customer_name="Alice")
        order.add_item(self._make_item())
        order.confirm()
        order.cancel()
        assert order.status == OrderStatus.CANCELLED

    def test_cannot_add_item_to_confirmed_order(self) -> None:
        order = Order(id="1", customer_name="Alice")
        order.add_item(self._make_item())
        order.confirm()
        with pytest.raises(ValueError, match="CONFIRMED"):
            order.add_item(self._make_item("Extra"))

    def test_cannot_cancel_shipped_order(self) -> None:
        from src.orders.domain.models import OrderStatus
        order = Order(id="1", customer_name="Alice", status=OrderStatus.SHIPPED)
        with pytest.raises(ValueError, match="shipped"):
            order.cancel()
