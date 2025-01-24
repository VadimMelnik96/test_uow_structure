import abc
from types import TracebackType
from typing import Type

class BaseAbstractUnitOfWork(abc.ABC):
    async def commit(self) -> None:
        await self._commit()

    @abc.abstractmethod
    async def rollback(self) -> None: ...

    @abc.abstractmethod
    async def expunge_all(self) -> None:
        """Remove all objects from uow."""
        ...

    @abc.abstractmethod
    async def _commit(self) -> None: ...

    async def __aenter__(self) -> None:
        pass

    async def __aexit__(
        self,
        exc_t: Type[BaseException] | None,
        exc_v: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.rollback()