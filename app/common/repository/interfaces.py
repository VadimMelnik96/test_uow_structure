from abc import abstractmethod, ABC


class IRepository(ABC):
    """Абстрактный CRUD - репозиторий"""

    @abstractmethod
    async def create(self, create_dto):
        pass

    @abstractmethod
    async def get_list(self, filters, order_filters):
        pass

    @abstractmethod
    async def get_one(self, filters):
        pass

    @abstractmethod
    async def update(self, update_dto, filters):
        pass

    @abstractmethod
    async def delete(self):
        pass

    @abstractmethod
    async def bulk_create(self, data: list):
        pass

