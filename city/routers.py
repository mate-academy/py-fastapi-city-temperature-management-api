from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from settings import settings
from city import schemas, crud
from dependencies import get_db


prefix = settings.API_PREFIX
router = APIRouter()


@router.get(f"{prefix}/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.post(
    f"{prefix}/cities/",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED
)
async def new_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_city(db=db, city=city)


@router.get(prefix + "/cities/{city_id}/", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.retrieve_city(db=db, id=city_id)


@router.put(prefix + "/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_city(db=db, id=city_id, city_data=city.dict())


@router.delete(prefix + "/cities/{city_id}/", response_model=dict)
async def delete_city(city_id: int, response: Response, db: AsyncSession = Depends(get_db)):
    await crud.delete_city(db=db, id=city_id)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response
