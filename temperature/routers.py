from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud

router = APIRouter()


@router.post(
    "/temperature/update/",
    response_model=schemas.TemperatureUpdate,
    summary="Update temperature",
    description=(
        f"This endpoint allows you to update the temperature for all "
        f"cities in the database from weatherapi. If some of the cities "
        f"are not available in the API, they will be returned in response"
    ),
)
async def update_temperature_for_cities(db: AsyncSession = Depends(get_db)):
    result = await crud.update_temperature(db)
    cities_total = result["updated"] + len(result["missing"])

    return {
        "cities_total": cities_total,
        "updated": result["updated"],
        "missing": result["missing"],
    }


@router.get(
    "/temperatures/",
    response_model=list[schemas.TemperatureResponse],
    summary="Get all temperatures",
    description=(
        f"This endpoint allows you to get all temperatures for all cities. "
        f"You can also filter the results by city_id, if that city_id not exists "
        f"empty list will be returned"
    ),
)
async def retrieve_temperature_list(
    city_id: int | None = None, db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_temperatures(db=db, city_id=city_id)
