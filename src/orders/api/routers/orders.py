"""
FastAPI роутер для Orders
==========================
Аналогии C# → Python:
  [ApiController]              = APIRouter
  [Route("api/orders")]        = prefix="/orders"
  [HttpPost]                   = @router.post("/")
  [HttpGet("{id}")]             = @router.get("/{order_id}")
  IActionResult                = автоматически из return
  [FromBody] Request req       = request: CreateOrderRequest (Pydantic)
  services.GetRequiredService  = Depends(get_service)
  BadRequest(detail)           = HTTPException(status_code=400)
  NotFound()                   = HTTPException(status_code=404)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from src.orders.application.services import OrderService
from src.orders.domain.models import OrderStatus
from src.orders.infrastructure.repositories import InMemoryOrderRepository

router = APIRouter(prefix="/orders", tags=["orders"])

# Синглтон репозитория (в реальном проекте — через DI контейнер)
_repository = InMemoryOrderRepository()


def get_service() -> OrderService:
    """
    Dependency provider для FastAPI.

    C# аналог:
        services.AddScoped<OrderService>();
        // FastAPI автоматически инжектирует через Depends(get_service)

    В реальном проекте здесь был бы async generator с async with session:
        async def get_service(session: AsyncSession = Depends(get_session)):
            yield OrderService(SqlAlchemyOrderRepository(session))
    """
    return OrderService(_repository)


# --- Pydantic модели запросов/ответов ---

class OrderItemRequest(BaseModel):
    """
    C# аналог:
        public record OrderItemRequest(
            string Name,
            decimal UnitPrice,
            int Quantity,
            string Currency = "USD"
        );
    """
    name: str = Field(min_length=1, max_length=200)
    unit_price: float = Field(gt=0, description="Цена за единицу (> 0)")
    quantity: int = Field(ge=1, description="Количество (>= 1)")
    currency: str = Field(default="USD", min_length=3, max_length=3)


class CreateOrderRequest(BaseModel):
    """C#: public record CreateOrderRequest(string CustomerName, List<OrderItemRequest> Items)"""
    customer_name: str = Field(min_length=1, max_length=200)
    items: list[OrderItemRequest] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    name: str
    unit_price: float
    quantity: int
    currency: str
    total: float


class OrderResponse(BaseModel):
    """
    C# аналог:
        public record OrderResponse(string Id, string CustomerName, string Status, decimal Total);
    """
    id: str
    customer_name: str
    status: str
    total: float
    currency: str
    items: list[OrderItemResponse]


def _map_order_response(order: object) -> OrderResponse:
    """Маппинг доменной модели в DTO ответа. C#: AutoMapper."""
    from src.orders.domain.models import Order
    assert isinstance(order, Order)
    total = order.total
    return OrderResponse(
        id=order.id,
        customer_name=order.customer_name,
        status=order.status.name,
        total=total.amount,
        currency=total.currency,
        items=[
            OrderItemResponse(
                name=item.name,
                unit_price=item.unit_price.amount,
                quantity=item.quantity,
                currency=item.unit_price.currency,
                total=item.total.amount,
            )
            for item in order.items
        ],
    )


# --- Endpoints ---

@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать заказ",
)
async def create_order(
    request: CreateOrderRequest,
    service: OrderService = Depends(get_service),
) -> OrderResponse:
    """
    C# аналог:
        [HttpPost]
        public async Task<ActionResult<OrderResponse>> CreateOrder(
            [FromBody] CreateOrderRequest request,
            [FromServices] OrderService service)
        {
            var order = await service.CreateOrderAsync(request);
            return CreatedAtAction(nameof(GetOrder), new { id = order.Id }, Map(order));
        }
    """
    items = [
        {
            "name": item.name,
            "unit_price": item.unit_price,
            "quantity": item.quantity,
            "currency": item.currency,
        }
        for item in request.items
    ]
    order = await service.create_order(request.customer_name, items)
    return _map_order_response(order)


@router.get(
    "/",
    response_model=list[OrderResponse],
    summary="Список заказов",
)
async def get_all_orders(
    service: OrderService = Depends(get_service),
) -> list[OrderResponse]:
    """C#: [HttpGet] public async Task<ActionResult<IEnumerable<OrderResponse>>> GetAll()"""
    orders = await service.get_all_orders()
    return [_map_order_response(o) for o in orders]


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Получить заказ по ID",
)
async def get_order(
    order_id: str,
    service: OrderService = Depends(get_service),
) -> OrderResponse:
    """
    C# аналог:
        [HttpGet("{id}")]
        public async Task<ActionResult<OrderResponse>> GetOrder(string id) {
            var order = await service.GetOrderAsync(id);
            if (order is null) return NotFound();
            return Ok(Map(order));
        }
    """
    order = await service.get_order(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found",
        )
    return _map_order_response(order)


@router.put(
    "/{order_id}/confirm",
    response_model=OrderResponse,
    summary="Подтвердить заказ",
)
async def confirm_order(
    order_id: str,
    service: OrderService = Depends(get_service),
) -> OrderResponse:
    """C#: [HttpPut("{id}/confirm")] public async Task<IActionResult> Confirm(string id)"""
    try:
        order = await service.confirm_order(order_id)
        return _map_order_response(order)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
