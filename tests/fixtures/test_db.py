import uuid
from datetime import datetime
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

from core.settings import Settings, DatabaseConfig
from db.models import BaseModel
from db.connector import DatabaseConnector


ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent / "src"

@pytest.fixture(scope="session")
def database_name() -> str:
    return f"{uuid.uuid4().hex}.pytest"


@pytest.fixture(scope="session")
def database(settings: Settings) -> DatabaseConfig:
    return settings.DB


@pytest.fixture(scope="session")
def prepare_test_database(database_name: str, database: DatabaseConfig) -> None:
    real_database_dsn = f"postgresql://{database.USERNAME}:{database.PASSWORD}@{database.HOST}:{database.PORT}/{database.NAME}"
    test_database_dsn = f"postgresql://{database.USERNAME}:{database.PASSWORD}@{database.HOST}:{database.PORT}/{database_name}"
    with create_engine(
        real_database_dsn, isolation_level="AUTOCOMMIT"
    ).connect() as connection:
        connection.execute(text(f'CREATE DATABASE "{database_name}"'))
    try:
        migration_dir = ROOT_DIR / "db" / "alembic"
        alembic_file = ROOT_DIR / "alembic.ini"
        alembic_cfg = Config(alembic_file.as_posix())
        alembic_cfg.set_main_option("script_location", migration_dir.as_posix())
        alembic_cfg.set_main_option("sqlalchemy.url", test_database_dsn)
        command.upgrade(alembic_cfg, "head")

        yield test_database_dsn

    finally:
        with create_engine(
            real_database_dsn, isolation_level="AUTOCOMMIT"
        ).connect() as connection:
            q1 = text(
                "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
                "FROM pg_stat_activity "
                f"WHERE pg_stat_activity.datname = '{database_name}' AND pid <> pg_backend_pid();"
            )
            q2 = text(f'DROP DATABASE "{database_name}";')
            connection.execute(q1)
            connection.execute(q2)


@pytest.fixture
def test_db(
    prepare_test_database: str, database: DatabaseConfig, database_name: str
) -> DatabaseConnector:
    conf = database.model_copy(update={"NAME": database_name})
    _db = DatabaseConnector(conf.asyncpg_url)
    yield _db
    start_time = datetime.now()
    with create_engine(
        prepare_test_database, isolation_level="AUTOCOMMIT"
    ).connect() as connection:
        tables = ",".join(f'"{str(table)}"' for table in BaseModel.metadata.tables)
        connection.execute(text(f"TRUNCATE TABLE {tables} CASCADE"))
    print(
        f"Truncate tables took {datetime.now() - start_time} seconds, truncated tables: {tables}"
    )
