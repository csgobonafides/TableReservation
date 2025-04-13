import pytest
from httpx import AsyncClient
from unittest.mock import ANY

from db.models import Table


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_table")
async def test_get_table_200(xclient: AsyncClient, tables: Table):
    response = await xclient.get("/table/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 2,
            "name": "table",
            "seats": 1,
            "location": "location1",
            "create_at": ANY
        },
        {
            "id": 3,
            "name": "table2",
            "seats": 1,
            "location": "location2",
            "create_at": ANY
        }
    ]
