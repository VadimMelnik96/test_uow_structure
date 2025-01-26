from app.common.models.arbitrary_model import ArbitraryModel


class OrderCreateDTO(ArbitraryModel):
    """ДТО создания заказов"""

    customer_id: int
    name: str
    price: int


class Order(OrderCreateDTO):
    """Выходное ДТО для заказов"""

    id: int
