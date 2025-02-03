import asyncio
import pathlib
import uuid
from typing import Callable

import pytest
from _pytest.fixtures import SubRequest
from alembic import command
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

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
def test_db_name() -> str:
    """Генерация уникального имени тестовой базы данных."""
    return f"test_db_{uuid.uuid4().hex}"


@pytest.fixture(scope="session")
async def create_test_db(settings: Settings, test_db_name: str) -> None:
    """Создание тестовой базы данных."""
    admin_engine = create_async_engine(
        str(settings.database.dsn).replace(settings.database.db, "postgres"),
        isolation_level="AUTOCOMMIT",
    )

    async with admin_engine.connect() as conn:
        await conn.execute(text(f"CREATE DATABASE {test_db_name}"))

    await admin_engine.dispose()


@pytest.fixture(scope="session")
async def drop_test_db(settings: Settings, test_db_name: str) -> None:
    """Удаление тестовой базы данных."""
    yield

    admin_engine = create_async_engine(
        str(settings.database.dsn).replace(settings.database.db, "postgres"),
        isolation_level="AUTOCOMMIT",
    )

    async with admin_engine.connect() as conn:
        # Завершаем все соединения с тестовой базой данных
        await conn.execute(
            text(
                f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{test_db_name}'
                AND pid <> pg_backend_pid();
                """
            )
        )
        await conn.execute(text(f"DROP DATABASE {test_db_name}"))

    await admin_engine.dispose()


@pytest.fixture(scope="session")
def project_dir(request: SubRequest) -> pathlib.Path:
    """Директория расположения проекта."""
    return pathlib.Path(request.config.rootdir)


@pytest.fixture(scope="session")
def migrations_dir(request: SubRequest) -> pathlib.Path:
    """Директория расположения миграций."""
    return pathlib.Path(request.config.rootdir) / "app/infrastructure/database/migrations"


@pytest.fixture(scope="session")
async def db(
    settings: Settings,
    test_db_name: str,
    create_test_db: Callable,
    drop_test_db: Callable,
    request: SubRequest,
    migrations_dir: pathlib.Path,
    project_dir: pathlib.Path,
) -> Database:
    """Фикстура для инициализации тестовой базы данных."""
    test_db_url = str(settings.database.dsn).replace(settings.database.db, test_db_name)

    class TestDatabase:
        """Вспомогательный класс для работы с БД"""

        def __init__(self, dsn: str):
            self.engine = create_async_engine(url=str(dsn), echo=True, pool_size=5, max_overflow=10)

            self.session_factory = async_sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )

    database = TestDatabase(dsn=test_db_url)

    # Применяем миграции Alembic
    alembic_cfg = Config(project_dir / "alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url.replace("+asyncpg", ""))
    alembic_cfg.set_main_option("script_location", str(migrations_dir))

    engine = create_async_engine(test_db_url)

    async with engine.connect() as connection:

        def run_migrations(connection):
            with connection.begin():
                command.upgrade(alembic_cfg, "head")

        await connection.run_sync(run_migrations)

    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return database


@pytest.fixture()
async def db_session(db: Database) -> AsyncSession:
    """Фикстура для создания изолированной сессии для каждого теста."""
    async with db.session_factory() as session:  # noqa: SIM117
        async with session.begin():  # noqa: SIM117
            yield session
            await session.rollback()


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
