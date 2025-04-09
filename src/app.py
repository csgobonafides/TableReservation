from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from api.table import router as table_router
from api.reservation import router as reservation_router
from db.connector import DatabaseConnector
from core.settings import get_settings
import controllers.table as table_modul
import controllers.reservation as reservation_modul


logger = logging.getLogger(__name__)
config = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Launching the application.")
    db = DatabaseConnector(config.DB.asyncpg_url)
    table_modul.table_controller = table_modul.TableController(db=db)
    reservation_modul.reservation_controller = reservation_modul.ReservationController(db=db)
    yield
    logger.info("Application shutdown.")
    await db.disconnect()


app = FastAPI(lifespan=lifespan, title="FastAPI")
app.include_router(table_router, tags=["table"], prefix="/table")
app.include_router(reservation_router, tags=["reservation"], prefix="/reservation")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config="core/logging.yaml")
