from app.common.repository.repository import SQLAlchemyRepository

from app.domain.models.orders import Orders
from app.domain.orders.order import Order
from app.domain.orders.repositories.interfaces import IOrdersRepository


class OrderRepo(SQLAlchemyRepository, IOrdersRepository):
    model = Orders
    response_dto = Order
