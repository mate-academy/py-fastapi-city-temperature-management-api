from sqlalchemy.ext.asyncio import AsyncSession

from city_crud import schemas as city_schemas
from city_crud import crud as city_crud
from db.engine import get_db


from fastapi import Depends, Query, APIRouter

router = APIRouter()


@router.post("/", response_model=city_schemas.CityCreate)
async def create_city(
    city_create: city_schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    return await city_crud.create_city(db=db, city=city_create)


@router.get("/", response_model=list[city_schemas.CityResponse])
async def get_cities(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    cities = await city_crud.get_cities(db=db, skip=skip, limit=limit)

    return [city_schemas.CityResponse.model_validate(city) for city in cities]


@router.get("/{city_id}/", response_model=city_schemas.CityResponse)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await city_crud.get_city(db=db, city_id=city_id)


@router.put("/{city_id}/", response_model=city_schemas.CityResponse)
async def update_city(
    city_id: int,
    updated_city: city_schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
):
    db_city = await city_crud.update_city(
        db=db, city_id=city_id, updated_city=updated_city
    )

    return db_city


@router.delete("/{city_id}/")
async def delete_city(city_delete_id: int, db: AsyncSession = Depends(get_db)):
    result = await city_crud.delete_city(db=db, city_id=city_delete_id)

    return result
