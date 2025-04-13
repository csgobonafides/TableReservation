import pytest
from unittest.mock import ANY
from httpx import AsyncClient

from db.connector import DatabaseConnector
from db.models import Table


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_table")
async def test_add_table_201(xclient: AsyncClient, test_db: DatabaseConnector):
    payload = {"name": "table3", "seats": 4, "location": "location"}
    response = await xclient.post("/table/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data == {"id": ANY, "name":"table3", "seats": 4, "location": "location", 'create_at': ANY}
    async with test_db.session_maker() as session:
        table_db = await session.get(Table, data["id"])
        assert table_db.name == data["name"]
        assert table_db.seats == data["seats"]
        assert table_db.location == data["location"]


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_table")
async def test_add_table_400(xclient: AsyncClient, test_db: DatabaseConnector):
    payload = {"name": "table", "seats": 2, "location": "location"}
    response = await xclient.post("/table/", json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': 'An object with this name already exists.'}


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_table")
async def test_add_table_422_name(xclient: AsyncClient, test_db: DatabaseConnector):
    payload = {"name": 123, "seats": 2, "location": "location"}
    response = await xclient.post("/table/", json=payload)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': 123,
                                           'loc': ['body', 'name'],
                                           'msg': 'Input should be a valid string',
                                           'type': 'string_type'}]}

