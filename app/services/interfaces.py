import abc

from app.adapters.api.http.v1.dto.customer import CustomerCreateCommand


class ICustomerService(abc.ABC):
    """Интерфейс сервиса пользователей"""

    @abc.abstractmethod
    async def create_customer_with_orders(self, command: CustomerCreateCommand) -> None:
        """Создание пользователя и его заказов"""
        pass
