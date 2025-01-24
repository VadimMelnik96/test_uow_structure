from pydantic import BaseModel

from app.common.models.arbitrary_model import ArbitraryModel



class OrderCreate(BaseModel):
    price: int
    name: str


class CustomerCreateCommand(ArbitraryModel):
    first_name: str
    last_name: str
    orders: list[OrderCreate]


