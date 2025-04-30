from fastapi import Depends, Query, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_cities
from temperature import crud
from dependencies import get_db
from temperature.crud import fetch_temperature_for_city
from temperature.schemas import TemperatureListSchema, TemperatureRetrieveSchema

router = APIRouter()


@router.get(
    "/temperatures/",
    response_model=TemperatureListSchema | TemperatureRetrieveSchema)
async def temperatures_list(
        city_id: int = Query(None),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db),
):
    total_items = await crud.get_temperature_count(db=db, city_id=city_id)
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No temperature found.")

    total_pages = (total_items + per_page - 1) // per_page
    temperatures_list = await crud.get_temperature(
        db=db,
        skip=(page - 1) * per_page,
        limit=per_page,
        city_id=city_id
    )

    prev_page = f"/temperatures/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/temperatures/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return TemperatureListSchema(
        temperatures_list=temperatures_list,
        total_items=total_items,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page
    )


@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_cities(db)

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")

    for city in cities:
        temperature = await fetch_temperature_for_city(city.name)
        if temperature is not None:
            await crud.create_temperature(
                db=db,
                city=city,
                temperature=temperature
            )

    return {"status": "temperatures updated"}
