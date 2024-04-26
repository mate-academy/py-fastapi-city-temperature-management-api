import httpx
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models as temperature_models
from city import models as city_models
from temperature.utils import create_temp_entries

from fastapi.responses import JSONResponse


async def get_temp_list(
    db: AsyncSession, city_id: int | None = None
) -> list[temperature_models.DbTemperature]:

    query = select(temperature_models.DbTemperature)
    if city_id is not None:
        query = query.filter(
            temperature_models.DbTemperature.city_id == city_id
        )

    temp_list = await db.execute(query)

    return temp_list.scalars().all()


async def get_temp_detail(
    db: AsyncSession, temperature_id: int
) -> temperature_models.DbTemperature:

    query = select(temperature_models.DbTemperature).filter(
        temperature_models.DbTemperature.id == temperature_id
    )
    result = await db.execute(query)
    temp = result.scalar_one_or_none()

    if temp:
        return temp

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Temperature with id {temperature_id} not found",
    )


async def populate_temp_db(db: AsyncSession) -> JSONResponse:
    async with httpx.AsyncClient() as client:
        query = select(city_models.DbCity)
        city_list = await db.execute(query)
        cities = city_list.scalars().all()

        response_content = {
            "message": "Temperature entries updated.",
            "errors": [],
        }

        for city in cities:
            try:
                temperature = await create_temp_entries(
                    city=city, client=client
                )
                if temperature:
                    existing_entry = (
                        await db.execute(
                            select(temperature_models.DbTemperature).filter(
                                temperature_models.DbTemperature.city_id
                                == city.id
                            )
                        )
                    ).scalar_one_or_none()

                    if existing_entry:
                        existing_entry.date_time = temperature.date_time
                        existing_entry.temperature = temperature.temperature
                    else:
                        db.add(temperature)
                else:
                    response_content["errors"].append(
                        {
                            "city": city.name,
                            "error": "Temperature data not found",
                        }
                    )
            except Exception as e:
                response_content["errors"].append(
                    {"city": city.name, "error": str(e)}
                )

        await db.commit()
        return JSONResponse(content=response_content)
