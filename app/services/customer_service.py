from app.adapters.api.http.v1.dto.customer import CustomerCreateCommand
from app.domain.customers.customer import CustomerCreateDTO
from app.domain.orders.order import OrderCreateDTO
from app.domain.unit_of_work import IUnitOfWork
from app.services.interfaces import ICustomerService


class CustomerService(ICustomerService):
    """Сервис пользователей"""

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create_customer_with_orders(self, command: CustomerCreateCommand) -> None:
        """Создание пользователя и его заказов"""
        async with self.uow:
            customer_dto = CustomerCreateDTO(
                first_name=command.first_name, last_name=command.last_name
            )
            customer = await self.uow.customers.create(customer_dto)

            for order in command.orders:
                order_dto = OrderCreateDTO(
                    customer_id=customer.id, name=order.name, price=order.price
                )
                await self.uow.orders.create(order_dto)
            await self.uow.commit()
