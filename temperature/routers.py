from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud
from temperature.get_temperature import get_city_temperatures

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    temperature_records = await get_city_temperatures(db=db)
    return await crud.create_temperature_records(
        db=db,
        temperature_records=temperature_records
    )


@router.get("/temperatures/list", response_model=list[schemas.Temperature])
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_temperature_list(db=db)


@router.get(
    "/temperatures/",
    response_model=schemas.Temperature
)  # Endpoint format: "/temperatures/?city_id={city_id}"
async def get_temperatures_by_city_id(
        city_id: int = Query(
            ..., title="city_id",
            description="The ID of the city"
        ),
        db: AsyncSession = Depends(get_db)):
    city = await crud.get_temperatures_by_city_id(db=db, city_id=city_id)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city
