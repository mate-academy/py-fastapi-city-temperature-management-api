from datetime import datetime, timezone
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.temperature import models as temperature_models
from src.city import models as city_models
from src.temperature.weather_service import fetch_temperature_for_city


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None):
    query = select(temperature_models.TemperatureModel)

    if city_id is not None:
        query = query.where(temperature_models.TemperatureModel.city_id == city_id)

    result = await db.execute(query)

    temperatures = result.scalars().all()
    return temperatures


async def update_all_temperatures(db: AsyncSession):
    result = await db.execute(select(city_models.CityModel))
    cities = result.scalars().all()

    successes = []
    failures = []

    for city in cities:
        try:
            temperature = await fetch_temperature_for_city(city.name)

            new_record = temperature_models.TemperatureModel(
                city_id=city.id,
                date_time=datetime.now(timezone.utc),
                temperature=temperature
            )

            db.add(new_record)
            successes.append({"city": city.name, "temperature": temperature})
        except HTTPException as e:
            failures.append({"city": city.name, "error": e.detail})
        except Exception as e:
            failures.append({"city": city.name, "error": str(e)})

    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update temperatures: {str(e)}")

    return {
        "updated": len(successes),
        "failed": len(failures),
        "successes": successes,
        "failures": failures,
    }
