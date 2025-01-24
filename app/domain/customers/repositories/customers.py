from app.common.repository.repository import SQLAlchemyRepository
from app.domain.customers.customer import Customer
from app.domain.customers.repositories.interfaces import ICustomersRepository
from app.domain.models.customers import Customers


class CustomerRepo(SQLAlchemyRepository, ICustomersRepository):
    model = Customers
    response_dto = Customer