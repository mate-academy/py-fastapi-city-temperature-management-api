from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city.schemas import MessageSchema
from dependencies import get_db
from temperature import weather_service
from temperature.crud import get_all_temperatures_crud, get_max_temperature_for_city
from temperature.schemas import CityMaxTemperatureSchema

router = APIRouter(prefix="/temperatures", tags=["temperature"])


async def run_update_task() -> None:
    from database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        await weather_service.update_temperatures_for_all_cities(db)


@router.post("/update", response_model=MessageSchema)
async def update_all_temperatures(background_tasks: BackgroundTasks):

    background_tasks.add_task(run_update_task)
    return MessageSchema(
        message="Task completed",
    )


@router.get("/", response_model=list[CityMaxTemperatureSchema])
async def get_all_temperatures(db: AsyncSession = Depends(get_db)):
    result = await get_all_temperatures_crud(db=db)

    return result


@router.get("/{city_id}")
async def get_temperature(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> list[dict[str, Any]]:
    result = await get_max_temperature_for_city(db=db, city_id=city_id)

    return [t.model_dump() for t in result]
