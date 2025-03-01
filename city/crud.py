from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.exc import UnmappedInstanceError
from city.models import DBCity
from city.schemas import CityCreate, City


async def create_city(db: AsyncSession, city: CityCreate):
    """
    Create a new city in the database.

    Args:
        db (AsyncSession): Database session.
        city (CityCreate): Pydantic model with city data.

    Returns:
        City: The created city instance.
    """
    db_city = DBCity(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_all_cities(db: AsyncSession, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of cities from the database.

    Args:
        db (AsyncSession): Database session.
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.

    Returns:
        list[City]: List of cities.
    """
    result = await db.execute(select(DBCity).offset(skip).limit(limit))
    cities = result.scalars().all()
    return cities


async def get_city_by_id(db: AsyncSession, city_id: int):
    """
    Retrieve a specific city by its ID.

    Args:
        db (AsyncSession): Database session.
        city_id (int): ID of the city.

    Returns:
        City: The city instance.
    """
    result = await db.execute(select(City).where(DBCity.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise NoResultFound(f"City with id {city_id} does not exist.")
    return city


async def delete_city_by_id(db: AsyncSession, city_id: int) -> None:
    """
    Delete a city by its ID.

    Args:
        db (AsyncSession): Database session.
        city_id (int): ID of the city to delete.

    Returns:
        None
    """
    try:
        result = await db.execute(select(DBCity).where(DBCity.id == city_id))
        city = result.scalar_one_or_none()
        if not city:
            raise NoResultFound(f"City with id {city_id} does not exist.")

        await db.delete(city)
        await db.commit()
    except NoResultFound:
        raise
    except UnmappedInstanceError:
        raise ValueError("An attempt was made to delete an unknown object.")


async def update_city_by_id(db: AsyncSession, city_id: int, updated_data: CityCreate):
    """
    Update a specific city's data by its ID.

    Args:
        db (AsyncSession): Database session.
        city_id (int): ID of the city to update.
        updated_data (CityCreate): Pydantic model containing new data for the city.

    Returns:
        City: The updated city instance.
    """
    # Find the city to be updated
    result = await db.execute(select(DBCity).where(DBCity.id == city_id))
    city = result.scalar_one_or_none()

    if not city:
        raise NoResultFound(f"City with id {city_id} not found.")

    # Update the city
    city.name = updated_data.name
    city.additional_info = updated_data.additional_info

    # Commit changes
    db.add(city)
    await db.commit()
    await db.refresh(city)

    return city
