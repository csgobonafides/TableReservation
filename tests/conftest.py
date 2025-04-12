import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

import controllers.table as table_modul
import controllers.reservation as reservation_modul
from app import app

from core.settings import get_settings, Settings
from db.connector import DatabaseConnector

pytest_plugins = [
    "fixtures.test_db",
    "fixtures.prepare_table",
    "fixtures.prepare_reservation",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest_asyncio.fixture(autouse=True)
async def table_controller(test_db: DatabaseConnector) -> table_modul.TableController:
    table_modul.table_controller = table_modul.TableController(test_db)
    return table_modul.table_controller


@pytest_asyncio.fixture(autouse=True)
async def reservation_controller(test_db: DatabaseConnector) -> reservation_modul.ReservationController:
    reservation_modul.reservation_controller = reservation_modul.ReservationController(test_db)
    return reservation_modul.reservation_controller


@pytest_asyncio.fixture
async def xclient() -> AsyncClient:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(base_url="http://127.0.0.1:8010", transport=transport) as cli:
        yield cli
