"""
Доменные модели: Order, OrderItem, Money, OrderStatus
======================================================
Аналогии C# → Python:
  @dataclass            = record (C# 9+) / class с auto-properties
  @dataclass(frozen=True) = readonly record struct
  __post_init__         = конструктор с валидацией
  __add__, __mul__      = operator overloading (operator +, operator *)
  Enum с auto()         = enum с автоматическими значениями
  @property             = get-only property
  functools.reduce      = LINQ .Aggregate()
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from functools import reduce


class OrderStatus(Enum):
    """
    C# аналог:
        public enum OrderStatus { Pending, Confirmed, Cancelled, Shipped }

    auto() автоматически назначает целочисленные значения (1, 2, 3...).
    """
    PENDING = auto()
    CONFIRMED = auto()
    CANCELLED = auto()
    SHIPPED = auto()


@dataclass
class Money:
    """
    Объект-значение для денег.

    C# аналог (readonly record struct):
        public readonly record struct Money(decimal Amount, string Currency) {
            public static Money operator +(Money a, Money b) { ... }
            public static Money operator *(Money m, int qty) { ... }
        }

    frozen=False т.к. Python dataclass с frozen=True не поддерживает
    изменение полей в __post_init__ напрямую.
    """
    amount: float
    currency: str = "USD"

    def __post_init__(self) -> None:
        """Валидация при создании — аналог конструктора с guard clauses."""
        if self.amount < 0:
            raise ValueError(f"Amount cannot be negative: {self.amount}")
        if not self.currency:
            raise ValueError("Currency cannot be empty")
        self.currency = self.currency.upper()

    def __add__(self, other: "Money") -> "Money":
        """C#: public static Money operator +(Money a, Money b)"""
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add {self.currency} and {other.currency}"
            )
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, quantity: int) -> "Money":
        """C#: public static Money operator *(Money m, int qty)"""
        if quantity < 0:
            raise ValueError(f"Quantity cannot be negative: {quantity}")
        return Money(self.amount * quantity, self.currency)

    def __str__(self) -> str:
        """C#: public override string ToString()"""
        return f"{self.amount:,.2f} {self.currency}"

    def __repr__(self) -> str:
        return f"Money(amount={self.amount}, currency={self.currency!r})"


@dataclass
class OrderItem:
    """
    Элемент заказа.

    C# аналог:
        public record OrderItem(string Name, Money UnitPrice, int Quantity) {
            public Money Total => UnitPrice * Quantity;
        }
    """
    name: str
    unit_price: Money
    quantity: int

    def __post_init__(self) -> None:
        """Валидация бизнес-правил."""
        if not self.name or not self.name.strip():
            raise ValueError("Item name cannot be empty")
        if self.quantity <= 0:
            raise ValueError(f"Quantity must be positive: {self.quantity}")

    @property
    def total(self) -> Money:
        """
        C# аналог:
            public Money Total => UnitPrice * Quantity;
        """
        return self.unit_price * self.quantity

    def __str__(self) -> str:
        return f"{self.name} x{self.quantity} = {self.total}"


@dataclass
class Order:
    """
    Агрегат заказа.

    C# аналог:
        public class Order {
            public Guid Id { get; }
            public List<OrderItem> Items { get; } = new();
            public OrderStatus Status { get; private set; }
            public Money Total => Items.Aggregate(Money.Zero, (acc, i) => acc + i.Total);
        }
    """
    id: str
    customer_name: str
    status: OrderStatus = field(default=OrderStatus.PENDING)
    items: list[OrderItem] = field(default_factory=list)

    def add_item(self, item: OrderItem) -> None:
        """
        Добавляет позицию в заказ.

        C# аналог:
            public void AddItem(OrderItem item) {
                if (Status != OrderStatus.Pending)
                    throw new InvalidOperationException("...");
                Items.Add(item);
            }
        """
        if self.status != OrderStatus.PENDING:
            raise ValueError(
                f"Cannot add items to order with status {self.status.name}"
            )
        self.items.append(item)

    def confirm(self) -> None:
        """
        C# аналог:
            public void Confirm() {
                if (Status != OrderStatus.Pending) throw ...;
                if (!Items.Any()) throw ...;
                Status = OrderStatus.Confirmed;
            }
        """
        if self.status != OrderStatus.PENDING:
            raise ValueError(
                f"Cannot confirm order with status {self.status.name}"
            )
        if not self.items:
            raise ValueError("Cannot confirm empty order")
        self.status = OrderStatus.CONFIRMED

    def cancel(self) -> None:
        """
        C# аналог:
            public void Cancel() {
                if (Status == OrderStatus.Shipped) throw ...;
                Status = OrderStatus.Cancelled;
            }
        """
        if self.status == OrderStatus.SHIPPED:
            raise ValueError("Cannot cancel a shipped order")
        self.status = OrderStatus.CANCELLED

    @property
    def total(self) -> Money:
        """
        Сумма заказа через reduce (аналог LINQ .Aggregate()).

        C# аналог:
            public Money Total => Items
                .Select(i => i.Total)
                .Aggregate(new Money(0), (acc, t) => acc + t);
        """
        if not self.items:
            return Money(0.0, "USD")
        return reduce(lambda acc, item: acc + item.total, self.items)

    def __str__(self) -> str:
        return (
            f"Order #{self.id} [{self.status.name}] "
            f"for {self.customer_name}: {self.total}"
        )
