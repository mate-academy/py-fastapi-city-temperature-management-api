from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.cities.schemas import City, CityCreate, CityUpdate
from app.cities import service

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=City, status_code=status.HTTP_201_CREATED)
async def create_city(city_data: CityCreate, db: AsyncSession = Depends(get_db)):
    db_city = await service.get_city_by_name(db, name=city_data.name)
    if db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists",
        )
    return await service.create_city(db, city_data=city_data)


@router.get("/", response_model=list[City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await service.get_all_cities(db)


@router.get("/{city_id}", response_model=City)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await service.get_city_by_id(db, city_id=city_id)
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return db_city


@router.put("/{city_id}", response_model=City)
async def update_city(
    city_id: int, city_data: CityUpdate, db: AsyncSession = Depends(get_db)
):
    db_city = await service.get_city_by_id(db, city_id=city_id)
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return await service.update_city(db, db_city=db_city, update_data=city_data)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await service.get_city_by_id(db, city_id=city_id)
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    await service.delete_city(db, db_city=db_city)
