from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.cities.crud import create_new_city, delete_city_by_id, get_all_cities
from src.cities.models import DBCity
from src.cities.schemas import City, CityCreate, CRUDDetails
from src.dependencies import get_db

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[City])
async def read_cities(db: AsyncSession = Depends(get_db)) -> list[DBCity]:
    return await get_all_cities(db)


@router.post("/", response_model=CRUDDetails)
async def create_city(
    city: CityCreate, db: AsyncSession = Depends(get_db)
) -> CRUDDetails:
    return await create_new_city(db, city)


@router.delete("/{city_id}", response_model=CRUDDetails)
async def delete_city(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> CRUDDetails:
    return await delete_city_by_id(db, city_id)
