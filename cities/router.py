from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from cities import schemas, crud
from cities.models import City
from cities.utils import get_city_or_404
from dependencies import DbSession

router = APIRouter(prefix="/cities", tags=["cities"])

CityOr404 = Annotated[City, Depends(get_city_or_404)]


@router.post(
    "/",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED,
)
async def create_city(db: DbSession, city: schemas.CityCreate):
    if await crud.get_city_by_name(db=db, name=city.name):
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return await crud.create_city(db=db, city=city)


@router.get("/", response_model=list[schemas.City])
async def cities_list(db: DbSession):
    return await crud.get_cities(db=db)


@router.get("/{city_id}/", response_model=schemas.CityDetail)
async def city_detail(city: CityOr404):
    return city


@router.put("/{city_id}/", response_model=schemas.City)
async def city_update(
    db: DbSession,
    city: CityOr404,
    city_data: schemas.CityUpdate,
):
    same_name_city = await crud.get_city_by_name(db=db, name=city_data.name)
    if same_name_city and same_name_city.id != city.id:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return await crud.update_city(db=db, db_city=city, city_data=city_data)


@router.delete("/{city_id}/")
async def city_delete(db: DbSession, city: CityOr404):
    await crud.delete_city(db=db, db_city=city)
    return {"detail": "City deleted"}
