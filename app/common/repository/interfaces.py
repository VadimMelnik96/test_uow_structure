from abc import ABC, abstractmethod
from typing import Optional, TypeVar

Entity = TypeVar("Entity")
CreateDTO = TypeVar("CreateDTO")
UpdateDTO = TypeVar("UpdateDTO")
Filters = TypeVar("Filters")
OrderFilters = TypeVar("OrderFilters")


class IRepository(ABC):
    """Абстрактный CRUD - репозиторий"""

    @abstractmethod
    async def create(self, create_dto: CreateDTO) -> Entity:
        """Интерфейс создания объектов"""
        pass

    @abstractmethod
    async def get_list(
        self, filters: Filters, order_filters: Optional[OrderFilters] = None
    ) -> list[Entity]:
        """Интерфейс получения списка объектов"""
        pass

    @abstractmethod
    async def get_one(self, filters: Filters) -> Optional[Entity]:
        """Интерфейс получения одного объекта"""
        pass

    @abstractmethod
    async def update(self, update_dto: UpdateDTO, filters: Filters) -> Entity:
        """Интерфейс обновления одного объекта"""
        pass

    @abstractmethod
    async def delete(self, filters: Filters) -> None:
        """Интерфейс удаления одного объекта"""
        pass

    @abstractmethod
    async def bulk_create(self, data: list[CreateDTO]) -> list[Entity]:
        """Интерфейс массового создания объектов"""
        pass
