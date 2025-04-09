from datetime import datetime
from pydantic import BaseModel
from schemas.table import TableDtlInfo


class ReservationBase(BaseModel):
    customer_name: str
    reservation_time: datetime
    duration_minutes: int


class ReservationIN(ReservationBase):
    table_id: int


class ReservationDtlInfo(ReservationBase):
    id: int
    table: TableDtlInfo
