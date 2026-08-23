import asyncio

import httpx
from fastapi import APIRouter, HTTPException

from dependencies import PaginationDep, DB
from temperature import schemas, crud, weather
from city import crud as city_crud

router = APIRouter()


@router.get(
    "/temperatures/",
    response_model=list[schemas.Temperature],
    responses={
        200: {"description": "List of temperature records returned successfully"},
    },
)
async def read_temperatures(
    db: DB,
    pagination: PaginationDep,
    city_id: int | None = None,
):
    if city_id is not None:
        return await crud.get_temperature_by_city_id(
            db=db,
            city_id=city_id,
            pagination=pagination,
        )
    return await crud.get_all_temperature(
        db=db,
        pagination=pagination,
    )


@router.post(
    "/temperatures/update/",
    response_model=list[schemas.TemperatureOut],
    responses={
        200: {"description": "Temperatures fetched and stored successfully"},
        404: {"description": "No cities found in the database"},
    },
)
async def update_temperatures(
    db: DB,
    pagination: PaginationDep,
):
    cities = await city_crud.get_all_cities(
        db=db,
        pagination=pagination,
    )

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")

    async with httpx.AsyncClient(timeout=10.0) as client:
        fetched = await asyncio.gather(
            *(weather.fetch_current_temperature(client, c.name) for c in cities),
            return_exceptions=True,
        )

    results = []
    for city_obj, temperature in zip(cities, fetched):
        if not isinstance(temperature, float):
            continue
        results.append(
            await crud.create_temperature(db=db, city_id=city_obj.id, value=temperature)
        )

    return results
