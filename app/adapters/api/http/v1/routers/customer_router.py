from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.adapters.api.http.v1.dto.customer import CustomerCreateCommand
from app.domain.dependencies.uow import get_customer_service
from app.services.interfaces import ICustomerService

router = APIRouter(tags=["Customers"])


@router.post("/customers")
async def create_customers_with_orders(
    customer_data: CustomerCreateCommand,
    service: Annotated[ICustomerService, Depends(get_customer_service)],
) -> dict[str, Any]:
    """Создание пользователя и заказа"""
    await service.create_customer_with_orders(customer_data)
    return {"message": "Customer and orders created successfully"}
