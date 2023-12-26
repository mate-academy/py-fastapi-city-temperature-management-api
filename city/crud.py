from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import city.models as models
import city.schemas as schemas


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def check_city_name(db: AsyncSession, city_name: str) -> Optional[models.City]:
    return (
        db.query(models.City).filter(models.City.name == city_name).first()
    )


async def get_all_cities(
        db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


async def get_city(db: AsyncSession, city_id: int) -> models.City:
    return db.query(models.City).filter(models.City.id == city_id).first()


async def update_city(
        db: AsyncSession, city: schemas.CityCreate, city_id: int
) -> models.City:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city is None:
        raise HTTPException(status_code=404, detail="City is not found")

    for key, value in city.dict().items():
        setattr(db_city, key, value)

    await db.commit()
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    city = db.query(models.City).filter(models.City.id == city_id).first()

    if city is None:
        raise HTTPException(status_code=404, detail="City is not found")

    await db.delete(city)
    await db.commit()
