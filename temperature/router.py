from fastapi import APIRouter

from dependencies import Pagination, DB

from temperature import schemas, crud


router = APIRouter()


@router.get(
    "/temperatures/update/",
    response_model=schemas.TemperatureUpdate,
)
async def create_temperature(
    db: DB
) -> dict:
    return await crud.update_temperatures(db=db)


@router.get(
    "/temperatures/",
    response_model=list[schemas.Temperature],
)
async def get_temperatures(
    db: DB,
    pagination: Pagination
) -> list[schemas.Temperature]:
    return await crud.get_all_temperatures(db=db, **pagination)


@router.get(
    "/temperatures/{city_id}/",
    response_model=list[schemas.Temperature],
)
async def get_temperatures_by_city_id(
        db: DB,
        pagination: Pagination,
        city_id: int
) -> list[schemas.Temperature]:
    return await crud.get_temperatures_by_city_id(db=db,
                                                  city_id=city_id,
                                                  **pagination)
