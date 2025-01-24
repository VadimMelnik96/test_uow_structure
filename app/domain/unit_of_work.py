import abc

from sqlalchemy.orm import Session

from app.common.uow.interfaces import BaseAbstractUnitOfWork
from app.common.uow.uow import BaseUnitOfWork
from app.domain.customers.repositories.customers import CustomerRepo
from app.domain.customers.repositories.interfaces import ICustomersRepository
from app.domain.orders.repositories.interfaces import IOrdersRepository
from app.domain.orders.repositories.orders import OrderRepo


class IUnitOfWork(BaseAbstractUnitOfWork, abc.ABC):
    """Интерфейс единицы работы."""

    customers: ICustomersRepository
    orders: IOrdersRepository



class UnitOfWork(BaseUnitOfWork, IUnitOfWork):

    async def __aenter__(self) -> None:
        """Инициализация сессии и репозиториев."""
        await super().__aenter__()
        self.customers = CustomerRepo(session=self.session)
        self.orders = OrderRepo(session=self.session)