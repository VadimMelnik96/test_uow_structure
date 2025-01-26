from collections.abc import Iterable
from typing import Any

from pydantic import BaseModel
from sqlalchemy import (
    Delete,
    Result,
    ScalarResult,
    Select,
    ValuesBase,
    delete,
    insert,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.common.exceptions.exceptions import NotFoundError
from app.common.repository.interfaces import IRepository


class SQLAlchemyRepository(IRepository):
    """CRUD - репозиторий для SQLAlchemy"""

    model: type[DeclarativeBase] = None
    response_dto: BaseModel = None

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.auto_commit = None
        self.auto_refresh = None

    async def create(
        self,
        create_dto: BaseModel,
        response_dto: DeclarativeBase | None = None,
        auto_commit: bool = True,
    ) -> BaseModel:
        """Создание объекта"""
        stmt = insert(self.model).values(**create_dto.model_dump()).returning(self.model)
        res = await self._execute(stmt)
        return self.to_dto(res.scalar_one(), response_dto)

    async def bulk_create(
        self,
        bulk_create_dto: list[BaseModel],
        response_dto: BaseModel | None = None,
        auto_commit: bool = True,
    ) -> BaseModel:
        """Создание нескольких объектов"""
        stmt = (
            insert(self.model)
            .values([entity.model_dump() for entity in bulk_create_dto])
            .returning(self.model)
        )
        res = await self._execute(stmt)
        return self.to_dto(res.scalar_one(), response_dto)

    async def get_one(self, filters: BaseModel, response_dto: BaseModel | None = None) -> BaseModel:
        """Получение одного объекта"""
        stmt = select(self.model).filter_by(**filters.model_dump(exclude_none=True))
        result = await self._execute(stmt)
        instance = result.scalar_one_or_none()
        self.check_not_found(instance)
        return self.to_dto(instance, response_dto)

    async def get_list(
        self,
        response_dto: DeclarativeBase | None = None,
        filters: BaseModel = None,
        order_filters: BaseModel = None,
    ) -> list[BaseModel]:
        """Получение списка объектов"""
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters.model_dump(exclude_none=True))
        if order_filters:
            if order_filters.limit:
                stmt = stmt.limit(order_filters.limit)
            if order_filters.offset:
                stmt = stmt.offset(order_filters.offset)
            if order_filters.ordering:
                stmt = stmt.order_by(order_filters.ordering)
        res = await self._execute(stmt)
        return self.to_dto(res.scalars())

    async def update(
        self,
        update_dto: BaseModel,
        filters: BaseModel,
        response_dto: BaseModel | None = None,
        auto_commit: bool = True,
    ) -> BaseModel:
        """Обновление объекта"""
        stmt = (
            update(self.model)
            .values(**update_dto.model_dump(exclude_unset=True))
            .filter_by(**filters.model_dump(exclude_unset=True))
            .returning(self.model)
        )  # noqa: ANN003
        res = (await self._execute(stmt)).scalar_one_or_none()
        self.check_not_found(res)
        return self.to_dto(res, response_dto)

    async def delete(self, auto_commit: bool = True, **filters: BaseModel) -> None:
        """Удаление объекта"""
        stmt = delete(self.model).filter_by(**filters)
        result = await self._execute(stmt)
        if result.rowcount == 0:
            raise NotFoundError(
                f"По данным запроса в таблице {self.model.__tablename__} записей не найдено"
            )

    def to_dto(
        self, instance: DeclarativeBase | ScalarResult, dto: BaseModel = None
    ) -> BaseModel | list[BaseModel]:
        """Метод, преобразующий модели SQLAlchemy к dto."""
        if dto is None:
            dto = self.response_dto
        if not isinstance(instance, ScalarResult | list):
            return dto.model_validate(instance, from_attributes=True)
        return [dto.model_validate(row, from_attributes=True) for row in instance]

    async def _refresh(
        self,
        instance: DeclarativeBase,
        auto_refresh: bool | None,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
    ) -> None:
        """Метод обновления объекта в сессии"""
        if auto_refresh is None:
            auto_refresh = self.auto_refresh

        return (
            await self.session.refresh(
                instance,
                attribute_names=attribute_names,
                with_for_update=with_for_update,
            )
            if auto_refresh
            else None
        )

    @staticmethod
    def check_not_found(item_or_none: DeclarativeBase | None) -> DeclarativeBase:
        """Метод проверки на существование в базе"""
        if item_or_none is None:
            msg = "No item found when one was expected"
            raise NotFoundError(msg)
        return item_or_none

    async def _execute(self, statement: ValuesBase | Select[Any] | Delete) -> Result[Any]:
        """Метод выполнения запроса"""
        return await self.session.execute(statement)
