from unittest.mock import ANY
from datetime import datetime, timezone

import pytest
from httpx import AsyncClient

from db.connector import DatabaseConnector
from db.models import Table, Reservation


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_table")
async def test_add_reservation_201(xclient: AsyncClient, test_db: DatabaseConnector, tables: Table):
    payload = {
        "customer_name": "user",
        "reservation_time": datetime(2024, 6, 15, 12, 0, tzinfo=timezone.utc).isoformat(),
        "duration_minutes": 5,
        "table_id": 1
    }
    response = await xclient.post("/reservation/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data == {
        "id": ANY,
        "customer_name": "user",
        "reservation_time": ANY,
        "duration_minutes": 5,
        "create_at": ANY,
        "table": {
            "id": 1,
            "create_at": ANY,
            "name": "table",
            "seats": 1,
            "location": "location1"
        }
    }
    async with test_db.session_maker() as session:
        res_db = await session.get(Reservation, data["id"])
    assert res_db.customer_name == data["customer_name"]
    assert res_db.duration_minutes == data["duration_minutes"]


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_table")
async def test_add_reservation_422(
        xclient: AsyncClient,
        test_db: DatabaseConnector,
):
    payload = {
        "customer_name": 123,
        "reservation_time": datetime(2024, 6, 15, 12, 0, tzinfo=timezone.utc).isoformat(),
        "duration_minutes": 5,
        "table_id": 1
    }
    response = await xclient.post("/reservation/", json=payload)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'type': 'string_type',
                                           'loc': ['body', 'customer_name'],
                                           'msg': 'Input should be a valid string', 'input': 123}]}
