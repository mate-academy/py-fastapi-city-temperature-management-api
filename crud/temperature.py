from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.temperature import Temperature
from schemas.temperature import TemperatureCreateSchema



async def get_temperature_by_id(
    db: AsyncSession,
    temp_id: int
) -> Temperature | None:
    result = await db.execute(
        select(Temperature).where(Temperature.id == temp_id)
    )
    return result.scalars().one_or_none()


async def get_temperatures_by_city_id(
    db: AsyncSession,
    city_id: int
) -> list[Temperature]:
    result = await db.execute(
        select(Temperature).where(Temperature.city_id == city_id)
    )
    return result.scalars().all()


async def create_temperature(
    db: AsyncSession,
    temp_in: TemperatureCreateSchema
) -> Temperature:
    temp = Temperature(**temp_in.model_dump())
    db.add(temp)
    await db.commit()
    await db.refresh(temp)
    return temp


async def update_temperature(
    db: AsyncSession,
    temp_id: int,
    temp_update: TemperatureCreateSchema
) -> Temperature | None:
    temp = await get_temperature_by_id(db, temp_id)
    if not temp:
        return None

    for key, value in temp_update.model_dump(exclude_unset=True).items():
        setattr(temp, key, value)

    await db.commit()
    await db.refresh(temp)
    return temp


async def get_all_temperatures(db: AsyncSession) -> list[Temperature]:
    result = await db.execute(select(Temperature))
    return result.scalars().all()


async def delete_temperature(
    db: AsyncSession,
    temp_id: int
) -> bool:
    result = await db.execute(
        delete(Temperature).where(Temperature.id == temp_id)
    )
    await db.commit()
    return result.rowcount > 0
