from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from city_crud_api import schemas, crud
from dependencies import get_db, pagination_params


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityList])
async def read_cities(
        db: AsyncSession = Depends(get_db),
        pagination: tuple[int, int] = Depends(pagination_params)
) -> list[schemas.CityList]:
    skip, limit = pagination
    cities = await crud.get_cities(db, skip=skip, limit=limit)
    return cities


@router.post("/cities/", response_model=schemas.CityList)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.CityList:
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.CityList)
async def update_city(
        city_id: int,
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.CityList:
    db_city = await crud.update_city(db=db, city_id=city_id, city_update=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city_route(city_id: int, db: AsyncSession = Depends(get_db)) -> None:
    await crud.delete_city(db=db, city_id=city_id)
