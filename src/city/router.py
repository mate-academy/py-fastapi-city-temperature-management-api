from fastapi import APIRouter, Response
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from src.city.schemas import CityRead, CityCreate, CityUpdate
from src.city.crud import create_city, read_all_cities, read_city_by_id, \
    put_city_by_id, delete_city_by_id
from src.database.dependencies import get_db

router = APIRouter()

@router.post("/cities", response_model=CityRead)
async def add_new_city(
    city_data: CityCreate,
    db: Session=Depends(get_db),
) -> CityRead:
    city = await create_city(db=db, city_data=city_data)
    return CityRead.model_validate(city)

@router.get("/cities", response_model=list[CityRead])
async def get_cities(
    db: AsyncSession=Depends(get_db),
) -> list[CityRead]:
    return await read_all_cities(db=db)

@router.get("/cities/{city_id}", response_model=CityRead)
async def get_city_by_id(
        city_id: int,
        db: AsyncSession=Depends(get_db),
) -> CityRead:
    city = await read_city_by_id(db=db, city_id=city_id)
    return CityRead.model_validate(city)

@router.put("/cities/{city_id}", response_model=CityRead)
async def update_city(
        city_data: CityUpdate,
        city_id: int,
        db: AsyncSession=Depends(get_db),
) -> CityRead:
    city = await put_city_by_id(db=db, city_id=city_id, data=city_data)
    return CityRead.model_validate(city)

@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession=Depends(get_db)):
    await delete_city_by_id(db=db, city_id=city_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
