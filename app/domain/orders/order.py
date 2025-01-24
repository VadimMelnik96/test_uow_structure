from app.common.models.arbitrary_model import ArbitraryModel


class OrderCreateDTO(ArbitraryModel):
    customer_id: int
    name: str
    price: int


class Order(OrderCreateDTO):
    id: int
