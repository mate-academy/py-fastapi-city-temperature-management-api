from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud
from city import crud as city_crud

router = APIRouter()


@router.post(
    "/temperatures/update/",
    response_model=list[schemas.Temperature],
    status_code=201
)
async def update_temperature(db: AsyncSession = Depends(get_db)):
    city_list = await city_crud.get_city_list(db=db)

    result = await crud.update_all_cities_temperatures(
        db=db,
        cities=city_list
    )

    return result


@router.get(
    "/temperatures/",
    response_model=list[schemas.Temperature],
    response_model_exclude_none=True,
)
async def read_temperature(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    if city_id is None:
        return await crud.get_temperature_list(db=db)

    result = await crud.get_temperature_by_city_id(db=db, city_id=city_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Temperature for city with id {city_id} not found"
        )

    return result
