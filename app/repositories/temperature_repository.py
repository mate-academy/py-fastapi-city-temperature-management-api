from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.temperature import DBTemperature
from typing import Sequence


class TemperatureRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> Sequence[DBTemperature]:
        result = await self.session.execute(select(DBTemperature))
        return result.scalars().all()

    async def get_by_city(self, city_id: int):
        query = select(DBTemperature).where(DBTemperature.city_id == city_id)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def create_many(self, temperatures: list[DBTemperature]):
        self.session.add_all(temperatures)
        await self.session.commit()
