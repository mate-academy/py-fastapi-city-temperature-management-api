from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import dependencies
from city.crud import get_cities
from temperature import crud, schemas
from temperature.utils import get_temperature

router = APIRouter()


@router.post("/temperatures/update/")
async def add_temperature(
    db: AsyncSession = Depends(dependencies.get_db)
):
    cities = await get_cities(db=db)

    for city in cities:
        try:
            temperature_data = await get_temperature(city)

            temperature_create = schemas.TemperatureCreate(
                temperature=temperature_data.get("current").get("temp_c"),
                city_id=city.id
            )
            await crud.create_temperature(
                db=db, temperature=temperature_create
            )
        except AttributeError:
            return {"message": "City with id: {} cannot be "
                               "accessed with weather api".format(city.id)}

    return {"message": "Temperature was updated successfully"}


@router.get("/temperatures/", response_model=list[schemas.TemperatureList])
async def get_temperatures_list(
        db: AsyncSession = Depends(dependencies.get_db),
        city_id: int = None
):
    return await crud.get_temperatures(db=db, city_id=city_id)
