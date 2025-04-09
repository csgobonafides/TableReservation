import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import BadRequestError, NotFoundError
from db.connector import DatabaseConnector
from db.models import Table
from schemas.table import TableDtlInfo, TableIN


logger = logging.getLogger("table_controller")


class TableController:

    def __init__(self, db: DatabaseConnector):
        self.db = db


    async def add_table(self, table: TableIN) -> TableDtlInfo:

        logger.info(f"Requested to create a table: {table.name}.")

        async with self.db.session_maker() as session:
            try:
                tbl = Table(name=table.name, seats=table.seats, location=table.location)
                session.add(tbl)
                await session.commit()
                await session.refresh(tbl)
            except IntegrityError:
                logger.error(f"Attempting to add an existing table: {table.name}")
                raise NotFoundError("An object with this name already exists.")

        return TableDtlInfo(
            id=tbl.id,
            name=tbl.name,
            seats=tbl.seats,
            location=tbl.location
        )


    async def all_table(self) -> list[TableDtlInfo]:

        logger.info("A list of all tables has been requested.")

        async with self.db.session_maker() as session:
            cursor = await session.execute(select(Table))
            tables = cursor.scalars().all()

        return [
            TableDtlInfo(
                id=table.id,
                name=table.name,
                seats=table.seats,
                location=table.location
            )
            for table in tables
        ]


    async def del_table(self, table_id: int) -> None:

        logger.info(f"Request to remove table: {table_id}.")

        async with self.db.session_maker() as session:
            table = await session.get(Table, table_id)
            if not table:
                raise NotFoundError("Table not found.")
            await session.delete(table)
            await session.commit()


table_controller: TableController = None

def get_controller() -> TableController:
    if table_controller is None:
        raise BadRequestError("Controller is none.")
    return table_controller
