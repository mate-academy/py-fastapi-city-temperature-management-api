from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db
from schemas.city import CityCreate, CityRead
from crud.city import (
    get_cities,
    get_city_by_id,
    create_city,
    update_city,
    delete_city,
)

router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("", response_model=list[CityRead])
async def list_cities(db: AsyncSession = Depends(get_db)):
    return await get_cities(db)


@router.get("/{city_id}", response_model=CityRead)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await get_city_by_id(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("", response_model=CityRead, status_code=status.HTTP_201_CREATED)
async def create_city_endpoint(payload: CityCreate, db: AsyncSession = Depends(get_db)):
    return await create_city(db, payload)


@router.put("/{city_id}", response_model=CityRead)
async def put_city(city_id: int, payload: CityCreate, db: AsyncSession = Depends(get_db)):
    city = await update_city(db, city_id, payload)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_city(city_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_city(db, city_id)
    if not ok:
        raise HTTPException(status_code=404, detail="City not found")
    return None
