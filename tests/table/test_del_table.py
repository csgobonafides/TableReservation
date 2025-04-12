import pytest
from httpx import AsyncClient

from db.connector import DatabaseConnector
from db.models import Table


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_table")
async def test_del_table_204(xclient: AsyncClient, test_db: DatabaseConnector):
    response = await xclient.delete("/table/2")
    assert response.status_code == 204
    assert response.content == b""
    async with test_db.session_maker() as session:
        del_table = await session.get(Table, 2)
    assert del_table is None


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_table")
async def test_del_table_404(xclient: AsyncClient, test_db: DatabaseConnector):
    response = await xclient.delete("/table/5")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Table not found.'}
