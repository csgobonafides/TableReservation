from fastapi import  APIRouter, Depends, status

from controllers.reservation import get_controller, ReservationController
from schemas.reservation import ReservationIN, ReservationDtlInfo


router = APIRouter()


@router.get('/', response_model=list[ReservationDtlInfo], status_code=status.HTTP_200_OK)
async def all_reservation(
        controller: ReservationController = Depends(get_controller)
) -> list[ReservationDtlInfo]:
    return await controller.all_reservation()


@router.post('/', response_model=ReservationDtlInfo, status_code=status.HTTP_201_CREATED)
async def add_reservation(
        reservation: ReservationIN,
        controller: ReservationController = Depends(get_controller)
) -> ReservationDtlInfo:
    return await controller.add_reservation(reservation=reservation)


@router.delete('/{reservation_id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_reservation(
        reservation_id: int,
        controller: ReservationController = Depends(get_controller)
) -> None:
    return await controller.del_reservation(reservation_id=reservation_id)
