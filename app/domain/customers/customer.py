from typing import Optional

from app.common.models.arbitrary_model import ArbitraryModel


class CustomerCreateDTO(ArbitraryModel):
    """ДТО создания потребителя"""

    first_name: str
    last_name: str


class Customer(CustomerCreateDTO):
    """Возвратное ДТО потребителя"""

    id: Optional[int]
