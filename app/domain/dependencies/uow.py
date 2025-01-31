from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from app.domain.unit_of_work import IUnitOfWork, UnitOfWork
from app.infrastructure.database.database import Database
from app.services.customer_service import CustomerService
from app.services.interfaces import ICustomerService
from app.settings.settings import config


async def get_db() -> Database:
    """Инициализация базы данных"""
    yield Database(config=config.database)


async def get_uow(db: Annotated[Database, Depends(get_db)]) -> UnitOfWork:
    """Зависимость, возвращающая UOW"""
    yield UnitOfWork(db)


async def get_customer_service(
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
) -> AsyncGenerator[ICustomerService, None]:
    """Зависимость, возвращающая сервис"""
    yield CustomerService(uow)
