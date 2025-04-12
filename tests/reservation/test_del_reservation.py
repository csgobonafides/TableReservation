import pytest
from httpx import AsyncClient

from db.connector import DatabaseConnector
from db.models import Reservation


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_reservation")
async def test_del_reservation_204(xclient: AsyncClient, test_db: DatabaseConnector):
    response = await xclient.delete("/reservation/2")
    assert response.status_code == 204
    assert response.content == b""
    async with test_db.session_maker() as session:
        res_db = await session.get(Reservation, 2)
    assert res_db is None


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_reservation")
async def test_del_reservation_404(xclient: AsyncClient, test_db: DatabaseConnector):
    response = await xclient.delete("/reservation/5")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Reservations with this ID were not found.'}
