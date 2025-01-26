from pydantic import BaseModel

from app.common.models.arbitrary_model import ArbitraryModel


class OrderCreate(BaseModel):
    """Полезная нагрузка заказа"""

    price: int
    name: str


class CustomerCreateCommand(ArbitraryModel):
    """Команда создания потребителя с запросами"""

    first_name: str
    last_name: str
    orders: list[OrderCreate]
