from typing import Optional

from app.adapters.api.http.v1.dto.customer import CustomerCreateCommand
from app.common.models.arbitrary_model import ArbitraryModel
from app.domain.orders.order import OrderCreateDTO


class CustomerCreateDTO(ArbitraryModel):
    first_name: str
    last_name: str




class Customer(CustomerCreateDTO):
    id: Optional[int]

