import httpx


class TestCustomerAPI:
    """Тесты API заказчиков"""

    async def test_create_customer(self, client: httpx.AsyncClient, customer_data: dict) -> None:
        """Тест создания заказчика"""
        response = await client.post("/customers", json=customer_data)
        assert response.status_code == 200
