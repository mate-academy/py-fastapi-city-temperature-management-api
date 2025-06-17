from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.city import City
from schemas.city import CityCreateSchema


async def get_all_cities(db: AsyncSession):
    query = select(City)
    result = await db.execute(query)
    return result.scalars().all()


async def create_city(db: AsyncSession, city_data: CityCreateSchema):

    existing_city = await db.execute(select(City).where(City.name == city_data.name))

    if existing_city.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City with name '{city_data.name}' already exists"
        )

    new_city = City(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )

    try:
        db.add(new_city)
        await db.commit()
        await db.refresh(new_city)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating city: {e}"
        )

    return new_city


async def delete_city(db: AsyncSession, city_id: int):
    city_to_delete = await db.get(City, city_id)

    if not city_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found"
        )

    try:
        await db.delete(city_to_delete)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting city: {e}"
        )

    return {"message": f"City with id {city_id} deleted successfully"}
