from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.settings.settings import PostgresConfig


class Database:
    """Вспомогательный класс для работы с БД"""

    def __init__(self, config: PostgresConfig):
        self.engine = create_async_engine(
            url=str(config.dsn), echo=config.echo, pool_size=5, max_overflow=10
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=config.autoflush,
            autocommit=config.autocommit,
            expire_on_commit=config.expire_on_commit,
        )
