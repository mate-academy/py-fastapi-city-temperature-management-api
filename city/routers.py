from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import post_city, get_cities, get_city, update_city, delete_city
from city.schemas import City
from dependencies import get_db

router = APIRouter()


@router.post("/cities")
async def city_post(city: City, db: AsyncSession = Depends(get_db)):
    return await post_city(db, city)


@router.get("/cities")
async def cities_get(db: AsyncSession = Depends(get_db)):
    return await get_cities(db)


@router.get("/cities/{city_id}")
async def city_get(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await get_city(db, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.put("/cities/{city_id}")
async def city_update(
        city_id: int,
        name: str,
        additional_info: str,
        db: AsyncSession = Depends(get_db)
):
    city = await get_city(db, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return await update_city(db, city_id, name, additional_info)


@router.delete("/cities/{city_id}")
async def city_delete(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await get_city(db, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return await delete_city(db, city_id)
