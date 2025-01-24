from __future__ import annotations

from types import TracebackType
from typing import  Type

from app.common.uow.interfaces import BaseAbstractUnitOfWork
from app.infrastructure.database.database import Database



class BaseUnitOfWork(BaseAbstractUnitOfWork):
    def __init__(self, db: Database) -> None:
        self.db = db

    async def __aenter__(self):
        await super().__aenter__()
        self.session = self.db.session_factory()


    async def __aexit__(
        self,
        exc_t: Type[BaseException] | None,
        exc_v: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.session.expunge_all()
        await super().__aexit__(exc_t, exc_v, exc_tb)
        await self.session.close()

    async def _commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def expunge_all(self) -> None:
        self.session.expunge_all()

