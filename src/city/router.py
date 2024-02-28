from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db
from src.city import schemas, service

router = APIRouter(
    prefix="/cities",
    tags=["cities"],
)


DBDepend = Depends(get_db)


@router.get("/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = DBDepend):
    return await service.get_all_cities(db=db)


@router.get("/{city_id}/", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = DBDepend):
    return await service.get_city(db=db, city_id=city_id)


@router.post("/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = DBDepend,
):
    return await service.create_city(db=db, city=city)


@router.put("/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: AsyncSession = DBDepend,
):
    return await service.update_city(db=db, city_id=city_id, city=city)


@router.delete("/{city_id}/")
async def delete_city(
    city_id: int,
    db: AsyncSession = DBDepend,
):
    return await service.delete_city(db=db, city_id=city_id)
