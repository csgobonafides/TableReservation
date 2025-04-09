from pydantic import BaseModel


class TableIN(BaseModel):
    name: str
    seats: int
    location: str


class TableDtlInfo(TableIN):
    id: int
