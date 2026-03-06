"""
Интеграционные тесты API через AsyncClient
==========================================
Аналогии C# (WebApplicationFactory) → Python (httpx AsyncClient):
  WebApplicationFactory<Program>   = ASGITransport(app=app)
  factory.CreateClient()           = AsyncClient(transport=..., base_url=...)
  client.GetAsync("/health")       = await client.get("/health")
  Assert.Equal(HttpStatusCode.OK)  = assert response.status_code == 200
  response.Content.ReadAsStringAsync() = response.json()
"""

import pytest
from httpx import AsyncClient


class TestHealthCheck:

    async def test_health_check_returns_200(self, client: AsyncClient) -> None:
        """C#: Assert.Equal(HttpStatusCode.OK, response.StatusCode)"""
        response = await client.get("/health")
        assert response.status_code == 200

    async def test_health_check_returns_healthy(self, client: AsyncClient) -> None:
        response = await client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    async def test_root_returns_welcome(self, client: AsyncClient) -> None:
        response = await client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


class TestCreateOrder:

    async def test_create_order_returns_201(self, client: AsyncClient) -> None:
        """
        C# аналог:
            var response = await client.PostAsJsonAsync("/api/v1/orders", request);
            Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        """
        payload = {
            "customer_name": "Alice",
            "items": [
                {"name": "Widget", "unit_price": 10.0, "quantity": 2},
            ],
        }
        response = await client.post("/api/v1/orders/", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["customer_name"] == "Alice"
        assert data["status"] == "PENDING"
        assert "id" in data
        assert len(data["id"]) > 0

    async def test_create_order_calculates_total(self, client: AsyncClient) -> None:
        payload = {
            "customer_name": "Bob",
            "items": [
                {"name": "Item A", "unit_price": 10.0, "quantity": 3},
                {"name": "Item B", "unit_price": 5.0, "quantity": 2},
            ],
        }
        response = await client.post("/api/v1/orders/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["total"] == pytest.approx(40.0)  # 30 + 10

    async def test_validation_negative_price_returns_422(self, client: AsyncClient) -> None:
        """
        C# аналог: ModelState validation → 422 Unprocessable Entity
        Pydantic автоматически возвращает 422 при нарушении правил.
        """
        payload = {
            "customer_name": "Alice",
            "items": [
                {"name": "Widget", "unit_price": -10.0, "quantity": 1},
            ],
        }
        response = await client.post("/api/v1/orders/", json=payload)
        assert response.status_code == 422

    async def test_validation_zero_quantity_returns_422(self, client: AsyncClient) -> None:
        payload = {
            "customer_name": "Alice",
            "items": [
                {"name": "Widget", "unit_price": 10.0, "quantity": 0},
            ],
        }
        response = await client.post("/api/v1/orders/", json=payload)
        assert response.status_code == 422

    async def test_validation_empty_items_returns_422(self, client: AsyncClient) -> None:
        payload = {"customer_name": "Alice", "items": []}
        response = await client.post("/api/v1/orders/", json=payload)
        assert response.status_code == 422


class TestGetOrder:

    async def test_get_404_for_unknown_order(self, client: AsyncClient) -> None:
        """C#: Assert.Equal(HttpStatusCode.NotFound, response.StatusCode)"""
        response = await client.get("/api/v1/orders/nonexistent-id")
        assert response.status_code == 404

    async def test_get_created_order(self, client: AsyncClient) -> None:
        # Создаём заказ
        create_response = await client.post("/api/v1/orders/", json={
            "customer_name": "Charlie",
            "items": [{"name": "Gadget", "unit_price": 99.99, "quantity": 1}],
        })
        assert create_response.status_code == 201
        order_id = create_response.json()["id"]

        # Получаем его
        get_response = await client.get(f"/api/v1/orders/{order_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == order_id

    async def test_get_all_orders(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/orders/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestConfirmFlow:

    async def test_confirm_flow(self, client: AsyncClient) -> None:
        """
        Полный сценарий: создать → подтвердить → повторный confirm = 400.

        C# аналог:
            // Arrange: создать заказ
            var created = await client.PostAsJsonAsync(...);
            var id = (await created.Content.ReadFromJsonAsync<OrderResponse>()).Id;

            // Act: подтвердить
            var confirmed = await client.PutAsync($".../confirm");
            Assert.Equal(HttpStatusCode.OK, confirmed.StatusCode);

            // Assert: повторный confirm = BadRequest
            var repeat = await client.PutAsync($".../confirm");
            Assert.Equal(HttpStatusCode.BadRequest, repeat.StatusCode);
        """
        # Создать заказ
        create_resp = await client.post("/api/v1/orders/", json={
            "customer_name": "Diana",
            "items": [{"name": "Book", "unit_price": 25.0, "quantity": 1}],
        })
        assert create_resp.status_code == 201
        order_id = create_resp.json()["id"]

        # Подтвердить
        confirm_resp = await client.put(f"/api/v1/orders/{order_id}/confirm")
        assert confirm_resp.status_code == 200
        assert confirm_resp.json()["status"] == "CONFIRMED"

        # Повторный confirm → 400
        repeat_resp = await client.put(f"/api/v1/orders/{order_id}/confirm")
        assert repeat_resp.status_code == 400

    async def test_confirm_unknown_order_returns_400(self, client: AsyncClient) -> None:
        response = await client.put("/api/v1/orders/nonexistent/confirm")
        assert response.status_code == 400
