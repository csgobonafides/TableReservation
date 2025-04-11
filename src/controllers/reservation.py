import logging
from datetime import timedelta
from sqlalchemy import select, or_, text, cast, Interval
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload

from schemas.reservation import ReservationIN, ReservationDtlInfo
from schemas.table import TableDtlInfo
from db.models import Reservation, Table
from core.exceptions import NotFoundError


logger = logging.getLogger("reservation_controller")


from core.exceptions import BadRequestError
from db.connector import DatabaseConnector


class ReservationController:

    def __init__(self, db: DatabaseConnector):
        self.db = db


    async def add_reservation(self, reservation: ReservationIN) -> ReservationDtlInfo:

        logger.info("Request to create a new reservation.")

        async with self.db.session_maker() as session:

            table_exists = await session.execute(
                select(Table).filter(Table.id == reservation.table_id)
            )
            if not table_exists.scalars().first():
                logger.error("Table with the specified ID does not exist.")
                raise BadRequestError("Table with the specified ID does not exist.")

            end_time = reservation.reservation_time + timedelta(minutes=reservation.duration_minutes)

            existing_reservations = await session.execute(select(Reservation).filter(
                Reservation.table_id == reservation.table_id,
                or_(
                    Reservation.reservation_time.between(reservation.reservation_time, end_time),
                    (Reservation.reservation_time +
                     cast(Reservation.duration_minutes * text("interval '1 minute'"), Interval))
                     .between(reservation.reservation_time, end_time))
                )
            )
            existing_reservations = existing_reservations.scalars().all()

            if existing_reservations:
                logger.error("Table is already reserved for the specified time slot.")
                raise BadRequestError("Table is already reserved for the specified time slot.")

            new_reservation = Reservation(
                customer_name=reservation.customer_name,
                reservation_time=reservation.reservation_time,
                duration_minutes=reservation.duration_minutes,
                table_id=reservation.table_id
            )

            session.add(new_reservation)
            try:
                await session.commit()
                await session.refresh(new_reservation)
                logger.info("The table is reserved.")

                query = select(Reservation).options(selectinload(Reservation.table)).where(Reservation.id == new_reservation.id)
                result = await session.execute(query)
                reserv = result.scalars().first()
                return ReservationDtlInfo(
                    id=reserv.id,
                    customer_name=reserv.customer_name,
                    reservation_time=reserv.reservation_time,
                    duration_minutes=reserv.duration_minutes,
                    create_at=str(reserv.create_at),
                    table=TableDtlInfo(
                        id=reserv.table.id,
                        name=reserv.table.name,
                        seats=reserv.table.seats,
                        location=reserv.table.location,
                    )
                )
            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Failed to create reservation due to integrity error: {e}.")
                raise BadRequestError("Failed to create reservation due to integrity error.")


    async def all_reservation(self) -> list[ReservationDtlInfo]:

        logger.info("A list of all reservation has been requested.")

        async with self.db.session_maker() as session:
            query = (select(Reservation).options(joinedload(Reservation.table)))
            result = await session.execute(query)
            reservations = result.scalars().all()

        return [
            ReservationDtlInfo(
                id=reserv.id,
                customer_name=reserv.customer_name,
                reservation_time=reserv.reservation_time,
                duration_minutes=reserv.duration_minutes,
                create_at=str(reserv.create_at),
                table=TableDtlInfo(
                    id=reserv.table.id,
                    name=reserv.table.name,
                    seats=reserv.table.seats,
                    location=reserv.table.location
                )
            )
            for reserv in reservations
        ]


    async def del_reservation(self, reservation_id: int) -> None:

        logger.info("Request to delete a reservation.")

        async with self.db.session_maker() as session:
            reservation = await session.get(Reservation, reservation_id)
            if not reservation:
                logger.error("Reservations with this ID were not found.")
                raise NotFoundError("Reservations with this ID were not found.")
            await session.delete(reservation)
            await session.commit()


reservation_controller: ReservationController = None

def get_controller() -> ReservationController:
    if reservation_controller is None:
        raise BadRequestError("Controller is none.")
    return reservation_controller
