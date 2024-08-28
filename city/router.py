from typing import Callable, Sequence

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import crud, schemas
from models import City

router = APIRouter()


@router.get('/list/', response_model=list[schemas.City])
async def read_cities(
        db: AsyncSession = Depends(get_db)
) -> Sequence[City]:
    return await crud.get_list_city(db=db)


@router.get('/{city_id}/', response_model=schemas.City)
async def read_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(
            status_code=404, detail=f'City with id {city_id} not found'
        )
    return city


@router.post('/create/', response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.put('/{city_id}/update/', response_model=schemas.City)
async def update_city(
        city_id: int, city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db)
) -> Callable[[], int]:
    updated_city = await crud.update_city(db=db, city_id=city_id, city=city)
    if updated_city is None:
        raise HTTPException(
            status_code=404, detail=f'City with id {city_id} not found'
        )
    return updated_city


@router.delete('/cities/{city_id}', response_model=schemas.City)
async def delete_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> Callable[[], int]:
    city = await crud.delete_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(
            status_code=404, detail=f'City with id {city_id} not found'
        )
    return city
