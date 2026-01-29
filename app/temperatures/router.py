from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.temperatures.models import Temperature

from app.db.session import get_db
from app.cities.models import City
from sqlalchemy import select
from app.temperatures.schemas import TemperatureRead
from app.temperatures import crud
from app.temperatures.services.weather import fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])

@router.get("/", response_model=list[TemperatureRead])
async def read_temperatures(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperatures(db, city_id)

@router.post("/update")
async def update_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        result = await db.scalars(select(City))
        cities = result.all()

        temperatures: list[Temperature] = []

        for city in cities:
            temperature = await fetch_current_temperature(
                city.latitude,
                city.longitude,
            )

            temperatures.append(
                Temperature(
                    city_id=city.id,
                    temperature=temperature,
                )
            )

        db.add_all(temperatures)
        await db.commit()

        return {
            "status": "ok",
            "records_created": len(temperatures),
        }

    except Exception:
        await db.rollback()
        raise
