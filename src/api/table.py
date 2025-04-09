from fastapi import APIRouter, Depends, status

from controllers.table import get_controller, TableController
from schemas.table import TableIN, TableDtlInfo


router = APIRouter()


@router.get('/', response_model=list[TableDtlInfo], status_code=status.HTTP_200_OK)
async def list_table(
        controller: TableController = Depends(get_controller)
) -> list[TableDtlInfo]:
    return await controller.all_table()


@router.post('/', response_model=TableDtlInfo, status_code=status.HTTP_201_CREATED)
async def add_table(
        table: TableIN,
        controller: TableController = Depends(get_controller)
) -> TableDtlInfo:
    return await controller.add_table(table=table)


@router.delete('/{table_id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_table(
        table_id: int,
        controller: TableController = Depends(get_controller)
) -> None:
    return await controller.del_table(table_id=table_id)
