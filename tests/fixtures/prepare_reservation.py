from datetime import datetime, timezone

import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import Reservation


@pytest.fixture
def reservations() -> list[Reservation]:
    return [
        Reservation(
            id=2,
            customer_name="user",
            reservation_time=datetime(2024, 6, 15, 12, 0, tzinfo=timezone.utc),
            duration_minutes=5,
            table_id=2
    ),
        Reservation(
            id=3,
            customer_name="user2",
            reservation_time=datetime(2024, 8, 15, 12, 0, tzinfo=timezone.utc),
            duration_minutes=5,
            table_id=2
    )
    ]


@pytest_asyncio.fixture
async def prepare_reservation(
        test_db: DatabaseConnector,
        reservations: list[Reservation],
        prepare_table: None
) -> None:
    async with test_db.session_maker(expire_on_commit=False) as session:
        session.add_all(reservations)
        await session.commit()
