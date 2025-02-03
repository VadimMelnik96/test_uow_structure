from collections.abc import Sequence
from typing import Self

from dotenv import load_dotenv
from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class EnvBaseSettings(BaseSettings):
    """Базовый класс для прокидывания настроек из env"""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class PostgresConfig(EnvBaseSettings):
    """Настройки Postgres"""

    scheme: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    db: str = "postgres"
    pool_size: int = 10
    pool_overflow_size: int = 10
    leader_usage_coefficient: float = 0.3
    echo: bool = False
    autoflush: bool = False
    autocommit: bool = False
    expire_on_commit: bool = False
    engine_health_check_delay: int = 1
    dsn: PostgresDsn | None = None
    slave_hosts: Sequence[str] | str = ""
    slave_dsns: Sequence[PostgresDsn] | str = ""

    @model_validator(mode="after")
    def assemble_db_connection(self) -> Self:
        """Сборка Postgres DSN"""
        if self.dsn is None:
            self.dsn = str(
                PostgresDsn.build(
                    scheme=self.scheme,
                    username=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    path=f"{self.db}",
                )
            )
        return self

    model_config = SettingsConfigDict(env_prefix="postgres_")


class AppSettings(EnvBaseSettings):
    """Настройки приложения FastAPI."""

    name: str = ""
    debug: bool = True
    root_path: str = ""
    model_config = SettingsConfigDict(env_prefix="app_")


class RedisSettings(EnvBaseSettings):
    """Настройки Redis"""

    dsn: RedisDsn | None = None
    prefix: str = ""
    model_config = SettingsConfigDict(env_prefix="redis_")


class Settings(EnvBaseSettings):
    """Настройки проекта"""

    app: AppSettings = AppSettings()
    database: PostgresConfig = PostgresConfig()


config = Settings()
