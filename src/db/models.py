from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, DateTime, INT, ForeignKey, CheckConstraint


class BaseModel(DeclarativeBase):
    id = Column(INT, primary_key=True)


class Table(BaseModel):

    __tablename__ = "table"

    name = Column(String(100), unique=True, nullable=False)
    seats = Column(INT, CheckConstraint("seats >= 1 AND seats <= 10"), nullable=False)
    location = Column(String(100), unique=False, nullable=False)

    def __repr__(self) -> str:
        return f"Table({self.id=}, {self.name=}, {self.seats=}, {self.location})"


class Reservation(BaseModel):

    __tablename__ = "reservation"

    customer_name = Column(String(100), unique=True, nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    duration_minutes = Column(INT, CheckConstraint("duration_minutes >= 1"), nullable=False)
    table_id = Column(ForeignKey(Table.id), nullable=False)

    table = relationship(Table, backref="reservations")

    def __repr__(self) -> str:
        return (
            f"Reservation({self.id=}, "
            f"{self.customer_name=}, "
            f"{self.reservation_time=}, "
            f"{self.duration_minutes=}, "
            f"{self.table_id=})"
        )
