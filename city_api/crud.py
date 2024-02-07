from fastapi import HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    city_list = await db.execute(select(models.City))
    return [city[0] for city in city_list.fetchall()]


async def get_city_by_name(db: AsyncSession, name: str) -> models.City | None:
    result = await db.execute(
        select(models.City).filter(models.City.name == name)
    )
    city = result.scalars().first()
    return city


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | HTTPException:
    result = await db.execute(
        select(models.City).filter(models.City.id == city_id)
    )
    city = result.scalars().first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City | HTTPException:
    existing_city = await get_city_by_name(db=db, name=city.name)

    if existing_city:
        raise HTTPException(status_code=400, detail="Such name for City already exists")

    new_city = models.City(**city.dict())
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def update_city(db: AsyncSession, city: schemas.CityUpdate, city_id: int) -> None:
    existing_city = await get_city_by_id(db=db, city_id=city_id)

    update_data = city.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_city, key, value)
    await db.commit()


async def delete_city(db: AsyncSession, city_id: int) -> Response:
    city = await get_city_by_id(db, city_id)
    await db.delete(city)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
