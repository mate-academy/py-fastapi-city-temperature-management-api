from fastapi import FastAPI, Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_db
from schemas.city import (
    CityReadSchema,
    CityCreateSchema,
    CityUpdateSchema,
    CityPartialUpdateSchema
)
from services.city import (
    get_cities as get_cities_service,
    get_city as get_city_service,
    create_city as create_city_service,
    update_city as update_city_service,
    delete_city as delete_city_service,
    partial_update_city as partial_update_city_service
)


city_router = APIRouter()


@city_router.get(path="/")
async def root() -> dict:
    return {"message": "Hello World"}


@city_router.post(
    path="/cities/",
    response_model=CityReadSchema,
    status_code=status.HTTP_200_OK
)
async def create_city(
        city_schema: CityCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    return await create_city_service(city_schema, db)


@city_router.get(
    path="/cities/",
    response_model=list[CityReadSchema],
    status_code=status.HTTP_200_OK
)
async def get_cities(
        db: AsyncSession = Depends(get_db)
):
    return await get_cities_service(db)


@city_router.get(
    path="/cities/{city_id}/",
    response_model=CityReadSchema,
    status_code=status.HTTP_200_OK
)
async def get_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    return await get_city_service(city_id, db)


@city_router.put(
    path="/cities/{city_id}/",
    response_model=CityReadSchema,
    status_code=status.HTTP_200_OK
)
async def update_city(
        city_id: int,
        city_schema: CityUpdateSchema,
        db: AsyncSession = Depends(get_db)
):
    return await update_city_service(city_id, city_schema, db)


@city_router.patch(
    path="/cities/{city_id}/",
    response_model=CityReadSchema,
    status_code=status.HTTP_200_OK
)
async def partial_update_city(
        city_id: int,
        city_schema: CityPartialUpdateSchema,
        db: AsyncSession = Depends(get_db)
):
    return await partial_update_city_service(
        city_id,
        city_schema,
        db
    )


@city_router.delete(
    path="/cities/{city_id}/",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    await delete_city_service(city_id, db)
