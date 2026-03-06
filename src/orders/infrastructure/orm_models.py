"""
SQLAlchemy ORM модели
=====================
Аналогии C# (EF Core) → Python (SQLAlchemy 2.0):
  DbContext                     = DeclarativeBase + AsyncSession
  IEntityTypeConfiguration<T>   = настройки колонок через mapped_column()
  .Include(o => o.Items)        = relationship + lazy="selectin"
  [Required], [MaxLength]       = nullable=False, String(200)
  Owned type / Value Object     = встроенный тип или отдельная таблица
  migration (EF: dotnet ef)     = alembic revision --autogenerate
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """
    Базовый класс для всех ORM моделей.

    C# аналог:
        public class AppDbContext : DbContext {
            public DbSet<Order> Orders { get; set; }
            public DbSet<OrderItem> OrderItems { get; set; }
        }
    """
    pass


class OrderItemModel(Base):
    """
    ORM модель позиции заказа.

    C# аналог (EF Core):
        public class OrderItem {
            public int Id { get; set; }
            public string Name { get; set; } = "";
            [Column(TypeName = "decimal(18,2)")]
            public decimal UnitPrice { get; set; }
            public string Currency { get; set; } = "USD";
            public int Quantity { get; set; }
            public string OrderId { get; set; } = "";
            public Order Order { get; set; } = null!;
        }
    """
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Обратная связь к Order
    order: Mapped["OrderModel"] = relationship(back_populates="items")


class OrderModel(Base):
    """
    ORM модель заказа.

    C# аналог (EF Core):
        public class Order {
            public string Id { get; set; } = "";
            public string CustomerName { get; set; } = "";
            public string Status { get; set; } = "PENDING";
            public DateTime CreatedAt { get; set; }
            public List<OrderItem> Items { get; set; } = new();
        }

        // В DbContext:
        modelBuilder.Entity<Order>()
            .HasMany(o => o.Items)
            .WithOne(i => i.Order)
            .HasForeignKey(i => i.OrderId);
    """
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING",
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Связь один-ко-многим
    # lazy="selectin" = .Include(o => o.Items) в EF Core
    # SELECT IN загружает связанные записи одним запросом
    items: Mapped[list[OrderItemModel]] = relationship(
        "OrderItemModel",
        back_populates="order",
        lazy="selectin",        # C#: .Include(o => o.Items) автоматически
        cascade="all, delete-orphan",
    )
