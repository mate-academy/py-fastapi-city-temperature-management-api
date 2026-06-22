from fastapi import APIRouter

from app.schemas import temperature as temp_schema
from app.dependencies import CurrentSession
from app.services import temperature_service

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=list[temp_schema.Temperature])
async def update_temperatures(
        db: CurrentSession
) -> list[temp_schema.Temperature]:
    return await temperature_service.update_all_temperatures(db)


@router.get("/", response_model=list[temp_schema.Temperature])
def get_temperatures(
        db: CurrentSession,
        city_id: int | None = None
) -> list[temp_schema.Temperature]:
    return temperature_service.get_temperatures(db, city_id)
