from fastapi import APIRouter
from database import DbSession
from temperature.crud import update_temperatures, get_temperatures
from temperature.schemas import TemperatureResponse

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=list[TemperatureResponse])
async def update_temperatures_endpoint(db: DbSession):
    return await update_temperatures(db)


@router.get("/", response_model=list[TemperatureResponse])
def get_temperatures_endpoint(db: DbSession, city_id: int | None = None):
    return get_temperatures(db, city_id)
