from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from city_temperature_api.database.models.city import City
from city_temperature_api.database.session.engine import get_db
from city_temperature_api.schemas.city import (
    CityResponse,
    CityUpdate,
    CityCreate
)


router = APIRouter()


@router.post("/", response_model=CityResponse, status_code=201)
async def create_city(
        city_date: CityCreate,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(City).filter(City.name == city_date.name)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists"
        )

    new_city = City(
        name=city_date.name,
        additional_info=city_date.additional_info
    )
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)

    return new_city


@router.get("/", response_model=list[CityResponse])
async def get_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).options(
        selectinload(City.temperatures)
    ))
    cities = result.scalars().all()
    return cities


@router.put("/{city_id}", response_model=CityResponse)
async def update_city(
        city_id: int,
        updated_data: CityUpdate,
        db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalars().first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    if updated_data.name is not None:
        city.name = updated_data.name
    if updated_data.additional_info is not None:
        city.additional_info = updated_data.additional_info

    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


@router.delete("/{city_id}", status_code=204)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalars().first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    # Видаляємо запис
    await db.delete(city)
    await db.commit()

    return
