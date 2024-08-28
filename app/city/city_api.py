from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.city import schemas, crud_city
from database import get_db

router = APIRouter()


async def get_db_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    try:
        yield db
    finally:
        await db.close()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db_session)
) -> list[schemas.City]:
    cities = await crud_city.get_all_city(db, skip=skip, limit=limit)
    return cities


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db_session)
) -> schemas.City:
    return await crud_city.create_city(db, city)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_single_city(
    city_id: int,
    db: AsyncSession = Depends(get_db_session)
) -> schemas.City:
    city = await crud_city.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db_session)
) -> schemas.City:
    updated_city = await crud_city.update_city(db, city_id, city)
    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city


@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db_session)
) -> None:
    result = await crud_city.delete_city(db, city_id)
    if result is None:
        raise HTTPException(status_code=404, detail="City not found")
