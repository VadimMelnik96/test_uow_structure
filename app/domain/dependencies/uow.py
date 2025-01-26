from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from app.domain.unit_of_work import IUnitOfWork, UnitOfWork
from app.infrastructure.database.database import Database
from app.services.customer_service import CustomerService
from app.services.interfaces import ICustomerService
from app.settings.settings import config


async def get_uow() -> UnitOfWork:
    """Зависимость, возвращающая UOW"""
    db = Database(config=config.database)  # Инициализация базы данных
    return UnitOfWork(db)


async def get_customer_service(
    uow: Annotated[IUnitOfWork, Depends(get_uow)]
) -> AsyncGenerator[ICustomerService, None]:
    """Зависимость, возвращающаяя сервис"""
    yield CustomerService(uow)
