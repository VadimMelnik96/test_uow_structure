import asyncio

import pytest
from alembic import command
from alembic.config import Config
from httpx import AsyncClient

from app.adapters.api.http.main import app
from app.domain.dependencies.uow import get_db
from app.domain.models.base import Base
from app.infrastructure.database.database import Database
from app.settings.settings import Settings


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Фикстура для настройки anyio."""
    return "asyncio"


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Фикстура настроек"""
    return Settings()


@pytest.fixture(scope="session")
async def db(settings: Settings) -> Database:
    """Фикстура для инициализации тестовой базы данных."""
    database = Database(config=settings.database)
    engine = database.engine
    # Создаем все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield database
    # Удаляем все таблицы после завершения тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def _apply_migrations(settings: Settings) -> None:
    """Фикстура для применения миграций Alembic."""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.database.dsn))
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


@pytest.fixture()
async def client(db: Database) -> AsyncClient:
    """Фикстура для тестового клиента FastAPI."""

    def override_get_db():  # noqa: ANN202
        async def get_db_override() -> Database:
            yield db

        return get_db_override

    app.dependency_overrides[get_db] = override_get_db()
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def customer_data() -> dict:
    """Данные пользователя"""
    return {
        "first_name": "clark",
        "last_name": "kent",
        "orders": [{"price": 100, "name": "coat"}, {"price": 100, "name": "shoes"}],
    }
