import abc

from app.adapters.api.http.v1.dto.customer import CustomerCreateCommand


class ICustomerService(abc.ABC):

    @abc.abstractmethod
    async def create_customer_with_orders(self, command: CustomerCreateCommand):
        pass