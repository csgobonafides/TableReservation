import pytest
from httpx import AsyncClient
from unittest.mock import ANY

from db.models import Table, Reservation


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_reservation")
async def test_get_reservation_200(xclient: AsyncClient, tables: Table, reservations: Reservation):
    response = await xclient.get("/reservation/")
    assert response.status_code == 200
    assert response.json() == [
        {
            'create_at': ANY,
            'customer_name': "user",
            'duration_minutes': 5,
            'id': 2,
            'reservation_time': ANY,
            'table': {
                'create_at': ANY,
                'id': 2,
                'location': "location1",
                'name': "table",
                'seats': 1
            }
        },
        {
            'create_at': ANY,
            'customer_name': "user2",
            'duration_minutes': 5,
            'id': 3,
            'reservation_time': ANY,
            'table': {
                'create_at': ANY,
                'id': 2,
                'location': "location1",
                'name': "table",
                'seats': 1
            }
        }
    ]
