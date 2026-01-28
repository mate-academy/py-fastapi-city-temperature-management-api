from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.city import (
    CityAlreadyExistsError,
    create_city,
    delete_city,
    get_city,
    list_cities,
    update_city,
)
from app.db.session import get_db
from app.schemas.city import CityCreate, CityRead, CityUpdate

router = APIRouter(prefix="/cities")


@router.post("", response_model=CityRead, status_code=status.HTTP_201_CREATED)
async def create_city_endpoint(data: CityCreate, db: AsyncSession = Depends(get_db)) -> CityRead:
    try:
        city = await create_city(db, data)
    except CityAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return city


@router.get("", response_model=list[CityRead])
async def list_cities_endpoint(db: AsyncSession = Depends(get_db)) -> list[CityRead]:
    return await list_cities(db)


@router.get("/{city_id}", response_model=CityRead)
async def get_city_endpoint(city_id: int, db: AsyncSession = Depends(get_db)) -> CityRead:
    city = await get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=CityRead)
async def update_city_endpoint(
    city_id: int,
    data: CityUpdate,
    db: AsyncSession = Depends(get_db),
) -> CityRead:
    city = await get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    try:
        return await update_city(db, city, data)
    except CityAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city_endpoint(city_id: int, db: AsyncSession = Depends(get_db)) -> None:
    city = await get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    await delete_city(db, city)
