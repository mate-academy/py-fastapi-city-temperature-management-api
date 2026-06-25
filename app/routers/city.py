from fastapi import APIRouter, HTTPException
from starlette import status

from app.database.config import AsyncDatabaseSession
from app.schemas.city import CitySchema, CityCreateSchema, CityUpdateSchema
from app.services.city import (
    retrieve_city,
    list_cities,
    retrieve_city_by_name,
    create_city,
    update_city,
    delete_city,
)

router = APIRouter(
    prefix="/api/cities",
    tags=["Cities API"],
)


@router.get(
    "/{city_id}/",
    response_model=CitySchema,
)
async def get_city_api(db: AsyncDatabaseSession, city_id: int):
    city = await retrieve_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    return city


@router.get(
    "/",
    response_model=list[CitySchema],
)
async def get_cities_api(db: AsyncDatabaseSession):
    cities = await list_cities(db=db)
    return cities


@router.post("/", response_model=CitySchema)
async def create_city_api(db: AsyncDatabaseSession, city: CityCreateSchema):
    db_city = await retrieve_city_by_name(db=db, city_name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already exists.")
    db_city = await create_city(db=db, city=city)
    return db_city


@router.patch("/{city_id}/", response_model=CitySchema)
async def update_city_api(
    db: AsyncDatabaseSession, city_id: int, city: CityUpdateSchema
):
    if city.name:
        db_city = await retrieve_city_by_name(db=db, city_name=city.name)
        if db_city and db_city.id != city_id:
            raise HTTPException(status_code=400, detail="City already exists.")
    db_city = await retrieve_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    db_city = await update_city(db=db, city_id=city_id, city=city)
    return db_city


@router.delete("/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city_api(db: AsyncDatabaseSession, city_id: int) -> None:
    city = await retrieve_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    await delete_city(db=db, city_id=city_id)
