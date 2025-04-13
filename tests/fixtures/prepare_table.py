
import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import Table


@pytest.fixture
def tables() -> list[Table]:
    return [
        Table(
            id=2,
            name="table",
            seats=1,
            location="location1"
    ),
        Table(
            id=3,
            name="table2",
            seats=1,
            location="location2"
    )
    ]


@pytest_asyncio.fixture
async def prepare_table(test_db: DatabaseConnector, tables: list[Table]) -> None:
    async with test_db.session_maker(expire_on_commit=False) as session:
        session.add_all(tables)
        await session.commit()
